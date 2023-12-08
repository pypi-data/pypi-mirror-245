#  Copyright (c) Kuba Szczodrzyński 2023-5-22.

from logging import exception
from typing import Callable

import wx.xrc
from ltchiptool.gui.colors import ColorPalette
from ltchiptool.gui.mixin.devices import DevicesBase
from ltchiptool.gui.panels.base import BasePanel
from ltchiptool.gui.panels.flash import FlashPanel
from ltchiptool.gui.utils import on_event, with_event
from ltchiptool.gui.work.base import BaseThread
from ltchiptool.gui.work.flash import FlashThread
from ltchiptool.util.logging import verbose
from serial import Serial

from ltctplugin.terminal.work import TerminalThread


class SerialMixin(Serial):
    def open_real_terminal(self):
        ...

    def close_real_terminal(self):
        ...


class SerialHook:
    def on_serial_receive(self, data: bytes) -> bytes | None:
        pass

    def on_serial_open(self, port: str) -> None:
        pass

    def on_serial_close(self, port: str) -> None:
        pass


class TerminalPanel(BasePanel, DevicesBase):
    Flash: FlashPanel = None
    FlashWorkStopped: Callable[[BaseThread], None] = None
    delayed_port: str | None = None
    ports: list[tuple[str, bool, str]]
    ports_busy: set[str]
    serial: SerialMixin = None
    hooks: list[SerialHook] = None
    newlines = {
        (False, False): b"",
        (False, True): b"\n",
        (True, False): b"\r",
        (True, True): b"\r\n",
    }
    newline: bytes = b""
    bg = 0
    fg = 15

    def __init__(self, parent: wx.Window, frame):
        super().__init__(parent, frame)
        self.LoadXRCFile("terminal.xrc")
        self.LoadXRC("TerminalPanel")
        self.AddToNotebook("Terminal")

        self.ports = []
        self.ports_busy = set()

        self.Port = self.BindComboBox("combo_port")
        self.Rescan = self.BindButton("button_rescan", self.CallDeviceWatcher)
        self.Baudrate = self.BindComboBox("combo_baudrate")
        self.Clear = self.BindButton("button_clear", self.OnClearClick)
        self.Open: wx.ToggleButton = self.BindWindow(
            "button_open",
            (wx.EVT_TOGGLEBUTTON, self.OnOpenClick),
        )
        self.BoxCR = self.BindCheckBox("checkbox_cr")
        self.BoxLF = self.BindCheckBox("checkbox_lf")
        self.BoxWrap = self.BindCheckBox("checkbox_wrap")
        self.BoxScroll = self.BindCheckBox("checkbox_scroll")
        self.BoxAuto = self.BindCheckBox("checkbox_auto")
        self.BoxEcho = self.BindCheckBox("checkbox_echo")
        self.BoxClear = self.BindCheckBox("checkbox_clear")
        self.Text: wx.TextCtrl = self.FindWindowByName("text_console", self)
        self.Text.SetDefaultStyle(wx.TextAttr(wx.WHITE))
        self.Text.Bind(wx.EVT_CHAR, self.OnKeyEvent)

        # noinspection PyTypeChecker
        self.serial = Serial()
        self.hooks = []
        ColorPalette.get().apply(self.Text)
        self.Text.SetDefaultStyle(wx.TextAttr(ColorPalette.get()[self.fg]))

    def GetSettings(self) -> dict:
        return dict(
            port=self.port,
            baudrate=self.baudrate,
            cr=self.cr,
            lf=self.lf,
            wrap=self.wrap,
            scroll=self.scroll,
            auto=self.auto,
            echo=self.echo,
            clear=self.clear,
        )

    def SetSettings(
        self,
        port: str = None,
        baudrate: int = None,
        cr: bool = None,
        lf: bool = None,
        wrap: bool = None,
        scroll: bool = None,
        auto: bool = None,
        echo: bool = None,
        clear: bool = None,
        **_,
    ) -> None:
        self.port = port
        if baudrate:
            self.baudrate = baudrate
        if cr is not None:
            self.cr = cr
        if lf is not None:
            self.lf = lf
        if wrap is not None:
            self.wrap = wrap
        if scroll is not None:
            self.scroll = scroll
        if auto is not None:
            self.auto = auto
        if echo is not None:
            self.echo = echo
        if clear is not None:
            self.clear = clear

    def OnActivate(self):
        self.StartDeviceWatcher()

    def OnDeactivate(self):
        self.StopDeviceWatcher()

    def OnShow(self) -> None:
        self.Flash = self.Frame.Panels["flash"]
        # hook and replace OnWorkStopped
        self.FlashWorkStopped = self.Flash.OnWorkStopped
        self.Flash.OnWorkStopped = self.OnWorkStopped
        # copy and replace real methods
        Serial.open_real_terminal = Serial.open
        Serial.close_real_terminal = Serial.close
        Serial.open = lambda s: self.OnSerialOpen(s)
        Serial.close = lambda s: self.OnSerialClose(s)

    def OnClose(self):
        self.PortClose()
        super().OnClose()

    def OnUpdate(self, target: wx.Window = None):
        verbose(f"OnUpdate(busy={self.ports_busy})")
        match target:
            case self.Baudrate:
                if self.serial.is_open:
                    self.serial.baudrate = self.baudrate
            case self.BoxCR | self.BoxLF:
                self.newline = self.newlines[self.cr, self.lf]
            case self.BoxWrap:
                # TODO this doesn't work
                style = self.Text.GetWindowStyle()
                if self.BoxWrap.IsChecked():
                    self.Text.SetWindowStyle(style & ~wx.TE_DONTWRAP | wx.TE_CHARWRAP)
                else:
                    self.Text.SetWindowStyle(style & ~wx.TE_CHARWRAP | wx.TE_DONTWRAP)

        # enable the Open/Close button if the port is free
        self.Open.Enable(
            self.serial.is_open
            or self.real_port
            and self.real_port not in self.ports_busy
            or False
        )
        # press it if the terminal is active
        self.Open.SetValue(self.serial.is_open)
        self.Port.Enable(not self.serial.is_open)

    def OnSerialOpen(self, s: SerialMixin) -> None:
        if s.port and s.port.lower() == self.real_port.lower():
            # free the port for others
            self.PortClose()
        s.open_real_terminal()
        if s.port.lower() not in self.ports_busy:
            self.ports_busy.add(s.port.lower())
            self.DoUpdate()

    def OnSerialClose(self, s: SerialMixin) -> None:
        s.close_real_terminal()
        if s.port.lower() in self.ports_busy:
            self.ports_busy.remove(s.port.lower())
            self.DoUpdate()

    def OnWorkStopped(self, t: BaseThread) -> None:
        verbose(f"OnWorkStopped({type(t)})")
        if isinstance(t, FlashThread) and self.FlashWorkStopped:
            self.FlashWorkStopped(t)
        if isinstance(t, FlashThread) and self.auto:
            # flashing ended - open the port automatically
            # also switch and open non-flashing ports
            self.PortOpen()
            if self.serial.is_open:
                # switch to terminal tab
                self.Frame.NotebookPagePanel = self
        if isinstance(t, TerminalThread):
            self.PortClose()

    @on_event
    def OnOpenClick(self) -> None:
        if self.Open.GetValue():
            self.PortOpen()
        else:
            self.PortClose()

    @on_event
    def OnClearClick(self) -> None:
        self.Text.Clear()

    def PortOpen(self) -> None:
        real_port = self.real_port.lower()
        if self.serial.port and real_port != self.serial.port.lower():
            # close the port if it changed
            self.serial.close_real_terminal()
        if self.serial.is_open or real_port in self.ports_busy:
            # don't open twice, ignore busy ports
            return
        try:
            self.serial.port = self.real_port
            self.serial.baudrate = self.baudrate
            self.serial.open_real_terminal()
            for hook in self.hooks:
                hook.on_serial_open(self.serial.port)
            self.DoUpdate()
            self.StartWork(
                TerminalThread(
                    s=self.serial,
                    on_serial_data=self.OnSerialData,
                    on_control_data=self.OnControlData,
                ),
                freeze_ui=False,
            )
            if self.clear:
                self.Text.Clear()
        except Exception as e:
            exception(f"Couldn't open {self.port}", exc_info=e)
            self.PortClose()

    def PortClose(self) -> None:
        self.StopWork(TerminalThread)
        self.serial.close_real_terminal()
        for hook in self.hooks:
            hook.on_serial_close(self.serial.port)
        self.DoUpdate()

    def PortWrite(self, data: bytes) -> None:
        if not self.serial.is_open:
            return
        self.serial.write(data)

    def PortIsOpen(self) -> bool:
        return self.serial.is_open

    def PortAddHook(self, hook: SerialHook) -> None:
        if hook not in self.hooks:
            self.hooks.append(hook)

    def PortRemoveHook(self, hook: SerialHook) -> None:
        if hook in self.hooks:
            self.hooks.remove(hook)

    def OnPortsUpdated(self, ports: list[tuple[str, bool, str]]) -> None:
        user_port = self.port or self.delayed_port
        items = [port[2] for port in ports]
        items.insert(0, "Same as for flashing")
        self.Port.Set(items)
        self.ports = ports
        self.port = user_port
        self.delayed_port = None
        self.DoUpdate()

    def OnPaletteChanged(self, old: ColorPalette, new: ColorPalette):
        new.apply(self.Text, old)

    @with_event
    def OnKeyEvent(self, event: wx.KeyEvent):
        if not self.serial.is_open:
            return
        key = event.GetUnicodeKey()
        verbose(f"Key event: {key} - {chr(key)}")
        if key == 13:
            text = self.newline
            if self.echo:
                self.Text.AppendText("\n")
        elif key < 32:
            return
        else:
            text = chr(key)
            if self.echo:
                self.Text.AppendText(text)
            text = text.encode("utf-8", "ignore")
        self.serial.write(text)

    def OnSerialData(self, data: bytes) -> None:
        for hook in self.hooks:
            data_new = hook.on_serial_receive(data)
            if data_new is not None:
                data = data_new
        if not data:
            return
        data = data.replace(b"\r\n", b"\n")
        data = data.replace(b"\r", b"")
        text = data.decode("utf-8", errors="replace")
        self.Text.AppendText(text)

    def OnControlData(self, data: bytes) -> None:
        if not (data.startswith(b"\x1B[") and data.endswith(b"m")):
            return
        data = data[2:-1]
        try:
            data = [int(code) for code in data.decode().split(";")]
        except ValueError:
            return
        if not data:
            data = [0]
        bright = 0
        for code in data:
            match code:
                case 0:
                    self.bg = 0
                    self.fg = 15
                    bright = 0
                case 1:
                    bright = 8
                case 2:
                    bright = 0
                case _ if code in range(30, 38):
                    self.fg = bright + code - 30
                case _ if code in range(40, 48):
                    self.bg = bright + code - 40
                case _ if code in range(90, 98):
                    self.fg = 8 + code - 90
                case _ if code in range(100, 108):
                    self.bg = 8 + code - 100
        self.Text.SetDefaultStyle(
            wx.TextAttr(
                ColorPalette.get()[self.fg],
                ColorPalette.get()[self.bg] if self.bg else wx.NullColour,
            )
        )

    @property
    def port(self) -> str | None:
        if self.Port.GetSelection() in [wx.NOT_FOUND, 0]:
            return None
        return self.ports[self.Port.GetSelection() - 1][0]

    @port.setter
    def port(self, value: str | None) -> None:
        if value is None:
            self.Port.SetSelection(0)
        else:
            for port, _, description in self.ports:
                if value == port:
                    self.Port.SetValue(description)
                    self.DoUpdate(self.Port)
                    return
            # not found, revert to first option
            # self.port = None
            self.DoUpdate(self.Port)
            self.delayed_port = value

    @property
    def real_port(self) -> str | None:
        return self.port or (self.Flash and self.Flash.port)

    @property
    def baudrate(self) -> int:
        try:
            return int(self.Baudrate.GetValue())
        except ValueError:
            return 115200

    @baudrate.setter
    def baudrate(self, value: int) -> None:
        self.Baudrate.SetValue(str(value))

    @property
    def cr(self) -> bool:
        return self.BoxCR.IsChecked()

    @cr.setter
    def cr(self, value: bool) -> None:
        self.BoxCR.SetValue(value)
        self.newline = self.newlines[value, self.lf]

    @property
    def lf(self) -> bool:
        return self.BoxLF.IsChecked()

    @lf.setter
    def lf(self, value: bool) -> None:
        self.BoxLF.SetValue(value)
        self.newline = self.newlines[self.cr, value]

    @property
    def wrap(self) -> bool:
        return self.BoxWrap.IsChecked()

    @wrap.setter
    def wrap(self, value: bool) -> None:
        self.BoxWrap.SetValue(value)

    @property
    def scroll(self) -> bool:
        return self.BoxScroll.IsChecked()

    @scroll.setter
    def scroll(self, value: bool) -> None:
        self.BoxScroll.SetValue(value)

    @property
    def auto(self) -> bool:
        return self.BoxAuto.IsChecked()

    @auto.setter
    def auto(self, value: bool) -> None:
        self.BoxAuto.SetValue(value)

    @property
    def echo(self) -> bool:
        return self.BoxEcho.IsChecked()

    @echo.setter
    def echo(self, value: bool) -> None:
        self.BoxEcho.SetValue(value)

    @property
    def clear(self) -> bool:
        return self.BoxClear.IsChecked()

    @clear.setter
    def clear(self, value: bool) -> None:
        self.BoxClear.SetValue(value)
