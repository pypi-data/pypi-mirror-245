from __future__ import annotations

import dataclasses
import struct
from enum import Enum

__author__ = "Alberto Abarzua"


class MessageOp(Enum):
    MOVE = "M"
    STATUS = "S"
    CONFIG = "C"


@dataclasses.dataclass
class Message:
    op: MessageOp
    code: int
    num_args: int
    args: list[float]

    LENGTH_HEADERS = 1 + 4 * 2  # op + code + num_args

    def __init__(self, op: MessageOp, code: int, args: list[float] = []) -> None:
        self.op = op
        self.code = code
        self.num_args = len(args)
        self.args = args

    def __post_init__(self) -> None:
        error_msg_num_args = f"Number of arguments ({self.num_args}) does not match"
        error_msg_num_args += f" the length of the args list ({len(self.args)})"
        assert len(self.args) == self.num_args, error_msg_num_args
        assert isinstance(self.op, MessageOp), f"op must be a MessageOp, not {type(self.op)}"
        assert isinstance(self.code, int), f"code must be an int, not {type(self.code)}"
        assert isinstance(self.num_args, int), f"num_args must be an int, not {type(self.num_args)}"
        assert isinstance(self.args, list), f"args must be a list, not {type(self.args)}"
        for arg in self.args:
            assert isinstance(arg, float), f"args must be a list of floats, not {type(arg)}"

    def encode(self) -> bytes:
        return struct.pack(
            "<cii" + "f" * len(self.args),
            self.op.value.encode(),
            self.code,
            self.num_args,
            *self.args,
        )

    @staticmethod
    def decode_headers(bytes: bytes) -> tuple[MessageOp, int, int]:
        op, code, num_args = struct.unpack_from("<cii", bytes, offset=0)
        op = op.decode()
        return MessageOp(op), code, num_args

    @staticmethod
    def decode(bytes: bytes) -> Message:
        op, code, num_args = struct.unpack_from("<cii", bytes, offset=0)
        args = struct.unpack_from("<" + "f" * num_args, bytes, offset=9)
        op = op.decode()
        return Message(MessageOp(op), code, args)  # type: ignore

    def __str__(self) -> str:
        first_args = self.args[: self.num_args // 2]
        second_args = self.args[self.num_args // 2 :]
        first_args_str = ", ".join([f"{arg:.3f}" for arg in first_args])
        second_args_str = ", ".join([f"{arg:.3f}" for arg in second_args])
        args_str = f"\n{first_args_str}\n{second_args_str}"
        return f"op: {self.op}, code: {self.code}, num_args: {self.num_args}, args: {args_str}"
