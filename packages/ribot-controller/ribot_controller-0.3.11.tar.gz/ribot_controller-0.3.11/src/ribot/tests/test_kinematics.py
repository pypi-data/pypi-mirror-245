import unittest
from typing import List

import numpy as np

from ribot.control.arm_kinematics import ArmParameters, ArmPose
from ribot.controller import ArmController
from ribot.utils.algebra import (
    allclose,
    create_rotation_matrix_from_euler_angles,
    degree2rad,
    extract_euler_angles,
)
from ribot.utils.prints import disable_console


class TestArmKinematics(unittest.TestCase):
    EPSILON: float = 0.01
    controller: ArmController

    def helper_angle_to_pose(self, angles: List[float], expected_pose: ArmPose) -> None:
        angles = [degree2rad(angle) for angle in angles]
        current_pose = self.controller.kinematics.angles_to_pose(angles)
        curren_pose_list = current_pose.as_list
        expected_pose_list = expected_pose.as_list
        all_close = allclose(curren_pose_list, expected_pose_list, rtol=self.EPSILON)
        self.assertTrue(all_close, f"expected: {expected_pose_list} actual: {curren_pose_list}")

    def helper_pose_to_angles(self, expected_angles: List[float], pose: ArmPose) -> None:
        angles = self.controller.kinematics.pose_to_angles(pose, self.controller.current_angles)
        expected_angles = [degree2rad(angle) for angle in expected_angles]
        self.assertIsNotNone(angles)
        if angles is None:
            return
        all_close = allclose(angles, expected_angles, rtol=self.EPSILON)
        self.assertTrue(all_close, f"expected: {expected_angles} actual: {angles}")

    @classmethod
    @disable_console
    def setUpClass(cls) -> None:
        arm_params = ArmParameters()
        arm_params.a1z = 650.0
        arm_params.a2x = 400.0
        arm_params.a2z = 680.0
        arm_params.a3z = 1100.0
        arm_params.a4z = 230.0
        arm_params.a4x = 766.0
        arm_params.a5x = 345.0
        arm_params.a6x = 244.0
        cls.controller = ArmController(arm_parameters=arm_params)

    @disable_console
    def test_pose_to_angles(self) -> None:
        pose = ArmPose(1755, 0, 2660, 0, 0, 0, degree=True)
        self.helper_pose_to_angles([0, 0, 0, 0, 0, 0], pose)

        pose = ArmPose(0, 1755, 2660, 0, 0, 90, degree=True)
        self.helper_pose_to_angles([90, 0, 0, 0, 0, 0], pose)

        pose = ArmPose(1500, 1000, 2000, 0, 0, 0, degree=True)
        self.helper_pose_to_angles([38.5, 7.9, 25.5, 55.3, -49.2, -43.3], pose)

        pose = ArmPose(-500, 1000, 2000, 50, 50, 50, degree=True)
        self.helper_pose_to_angles([124.3, -24.7, 43.6, -42.8, 65.6, 140.8], pose)

        pose = ArmPose(600, -1000, 3300, 250, 0, -90, degree=True)
        self.helper_pose_to_angles([-51.6, -7.9, -31.3, -51.5, 52.6, -72.7], pose)

    @disable_console
    def test_angles_to_pose(self) -> None:
        self.helper_angle_to_pose([0, 0, 0, 0, 0, 0], ArmPose(1755, 0, 2660, 0, 0, 0, degree=True))

        self.helper_angle_to_pose([90, 0, 0, 0, 0, 0], ArmPose(0, 1755, 2660, 0, 0, 90, degree=True))

        self.helper_angle_to_pose(
            [130, -60, 30, 60, -90, 60],
            ArmPose(11.8, 314.7, 2740.3, -176.3, -25.7, 23.9, degree=True),
        )

        self.helper_angle_to_pose(
            [-46, 46, 46, 46, 46, 46],
            ArmPose(962.3, -814.8, 810.6, -132.0, 42.6, 89.3, degree=True),
        )

    @disable_console
    def test_angle_to_pose_to_angle(self) -> None:
        angles = [np.pi / 2 for _ in range(6)]
        pose = self.controller.kinematics.angles_to_pose(angles)
        angles2 = self.controller.kinematics.pose_to_angles(pose, self.controller.current_angles)

        if angles2 is None:
            self.fail("angles2 is None")
        all_close = allclose(angles, angles2, rtol=self.EPSILON)
        self.assertTrue(all_close, f"expected: {angles} actual: {angles2}")

    @disable_console
    def test_rotation_matrixs(self) -> None:
        R1 = create_rotation_matrix_from_euler_angles(90, 100, 20)

        roll, pitch, yaw = extract_euler_angles(R1)

        R2 = create_rotation_matrix_from_euler_angles(roll, pitch, yaw)

        all_close = np.allclose(R1, R2, rtol=self.EPSILON)
        self.assertTrue(all_close, f"expected: {R1} actual: {R2}")

    def test_stress(self) -> None:
        possible_angles = []
        for joint in self.controller.arm_params.joints:
            possible_angles.append(np.arange(joint.min_val, joint.max_val, 0.05))

        num_combinations = 1000
        for _ in range(num_combinations):
            # Generate a random combination of angles.
            pos_angles = list(np.random.choice(angles) for angles in possible_angles)
            pose = self.controller.kinematics.angles_to_pose(pos_angles)
            angles = self.controller.kinematics.pose_to_angles(pose, self.controller.current_angles)
            # calculate the pose from the angles and compare to the original pose
            self.assertIsNotNone(angles)
            if angles is not None:
                pose2 = self.controller.kinematics.angles_to_pose(angles)
                all_close = allclose(pose.as_list, pose2.as_list, rtol=self.EPSILON)
                self.assertTrue(all_close, f"expected: {pose.as_list} actual: {pose2.as_list}")
