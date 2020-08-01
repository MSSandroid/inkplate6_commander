import serial
import time
from .commands import Command


class Inkplate6():
    """
    size 800x,600y
    """

    def __init__(self, port: str):
        self.serial = serial.Serial(port, 115200)

    def cmd(self, do_display=True) -> Command:
        return Command(self.serial, do_display)

    def remove_burn_in(self):
        for _ in range(10):
            Command(self.serial).clear_display().send()
            time.sleep(.1)

    def close(self):
        self.serial.close()

    def __enter__(self) -> Command:
        return self

    def __exit__(self, type, value, traceback):
        self.close()
