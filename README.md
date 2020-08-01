# Inkplate6 Uart Commander

Send UART commands to your [Inkplate6](https://www.crowdsupply.com/e-radionica/inkplate-6) in UART mode.

## Setup

You need to have the Inkplate6 flashed with the example UART mode `.ino` which can be found in the [Inkplate6 Exampls Repository](https://github.com/e-radionicacom/Inkplate-6-Arduino-library/tree/master/examples/4.%20Others/1-Inkplate_Slave_Mode
).

## Example Usage

```python
from inkplate6_commander import Inkplate6

ink = Inkplate6('COM4')

with ink.cmd() as cmd:
    cmd.set_cursor(0,0)
    cmd.print("Hello World")
with ink.cmd(False) as cmd:
    cmd.read_battery()
    cmd.read_temperature()
    cmd.read_touchpad(1)
print(cmd.results)
```
prints:
```python
[ReadBatteryResult - 3.74, ReadTemperatureResult - 28, ReadTouchpadResult(pad=1) - True]
```
Dont forget to close the serial port with:
```python
ink.close()
```

## Details

Coordinates are as follows: `(x->from_left_to_right, y->from_top_to_buttom)`.