from __future__ import annotations
from typing import List
from .results import *


class Command():
    """
    Generate and send commands to Inkplate6 in UART mode.

    Implements commands of https://github.com/e-radionicacom/Inkplate-6-Arduino-library/tree/master/examples/4.%20Others/1-Inkplate_Slave_Mode
    and requires the `.ino` to run on Inkplate6.

    Coordinates are as follows (x->from_left_to_right, y->from_top_to_buttom).
    """
    def __init__(self, serial, do_display=True):
        self._command = ""
        self.results = []
        self.serial = serial
        self.do_display = do_display

    def send(self) -> Command:
        if self.do_display:
            self.display()
        self.serial.write(f'{self._command}\n\r'.encode())
        return self

    def receive(self) -> List[Result]:
        self.send()
        for response in self.results:
            line = self.serial.readline()
            response.parse(line)
        return self.results

    def append(self, cmd):
        self._command = self._command + cmd

    def __enter__(self) -> Command:
        self._command = ""
        self.results = []
        return self

    def __exit__(self, type, value, traceback):
        self.receive()

    def echo(self) -> Command:
        self.append(f'#?*')
        self.results.append(EchoResult())
        return self

    def draw_pixel(self, x, y, c) -> Command:
        self.append(f'#0({str(x).zfill(3)},{str(y).zfill(3)},{str(c).zfill(2)})*')
        return self

    def draw_line(self, x, y, i, j, c) -> Command:
        self.append(f'#1({str(x).zfill(3)},{str(y).zfill(3)},{str(i).zfill(3)},{str(j).zfill(3)},{str(c).zfill(2)})*')
        return self

    def draw_fast_v_line(self, x, y, l, c) -> Command:
        self.append(f'#2({str(x).zfill(3)},{str(y).zfill(3)},{str(l).zfill(3)},{str(c).zfill(2)})*')
        return self

    def draw_fast_h_line(self, x, y, l, c) -> Command:
        self.append(f'#3({str(x).zfill(3)},{str(y).zfill(3)},{str(l).zfill(3)},{str(c).zfill(2)})*')
        return self

    def draw_rect(self, x, w, h, c) -> Command:
        self.append(f'#4({str(x).zfill(3)},{str(y).zfill(3)},{str(w).zfill(3)},{str(h).zfill(3)},{str(c).zfill(2)})*')
        return self

    def draw_circle(self, x, r, c) -> Command:
        self.append(f'#5({str(x).zfill(3)},{str(y).zfill(3)},{str(r).zfill(3)},{str(c).zfill(2)})*')
        return self

    def draw_triangle(self, x1, y1, x2, y2, x3, y3, c) -> Command:
        self.append(f'#6({str(x1).zfill(3)},{str(yt).zfill(3)},{str(x2).zfill(3)},{str(y2).zfill(3)},{str(x3).zfill(3)},{str(y3).zfill(3)},{str(c).zfill(2)})*')
        return self

    def draw_round_rect(self, x, y, w, h, r, c) -> Command:
        self.append(f'#7({str(x).zfill(3)},{str(y).zfill(3)},{str(w).zfill(3)},{str(h).zfill(3)},{str(c).zfill(2)})*')
        return self

    def fill_rect(self, x, w, h, c) -> Command:
        self.append(f'#8({str(x).zfill(3)},{str(y).zfill(3)},{str(w).zfill(3)},{str(h).zfill(3)},{str(c).zfill(2)})*')
        return self

    def fill_circle(self, x, y, r, c) -> Command:
        self.append(f'#9({str(x).zfill(3)},{str(y).zfill(3)},{str(r).zfill(3)},{str(c).zfill(2)})*')
        return self

    def fill_triangle(self, x1, y1, x2, y2, x3, y3, c) -> Command:
        self.append(f'#A({str(x1).zfill(3)},{str(yt).zfill(3)},{str(x2).zfill(3)},{str(y2).zfill(3)},{str(x3).zfill(3)},{str(y3).zfill(3)},{str(c).zfill(2)})*')
        return self

    def fill_round_rect(self, x, y, w, h, r, c) -> Command:
        self.append(f'#B({str(x).zfill(3)},{str(y).zfill(3)},{str(w).zfill(3)},{str(h).zfill(3)},{str(c).zfill(2)})*')
        return self

    def print(self, text: str) -> Command:
        self.append(f'#C("{text.encode().hex()}")*')
        return self

    def set_text_size(self, size: int) -> Command:
        self.append(f'#D({str(size).zfill(2)})*')
        return self

    def set_cursor(self, x: int, y: int):
        self.append(f'#E({str(x).zfill(3)},{str(y).zfill(3)})*')
        return self

    def set_text_wrap(self, do_wrap=True) -> Command:
        self.append(f'#F({"T" if do_wrap else "F"}*')
        return self

    def set_rotation(self, r: int) -> Command:
        """for each increment roation by 90degree"""
        assert 0 <= r <= 3
        self.append(f'#G({str(r).zfill(3)})*')
        return self

    def draw_bitmap(self, x, y, path_on_sdcard) -> Command:
        self.append(f'#H({str(x).zfill(3)},{str(y).zfill(3)},"{path_on_sdcard.encode().hex()}")*')
        self.results.append(DrawBitmapResult())
        return self

    def set_display_mode(self, bit_mode) -> Command:
        assert bit_mode == 3 or bit_mode == 1
        self.append(f'#I({bit_mode})*')
        return self

    def get_display_mode(self) -> Command:
        self.append(f'#J(?)*')
        self.results.append(GetDisplayModeResult())
        return self

    def clear_display(self) -> Command:
        self.append('#K(1)*')
        return self

    def display(self) -> Command:
        self.append('#L(1)*')
        return self

    def partial_update(self, yy1, xx2, yy2) -> Command:
        self.append(f'#M({str(yy1).zfill(3)},{str(xx2).zfill(3)},{str(yy2).zfill(3)})*')
        return self

    def read_temperature(self) -> Command:
        self.append('#N(?)*')
        self.results.append(ReadTemperatureResult())
        return self

    def read_touchpad(self, pad: int) -> Command:
        assert 0 <= pad <= 3
        self.append(f'#O({pad})*')
        self.results.append(ReadTouchpadResult(pad))
        return self

    def read_battery(self) -> Command:
        self.append('#P(?)*')
        self.results.append(ReadBatteryResult())
        return self

    def panel_supply(self, eink_on=True) -> Command:
        self.append(f'#S({1 if eink_on else 0})*')
        return self

    def get_panel_state(self) -> Command:
        self.append('#R(?)*')
        self.results.append(GetPanelStateResult())
        return self
