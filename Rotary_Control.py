from machine import Pin
import utime

import utime
#import ds1302
from machine import I2C, Pin
from lcd_api import LcdApi
from pico_i2c_lcd import I2cLcd


DT_Pin = Pin(7, Pin.IN, Pin.PULL_UP)
CLK_Pin = Pin(6, Pin.IN, Pin.PULL_UP)
SW = Pin(8, Pin.IN, Pin.PULL_UP)

ledg=Pin(18, Pin.OUT)
ledy=Pin(17, Pin.OUT)
ledr=Pin(16, Pin.OUT)
value = 0
previousValue = 1


def rotary_changed():
    
    global previousValue
    global value
    
    if previousValue != CLK_Pin.value():
        if CLK_Pin.value() == 0:
            if DT_Pin.value() == 0:
          
                value +=1
                print( value)
            else:
        
                
                value -=1
                print(value)                
        previousValue = CLK_Pin.value()
         
         
    if SW.value() == 0:
        value=0
        print("Button pressed", value)

        
        utime.sleep(0.2)


def led_control():
    global previousValue
    global value
    
    while True:
        rotary_changed()
        utime.sleep(0.001)
        while value<0:
            ledr.value(1)
            rotary_changed()
            if value >=0:            
                ledr.value(0)
                break
        while value==0:
            ledy.value(1)
            rotary_changed()
            if value!=0:            
                ledy.value(0)
                break
        while value>0:
            ledg.value(1)
            rotary_changed()
            if value <=0:            
                ledg.value(0)
                break
try:
    led_control()
finally:
    ledr.value(0)
    ledg.value(0)
    ledy.value(0)