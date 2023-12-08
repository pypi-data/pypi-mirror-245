import dataclasses
import threading
import time
from enum import Enum
from pathlib import Path
from typing import Callable, Dict, List, Optional

import numpy as np
import toml  # type: ignore

from ribot.control.arm_kinematics import ArmKinematics, ArmParameters, ArmPose
from ribot.control.controller_servers import ControllerServer, WebsocketServer
from ribot.utils.algebra import allclose
from ribot.utils.fifo_lock import FIFOLock
from ribot.utils.messages import Message, MessageOp
from ribot.utils.prints import console


class Settings(Enum):
    HOMING_DIRECTION = 1
    SPEED_RAD_PER_S = 5
    STEPS_PER_REV_MOTOR_AXIS = 9
    CONVERSION_RATE_AXIS_JOINTS = 13
    HOMING_OFFSET_RADS = 17
    DIR_INVERTED = 31


@dataclasses.dataclass
class Setting:
    value: float
    code_set: int
    code_get: int
    last_updated: float = -1


class ControllerStatus(Enum):
    NOT_STARTED = 0
    WAITING_CONNECTION = 1
    RUNNING = 2
    STOPPED = 3


class ArmController:
    def __init__(
        self,
        arm_parameters: ArmParameters,
        websocket_port: int = 8600,
        server_port: int = 8500,
    ) -> None:
        self._current_angles: List[float] = [0, 0, 0, 0, 0, 0]
        self.current_angles_lock: FIFOLock = FIFOLock()

        self.target_pose: Optional[ArmPose] = None

        self.tool_value: float = 0
        self.move_queue_size: int = 0
        self.is_homed: bool = False

        self.config_file: Optional[Path] = None

        self.arm_params = arm_parameters
        self.num_joints: int = len(self._current_angles)
        self.kinematics: ArmKinematics = ArmKinematics(self.arm_params)

        self.joint_settings: List[Dict[Settings, Setting]] = []
        self.joint_settings_response_code: List[Dict[int, Setting]] = []

        self.last_status_time: float = 0

        self.status: ControllerStatus = ControllerStatus.NOT_STARTED

        self.print_status = False
        self.print_idx = 0

        self.stop_event: threading.Event = threading.Event()

        self.controller_server: ControllerServer = ControllerServer(self, server_port)
        self.websocket_server: Optional[WebsocketServer] = WebsocketServer(self, websocket_port)
        self.websocket_port = websocket_port
        self.file_reload_thread: Optional[threading.Thread] = None

        self.message_op_handlers: Dict[MessageOp, Callable[[Message], None]] = {
            MessageOp.MOVE: self.handle_move_message,
            MessageOp.STATUS: self.handle_status_message,
            MessageOp.CONFIG: self.handle_config_message,
        }

        for _ in range(self.num_joints):
            current_joint_settings = {
                Settings.HOMING_DIRECTION: Setting(value=1, code_set=1, code_get=3),
                Settings.SPEED_RAD_PER_S: Setting(value=1, code_set=5, code_get=7),
                Settings.STEPS_PER_REV_MOTOR_AXIS: Setting(value=200, code_set=9, code_get=11),
                Settings.CONVERSION_RATE_AXIS_JOINTS: Setting(value=1, code_set=13, code_get=15),
                Settings.HOMING_OFFSET_RADS: Setting(value=np.pi / 4, code_set=17, code_get=19),
                Settings.DIR_INVERTED: Setting(value=0, code_set=31, code_get=33),
            }
            self.joint_settings.append(current_joint_settings)
            self.joint_settings_response_code.append(
                {setting.code_get + 1: setting for setting in current_joint_settings.values()}
            )

    """
    ----------------------------------------
                    General Methods
    ----------------------------------------
    """

    def __str__(self) -> str:
        output = []
        output.append(f"Current Angles: {self._current_angles}")
        output.append(f"Tool Position: {self.tool_value}")
        output.append(f"Is Homed: {self.is_homed}")
        output.append(f"Queue Size: {self.move_queue_size}")

        return " ".join(output)

    def start(self, wait: bool = False, websocket_server: bool = True) -> None:
        console.log("Starting controller!", style="setup")

        if websocket_server and self.websocket_server is not None:
            self.websocket_server.start()
        else:
            self.websocket_server = None

        connection_controller_timeout = 60
        self.controller_server.start()
        start_time = time.time()
        if wait:
            while not self.is_ready and not self.stop_event.is_set():
                time.sleep(2)
                if time.time() - start_time > connection_controller_timeout:
                    raise TimeoutError("Controller took too long to start, check arm client")

        self.status = ControllerStatus.WAITING_CONNECTION

        console.log("\nController Started!", style="setup")

    def stop(self) -> None:
        console.log("Stopping controller...", style="setup", end="\n")
        self.stop_event.set()
        self.status = ControllerStatus.STOPPED

        if self.websocket_server is not None:
            self.websocket_server.stop()

        self.controller_server.stop()

        if self.file_reload_thread is not None and self.file_reload_thread.is_alive():
            self.file_reload_thread.join()

        console.log("Controller Stopped", style="setup")
        exit()

    @property
    def current_pose(self) -> ArmPose:
        return self.kinematics.angles_to_pose(self.current_angles)

    @property
    def current_angles(self) -> List[float]:
        with self.current_angles_lock:
            return self._current_angles

    @current_angles.setter
    def current_angles(self, angles: List[float]) -> None:
        if len(angles) != self.num_joints:
            raise ValueError(f"Angles must be a list of length {self.num_joints}")
        with self.current_angles_lock:
            self._current_angles = angles

    @property
    def is_ready(self) -> bool:
        if self.websocket_server is None:
            websocket_server_up = True
        else:
            websocket_server_up = self.websocket_server.is_ready
        controller_server_up = self.controller_server.is_ready

        return websocket_server_up and controller_server_up

    def set_config_file(self, file: Path) -> None:
        self.config_file = file

    def configure(self) -> None:
        if self.config_file is not None:
            self.configure_from_file(self.config_file)

    def configure_from_file(self, file: Path, reload: bool = True) -> None:
        contents = toml.load(file)
        joint_configuration = contents["joint_configuration"]
        joints = contents["joints"]
        arm_params = contents["arm_parameters"]
        for key, value in arm_params.items():
            self.arm_params.__setattr__(key, value)

        # Tool settings

        tool = contents["tool"]
        tool_driver = tool["driver"]
        if tool_driver["type"] == "servo":
            pin = int(tool_driver["pin"])
            self.set_tool_driver_servo(pin)

        default_speed = joint_configuration["speed_rad_per_s"]
        default_homing_direction = joint_configuration["homing_direction"]
        default_steps_per_rev_motor_axis = joint_configuration["steps_per_rev_motor_axis"]
        default_conversion_rate_axis_joint = joint_configuration["conversion_rate_axis_joint"]
        default_homing_offset_rads = joint_configuration["homing_offset_rad"]
        default_min_angle_rad = joint_configuration["min_angle_rad"]
        default_max_angle_rad = joint_configuration["max_angle_rad"]
        default_dir_inverted = joint_configuration["dir_inverted"]

        for i, joint in enumerate(joints):
            if "speed_rad_per_s" not in joint.keys():
                joint["speed_rad_per_s"] = default_speed

            if "homing_direction" not in joint.keys():
                joint["homing_direction"] = default_homing_direction

            if "steps_per_rev_motor_axis" not in joint.keys():
                joint["steps_per_rev_motor_axis"] = default_steps_per_rev_motor_axis

            if "conversion_rate_axis_joint" not in joint.keys():
                joint["conversion_rate_axis_joint"] = default_conversion_rate_axis_joint

            if "homing_offset_rad" not in joint.keys():
                joint["homing_offset_rad"] = default_homing_offset_rads

            if "min_angle_rad" not in joint.keys():
                joint["min_angle_rad"] = default_min_angle_rad

            if "max_angle_rad" not in joint.keys():
                joint["max_angle_rad"] = default_max_angle_rad

            if "dir_inverted" not in joint.keys():
                joint["dir_inverted"] = default_dir_inverted

            speed = joint["speed_rad_per_s"]
            homing_direction = joint["homing_direction"]
            steps_per_rev_motor_axis = joint["steps_per_rev_motor_axis"]
            conversion_rate_axis_joint = joint["conversion_rate_axis_joint"]
            homing_offset_rads = joint["homing_offset_rad"]
            min_angle_rad = joint["min_angle_rad"]
            max_angle_rad = joint["max_angle_rad"]
            dir_inverted = joint["dir_inverted"]

            driver = joint["driver"]
            if driver["type"] == "stepper":
                step_pin = driver["step_pin"]
                dir_pin = driver["dir_pin"]
                self.set_joint_driver_stepper(i, step_pin, dir_pin)
            elif driver["type"] == "servo":
                pin = driver["pin"]
                self.set_joint_driver_servo(i, pin)

            endstop = joint["endstop"]
            if endstop["type"] == "hall":
                pin = endstop["pin"]
                self.set_joint_endstop_hall(i, pin)
            elif endstop["type"] == "dummy":
                self.set_joint_endstop_dummy(i)
            elif endstop["type"] == "none":
                self.set_joint_endstop_none(i)

            self.set_setting_joint(Settings.SPEED_RAD_PER_S, speed, i)
            self.set_setting_joint(Settings.HOMING_DIRECTION, homing_direction, i)
            self.set_setting_joint(Settings.STEPS_PER_REV_MOTOR_AXIS, steps_per_rev_motor_axis, i)
            self.set_setting_joint(Settings.CONVERSION_RATE_AXIS_JOINTS, conversion_rate_axis_joint, i)
            self.set_setting_joint(Settings.HOMING_OFFSET_RADS, homing_offset_rads, i)
            self.set_setting_joint(Settings.DIR_INVERTED, dir_inverted, i)

            self.arm_params.joints[i].set_bounds(min_angle_rad, max_angle_rad)

        self.print_state()
        if reload:
            self.file_reload_thread = threading.Thread(target=self.check_and_reload_config, args=(file,))
            self.file_reload_thread.start()

    def check_and_reload_config(self, file: Path) -> None:
        start_time = time.time()
        while not self.stop_event.is_set():
            if file.stat().st_mtime > start_time:
                self.configure_from_file(file)
                start_time = time.time()
            time.sleep(3)
        exit(0)

    def set_status_running(self) -> None:
        self.status = ControllerStatus.RUNNING

    """
    ----------------------------------------
                    Handlers
    ----------------------------------------
    """

    def handle_move_message(self, _: Message) -> None:
        pass

    def check_last_status(self) -> None:
        current_time = time.time()
        if self.last_status_time == 0:
            return

        if current_time - self.last_status_time > 5:
            console.log("No status message received", style="error")
            self.stop()

    def handle_status_message(self, message: Message) -> None:
        code = message.code
        if code == 1:
            self.current_angles = message.args[: self.num_joints]
            self.tool_value = message.args[self.num_joints]
            self.move_queue_size = int(message.args[self.num_joints + 1])
            self.is_homed = message.args[self.num_joints + 2] == 1
            if self.print_status:
                if self.print_idx == 5:
                    console.log(self, style="status")
                    self.print_idx = 0
                self.print_idx += 1
            self.last_status_time = time.time()

    def handle_config_message(self, message: Message) -> None:
        code = message.code
        joint_idx = int(message.args[0])
        if code in self.joint_settings_response_code[joint_idx].keys():
            setting = self.joint_settings_response_code[joint_idx][code]
            setting.value = message.args[1]
            setting.last_updated = time.time()

    """
    ----------------------------------------
                    API Methods -- MOVE
    ----------------------------------------
    """

    def move_joints_to(self, angles: List[float]) -> bool:
        if not self.is_homed:
            console.log("Arm is not homed", style="error")
            return False
        message = Message(MessageOp.MOVE, 1, angles)
        self.controller_server.send_message(message, mutex=True)
        self.move_queue_size += 1

        if self.print_status:
            console.log(f"Moving to angles: {angles}", style="move_angles")
        return True

    def move_to(
        self,
        pose: ArmPose,
    ) -> bool:
        self.target_pose = pose
        target_angles = self.kinematics.pose_to_angles(pose, self.current_angles)
        if target_angles is None:
            console.log("Target pose is not reachable", style="error")
            return False
        return self.move_joints_to(target_angles)

    def move_to_relative(
        self,
        pose: ArmPose,
    ) -> bool:
        if self.target_pose is None:
            self.target_pose = self.current_pose

        self.target_pose = self.target_pose + pose
        return self.move_to(self.target_pose)

    def home(self, wait: bool = True) -> None:
        if self.print_status:
            console.log("Homing arm...", style="homing")

        message = Message(MessageOp.MOVE, 3)
        self.controller_server.send_message(message, mutex=True)
        start_time = time.time()
        self.is_homed = False
        time.sleep(1)
        if wait:
            while not self.is_homed and not self.stop_event.is_set():
                time.sleep(0.1)
                if time.time() - start_time > 60:
                    raise TimeoutError("Arm took too long to home")
            # wait for angles to get to 0
            start_time = time.time()

            while not all([abs(angle) < 0.1 for angle in self.current_angles]) and not self.stop_event.is_set():
                time.sleep(0.1)
                if time.time() - start_time > 60:
                    raise TimeoutError("Arm took too long to home")
        if self.print_status:
            console.log("Arm homed!", style="homing")

    def move_joint_to(self, joint_idx: int, angle: float) -> bool:
        message = Message(MessageOp.MOVE, 9, [joint_idx, angle])
        self.controller_server.send_message(message, mutex=True)
        self.target_pose = None
        self.move_queue_size += 1
        if self.print_status:
            console.log(f"Moving joint {joint_idx} to angle: {angle}", style="move_joints")
        return True

    def home_joint(self, joint_idx: int) -> None:
        message = Message(MessageOp.MOVE, 5, [joint_idx])

        self.controller_server.send_message(message, mutex=True)

    def move_joint_to_relative(self, joint_idx: int, angle: float) -> bool:
        message = Message(MessageOp.MOVE, 11, [joint_idx, angle])
        self.controller_server.send_message(message, mutex=True)
        self.target_pose = None
        self.move_queue_size += 1
        if self.print_status:
            console.log(f"Moving joint {joint_idx} relative angle: {angle}", style="move_joints")
        return True

    def move_joints_to_relative(self, angles: List[float]) -> bool:
        message = Message(MessageOp.MOVE, 13, angles)
        self.controller_server.send_message(message, mutex=True)
        self.target_pose = None
        self.move_queue_size += 1
        if self.print_status:
            console.log(f"Moving joints relative angles: {angles}", style="move_joints")
        return True

    def set_tool_value(self, angle: float) -> None:
        message = Message(MessageOp.MOVE, 7, [angle])
        self.controller_server.send_message(message, mutex=True)
        self.move_queue_size += 1
        if self.print_status:
            console.log(f"Setting tool value to: {angle}", style="set_tool")

    def set_tool_value_relative(self, angle: float) -> None:
        target_angle = self.tool_value + angle
        self.set_tool_value(target_angle)

    def wait_until_angles_at_target(self, target_angles: List[float], epsilon: float = 0.01) -> None:
        while not allclose(self.current_angles, target_angles, atol=epsilon) and not self.stop_event.is_set():
            time.sleep(0.2)

    def wait_done_moving(self) -> None:
        if self.print_status:
            console.log(f"Waiting for arm to finish moving qsize: {self.move_queue_size}", style="waiting")
        while self.move_queue_size > 0 and not self.stop_event.is_set():
            time.sleep(0.2)
        if self.print_status:
            console.log(f"Arm finished moving qsize: {self.move_queue_size}", style="waiting")

    def valid_pose(self, pose: ArmPose) -> bool:
        target_angles = self.kinematics.pose_to_angles(pose, self.current_angles)
        if target_angles is None:
            return False
        return True

    """
    ----------------------------------------
                    API Methods -- STATUS
    ----------------------------------------
    """

    def stop_movement(self) -> None:
        message = Message(MessageOp.STATUS, 5)
        self.controller_server.send_message(message, mutex=True)
        if self.print_status:
            console.log("Stopping arm", style="info")

    def print_state(self) -> None:
        message = Message(MessageOp.STATUS, 7)
        self.controller_server.send_message(message, mutex=True)
        if self.print_status:
            console.log("Printing arm state", style="info")

    """
    ----------------------------------------
                    API Methods -- CONFIG
    ----------------------------------------
    """

    def set_setting_joint(self, setting_key: Settings, value: float, joint_idx: int) -> None:
        if setting_key not in self.joint_settings[joint_idx].keys():
            raise ValueError(f"Invalid setting key for joint setting: {setting_key}")
        setting = self.joint_settings[joint_idx][setting_key]
        code = setting.code_set
        message = Message(MessageOp.CONFIG, code, [float(joint_idx), value])
        self.controller_server.send_message(message, mutex=True)
        setting.last_updated = -1

        if self.print_status:
            console.log(f"Setting {setting_key}:{code} to {value} for joint {joint_idx}", style="set_settings")

    def set_setting_joints(self, setting_key: Settings, value: float) -> None:
        for joint_idx in range(self.num_joints):
            self.set_setting_joint(setting_key, value, joint_idx)

    def get_setting_joint(self, setting_key: Settings, joint_idx: int) -> float:
        if setting_key not in self.joint_settings[joint_idx].keys():
            raise ValueError(f"Invalid setting key for joint setting: {setting_key}")

        setting = self.joint_settings[joint_idx][setting_key]
        code = setting.code_get

        if setting.last_updated < 0:  # valid value
            message = Message(MessageOp.CONFIG, code, [float(joint_idx)])
            self.controller_server.send_message(message, mutex=True)
            while setting.last_updated < 0 and not self.stop_event.is_set():
                time.sleep(0.01)
        return setting.value

    def get_setting_joints(self, setting_key: Settings) -> List[float]:
        return [self.get_setting_joint(setting_key, joint_idx) for joint_idx in range(self.num_joints)]

    def set_joint_driver_stepper(self, joint_idx: int, step_pin: int, dir_pin: int) -> None:
        message = Message(MessageOp.CONFIG, 21, [float(joint_idx), float(step_pin), float(dir_pin)])
        self.controller_server.send_message(message, mutex=True)
        if self.print_status:
            console.log(f"Setting stepper driver for joint {joint_idx}", style="set_settings")

    def set_joint_driver_servo(self, joint_idx: int, pin: int) -> None:
        message = Message(MessageOp.CONFIG, 23, [float(joint_idx), float(pin)])
        self.controller_server.send_message(message, mutex=True)
        if self.print_status:
            console.log(f"Setting servo driver for joint {joint_idx}", style="set_settings")

    def set_joint_endstop_hall(self, joint_idx: int, pin: int) -> None:
        message = Message(MessageOp.CONFIG, 25, [float(joint_idx), float(pin)])
        self.controller_server.send_message(message, mutex=True)
        if self.print_status:
            console.log(f"Setting endstop hall for joint {joint_idx}", style="set_settings")

    def set_joint_endstop_dummy(self, joint_idx: int) -> None:
        message = Message(MessageOp.CONFIG, 27, [float(joint_idx)])
        self.controller_server.send_message(message, mutex=True)
        if self.print_status:
            console.log(f"Setting endstop dummy for joint {joint_idx}", style="set_settings")

    def set_joint_endstop_none(self, joint_idx: int) -> None:
        message = Message(MessageOp.CONFIG, 29, [float(joint_idx)])
        self.controller_server.send_message(message, mutex=True)
        if self.print_status:
            console.log(f"Setting endstop none for joint {joint_idx}", style="set_settings")

    def set_tool_driver_servo(self, pin: int) -> None:
        message = Message(MessageOp.CONFIG, 35, [float(pin)])
        self.controller_server.send_message(message, mutex=True)
        if self.print_status:
            console.log(f"Setting servo driver for tool on pin {pin}", style="set_settings")


