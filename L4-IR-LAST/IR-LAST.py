# 2022/11/26 IR Remote
import time
from machine import Pin, PWM
from ir_rx.nec import NEC_8
from collections import namedtuple

# namedtupleの定義を行う
IRtuple =namedtuple("IRKey",("PW","AS","BS","CS","FL","FW","FR",
                             "CCW", "Center", "CW", "BL","BW","BR"))
Speedtuple = namedtuple("SpeedKey",("Max","Fast","Middle","Low"))

# 実際のインスタンスを作成する
irdata = IRtuple(0xD8, 0xF8, 0x78, 0x58, 0xB1,
             0xA0, 0x21, 0x10, 0x20, 0x80,
             0x11, 0x00, 0x81)
# PWMのスピードを設定する。0-65536
speedDuty = Speedtuple(65536, 40000, 30000, 20000)

# 速度は最初低速にしておく
speedData = speedDuty.Low
print(speedData)

last_code = 0xff
speed_code = 0xff
move_code = 0xff

# 赤外線の信号を受信時に呼び出されるコールバック関数
def callback(data, addr, ctrl):
    global last_code
    if data < 0: # repeat code -> 同じキーが繰り返しが押された時の処理
        pass
    else:
        last_code = data
        
# 2番ピンを使用するようにして、NEC_8クラスを初期化。
# 上記のcallback関数を登録します。
ir = NEC_8(Pin(6, Pin.IN), callback)

mL1 = PWM(Pin(8,Pin.OUT))   # Motor1(M1A):左車輪前進
mL2 = PWM(Pin(9,Pin.OUT))   # Motor1(M1B):左車輪後退
mR1 = PWM(Pin(11,Pin.OUT))   # Motor2(M2A):右車輪後退
mR2 = PWM(Pin(10,Pin.OUT))   # Motor2(M2B):右車輪前進
mL1.freq(1000)
mL2.freq(1000)
mR1.freq(1000)
mR2.freq(1000)

def moveForward(speed):
    mL1.duty_u16(speed)
    mL2.duty_u16(0)
    mR1.duty_u16(speed)
    mR2.duty_u16(0)
    
def moveBackward(speed):
    mL1.duty_u16(0)
    mL2.duty_u16(speed)
    mR1.duty_u16(0)
    mR2.duty_u16(speed)

def moveRight(speed):
    mL1.duty_u16(speed)
    mL2.duty_u16(0)
    mR1.duty_u16(0)
    mR2.duty_u16(0)
    
def moveLeft(speed):
    mL1.duty_u16(0)
    mL2.duty_u16(0)
    mR1.duty_u16(speed)
    mR2.duty_u16(0)
    
def moveCW(speed):
    mL1.duty_u16(speed)
    mL2.duty_u16(0)
    mR1.duty_u16(0)
    mR2.duty_u16(speed)
    
def moveCCW(speed):
    mL1.duty_u16(0)
    mL2.duty_u16(speed)
    mR1.duty_u16(speed)
    mR2.duty_u16(0)

def moveBackRight(speed):
    mL1.duty_u16(0)
    mL2.duty_u16(speed)
    mR1.duty_u16(0)
    mR2.duty_u16(0)
    
def moveBackLeft(speed):
    mL1.duty_u16(0)
    mL2.duty_u16(0)
    mR1.duty_u16(0)
    mR2.duty_u16(speed)
    
def stop(speed):
    mL1.duty_u16(0)
    mL2.duty_u16(0)
    mR1.duty_u16(0)
    mR2.duty_u16(0)
    
# 無限ループ、信号を受信するとcallback関数が呼ばれます。
while True:
    if (last_code == irdata.FW or
        last_code == irdata.BW or
        last_code == irdata.Center or
        last_code == irdata.FR or
        last_code == irdata.FL or
        last_code == irdata.CW or
        last_code == irdata.CCW or
        last_code == irdata.BR or
        last_code == irdata.BL):
        move_code = last_code
        
    if (last_code == irdata.PW or
        last_code == irdata.AS or
        last_code == irdata.BS or
        last_code == irdata.CS):
        speed_code = last_code
    
    # 速度の設定を行う
    if speed_code == irdata.PW:
        speedData = speedDuty.Max
    elif speed_code == irdata.AS:
       speedData = speedDuty.Fast
    elif speed_code == irdata.BS:
        speedData = speedDuty.Middle
    elif speed_code == irdata.CS:
        speedData =speedDuty.Low
    
    # 進行方向の設定を行う
    if move_code == irdata.FW:
        moveForward(speedData)
    elif move_code == irdata.Center:
        stop(speedData)
    elif move_code == irdata.BW:
        moveBackward(speedData)
    elif move_code == irdata.FL:
        moveLeft(speedData)
    elif move_code == irdata.FR:
        moveRight(speedData)
    elif move_code == irdata.CW:
        moveCW(speedData)
    elif move_code == irdata.CCW:
        moveCCW(speedData)
    elif move_code == irdata.BR:
        moveBackRight(speedData)
    elif move_code == irdata.BL:
        moveBackLeft(speedData)    
    time.sleep(0.1)