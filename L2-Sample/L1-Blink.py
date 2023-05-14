# while loop 
from machine import Pin
from utime import sleep

ledPin = Pin(0, Pin.OUT)
while True:
    ledPin.value(1)
    sleep(0.2)
    ledPin.value(0)
    sleep(0.4)