class SingletonArmController:
    _instance: Optional[ArmController] = None
    arm_parameters: Optional[ArmParameters] = None
    websocket_port: int = 8600
    server_port: int = 8500
    print_status: bool = False
    config_file: Optional[Path] = None

    @classmethod
    def create_instance(
        cls,
        arm_parameters: ArmParameters,
        websocket_port: int = 8600,
        server_port: int = 8500,
        config_file: Optional[Path] = None,
        print_status: bool = False,
    ) -> None:
        cls.arm_parameters = arm_parameters
        cls.websocket_port = websocket_port
        cls.server_port = server_port
        cls.print_status = print_status
        cls.config_file = config_file

        cls._instance = ArmController(arm_parameters=arm_parameters, websocket_port=websocket_port, server_port=server_port)
        cls._instance.print_status = print_status
        if config_file is not None:
            cls._instance.set_config_file(config_file)

    @classmethod
    def get_instance(cls) -> ArmController:
        if cls._instance is not None:
            if cls._instance.status == ControllerStatus.STOPPED:
                console.log("Error in SingletonArmController instance has stopped!", style="error")
                cls._instance = None

                time.sleep(5)

                if cls.arm_parameters is not None:
                    cls.create_instance(
                        cls.arm_parameters, cls.websocket_port, cls.server_port, cls.config_file, cls.print_status
                    )
                    if cls._instance is not None:
                        console.log("Restarting SingletonArmController instance", style="error")
                        cls._instance.start()
                        console.log("SingletonArmController instance restarted", style="error")

                return cls.get_instance()
            else:
                return cls._instance
        raise ValueError("Arm Controller not initialized")

    @classmethod
    def was_initialized(cls) -> bool:
        return cls._instance is not None
