#  Copyright (c) Kuba Szczodrzyński 2023-5-22.

from enum import IntEnum
from logging import debug
from typing import Callable

from ltchiptool.gui.work.base import BaseThread
from serial import Serial


class EscState(IntEnum):
    NONE = 0
    ESCAPE = 1
    CSI_PARAM = 3
    CSI_INTER = 4


class TerminalThread(BaseThread):
    control: list[int] = None
    state: EscState = EscState.NONE

    def __init__(
        self,
        s: Serial,
        on_serial_data: Callable[[bytes], None],
        on_control_data: Callable[[bytes], None],
    ):
        super().__init__()
        self.s = s
        self.on_serial_data = on_serial_data
        self.on_control_data = on_control_data
        self.reset_control()

    def run_impl(self) -> None:
        debug("Terminal opened")
        self.s.timeout = 1.0
        while self.should_run() and self.s.is_open:
            data = self.s.read(max(1, self.s.in_waiting))
            if not data:
                continue

            if b"\x1B" not in data and self.control is None:
                # no escape char, and not during a command
                self.on_serial_data(data)
                continue

            text = b""
            for i, c in enumerate(data):
                if c == 0x1B:
                    # new command
                    self.reset_control()
                    self.parse_control(c)
                    self.control.append(c)
                    continue
                if self.state != EscState.NONE:
                    # continuation
                    parse = self.parse_control(c)
                    self.control.append(c)
                    if parse is None:
                        continue
                    # either a command or invalid data
                    if parse is False:
                        # invalid data, treat as text
                        text += bytes(self.control)
                    else:
                        # found valid control command
                        if text:
                            # send queued text before sending control data
                            self.on_serial_data(text)
                            text = b""
                        self.on_control_data(bytes(self.control))
                    self.reset_control()
                else:
                    # not a command, append the text
                    text += bytes([c])
            if text:
                # send remaining text
                self.on_serial_data(text)

        debug("Terminal closed")

    def reset_control(self) -> None:
        self.control = []
        self.state = EscState.NONE

    def parse_control(self, c: int) -> bool | None:
        # print(f"parse_control(state={self.state.name}, c={hex(c)})")
        match self.state:
            case EscState.NONE:
                if c == 0x1B:
                    self.state = EscState.ESCAPE
                    return None
            case EscState.ESCAPE:
                if c == 0x5B:  # CSI
                    self.state = EscState.CSI_PARAM
                    return None
            case EscState.CSI_PARAM:
                if c in range(0x30, 0x40):  # parameter bytes
                    return None
                if c in range(0x20, 0x30):  # intermediate bytes
                    self.state = EscState.CSI_INTER
                    return None
                if c in range(0x40, 0x80):  # final byte
                    return True
            case EscState.CSI_INTER:
                if c in range(0x20, 0x30):  # intermediate bytes
                    return None
                if c in range(0x40, 0x80):  # final byte
                    return True
        return False

    def stop(self) -> None:
        super().stop()
        self.s.close()
