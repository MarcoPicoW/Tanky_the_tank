import utime
from machine import I2C, Pin


#Define which Pin is conected 
DT_Pin = Pin(7, Pin.IN, Pin.PULL_UP)
CLK_Pin = Pin(6, Pin.IN, Pin.PULL_UP)
SW = Pin(8, Pin.IN, Pin.PULL_UP)

ledg=Pin(18, Pin.OUT) #the green led
ledy=Pin(17, Pin.OUT) #the yellow led
ledr=Pin(16, Pin.OUT) #the red led
value = 0
previousValue = 1
# This will be the speed control for my tanky. Every click clockwise is +1 speed, else is -1. the click set the speed to 0. 

#The rotary encoder works with high/low signal, if the CLK if low first it means the rotary is rotating clockwise.

def rotary_changed():
    
    global previousValue
    global value  #Value=Speed.
    
    if previousValue != CLK_Pin.value():
        if CLK_Pin.value() == 0:     # CLK first+
            if DT_Pin.value() == 0:  #DT second = value + 1
                value +=1
                print( value)
            else:                    # if not, that means DT already was 0, so it's rotating anti-clokwise
                value -=1
                print(value)                
        previousValue = CLK_Pin.value()
         
         
    if SW.value() == 0:             # if you click the rotary it's set the value back to 0
        value=0
        print("Button pressed", value)
        utime.sleep(0.2)            # the clicker needed some rest


def led_control():                  # this will control the leds, green= forward, yellow=standing and red=backwards
    global value
    
    while True:
        rotary_changed()           #check if the rotary is rotating
        utime.sleep(0.001)
        while value<0:             #if the value is under 1, turn on the red led
            ledr.value(1)
            rotary_changed()           #check if the rotary is rotating
            if value >=0:            #if the value is back to 0, turn off the red led and exit the loop
                ledr.value(0)
                break
        while value==0:             # the same as above just yellow
            ledy.value(1)
            rotary_changed()
            if value!=0:            
                ledy.value(0)
                break
        while value>0:             # the same in greeen
            ledg.value(1)
            rotary_changed()
            if value <=0:            
                ledg.value(0)
                break
try:                              # the "program"
    led_control()
finally:                          #turn off all the leds when blocked
    ledr.value(0)
    ledg.value(0)
    ledy.value(0)
