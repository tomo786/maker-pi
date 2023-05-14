from machine import Pin, PWM
from utime import sleep
msb = machine.PWM(machine.Pin(12))
msb.freq(50)
# dutyの設定は、0-65536の範囲
# 0°：4751

while True:
     msb.duty_u16(1638)
     sleep(1)
     msb.duty_u16(4751)
     sleep(1)
     msb.duty_u16(7864)
     sleep(1)