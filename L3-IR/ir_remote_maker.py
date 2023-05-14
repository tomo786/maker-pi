import time
from machine import Pin
from ir_rx.nec import NEC_8
# from utime import sleep
from collections import namedtuple

# namedtupleの定義を行う
IRtuple =namedtuple("IRKey",("PW","AS","BS","CS","UL", "Upper","UR",
                             "Left", "Center", "Right", "DL","Down","DR"))

# 実際のインスタンスを作成する
irdata = IRtuple(0xD8, 0xF8, 0x78, 0x58, 0xB1,
             0xA0, 0x21, 0x10, 0x20, 0x80,
             0x11, 0x00, 0x81)
last_code = 0xff

# 赤外線の信号を受信時に呼び出されるコールバック関数
def callback(data, addr, ctrl):
    global last_code
    if data < 0: # repeat code -> 同じキーが繰り返しが押された時の処理
        pass
        # print(data)
    else:
        # print(data)
        last_code = data
        
# 2番ピンを使用するようにして、NEC_8クラスを初期化。
# 上記のcallback関数を登録します。
# GROVES5のpin配置(1pin:GND,2pin:VCC(3.3V),3pin:Sig(GP06))
ir = NEC_8(Pin(6, Pin.IN), callback)

mL1 = Pin(11,Pin.OUT)   # Motor1(M1A):左車輪前進
mL2 = Pin(10,Pin.OUT)   # Motor1(M1B):左車輪後退
mR1 = Pin( 9,Pin.OUT)   # Motor2(M2A):右車輪後退
mR2 = Pin( 8,Pin.OUT)   # Motor2(M2B):右車輪前進

def moveForward():
    mL1.value(1)
    mL2.value(0)
    mR1.value(0)
    mR2.value(1)
    
def moveBackward():
    mL1.value(0)
    mL2.value(1)
    mR1.value(1)
    mR2.value(0)
    
def moveRight():
    mL1.value(0)
    mL2.value(0)
    mR1.value(0)
    mR2.value(1)
    
def moveLeft():
    mL1.value(1)
    mL2.value(0)
    mR1.value(0)
    mR2.value(0)
    
def stop():
    mL1.value(0)
    mL2.value(0)
    mR1.value(0)
    mR2.value(0)    
    
# 無限ループ、信号を受信するとcallback関数が呼ばれます。
while True:
    moveData = last_code
    if (moveData == irdata.Upper):
        moveForward()
    elif(moveData == irdata.Center):
        stop()
    elif(moveData == irdata.Down):
        moveBackward()
    elif(moveData == irdata.Left):
        moveLeft()
    elif(moveData == irdata.Right):
        moveRight()
    else:
        pass
    time.sleep(0.1)
