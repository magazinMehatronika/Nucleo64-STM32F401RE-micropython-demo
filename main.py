from machine import I2C, Pin, ADC
from utime import sleep_ms
from ssd1306 import SSD1306_I2C

from pyb import Pin, Timer

blue_on = False

def remap(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def handle_interrupt(pin):
    global blue_on
    if (blue_on):
        blue_on = False
    else:
        blue_on = True
    global interrupt_pin
    interrupt_pin = pin
    sleep_ms(20)

xAxis = ADC(Pin('PA1'))
yAxis = ADC(Pin('PA0'))

SW = Pin('PA9', Pin.IN, Pin.PULL_UP)
SW.irq(trigger=Pin.IRQ_FALLING, handler=handle_interrupt)

red = 0
green = 0
blue = 0

p_red = Pin('PB3') # PB3-D3 has TIM2, CH2
tim = Timer(2, freq=4000)
ch = tim.channel(2, Timer.PWM, pin=p_red)
ch.pulse_width_percent(red)

p_green = Pin('PB4') # PB4-D5 has TIM3, CH1
tim = Timer(3, freq=4000)
ch = tim.channel(1, Timer.PWM, pin=p_green)
ch.pulse_width_percent(green)

p_blue = Pin('PA8') # PB10-D6 has TIM1, CH1
tim = Timer(1, freq=4000)
ch = tim.channel(1, Timer.PWM, pin=p_blue)
ch.pulse_width_percent(blue)


i2c = I2C(1)
oled = SSD1306_I2C(128, 64, i2c)

oled.show()
oled.fill(0)
oled.show()
oled.text("RED:   {}".format(red),10,10,1)
oled.text("GREEN: {}".format(green),10,30,1)
oled.text("BLUE:  {}".format(blue),10,50,1)
oled.show()



while True:
    xRef = round (remap (xAxis.read_u16(), 0, 65555, 0, 100))
    yRef = round (remap (yAxis.read_u16(), 0, 65555, 0, 100))
    oled.fill(0)
    oled.text("RED:   {}".format(str(xRef)),10,10,1)
    oled.text("GREEN: {}".format(str(yRef)),10,30,1)
    oled.text("BLUE: {}".format(str(blue)),10,50,1)
    oled.show()
    
    p_red = Pin('PB3') # PB3-D3 has TIM2, CH2
    tim = Timer(2, freq=4000)
    ch = tim.channel(2, Timer.PWM, pin=p_red)
    ch.pulse_width_percent(xRef)
    
    p_green = Pin('PB4') # PB4-D5 has TIM3, CH1
    tim = Timer(3, freq=4000)
    ch = tim.channel(1, Timer.PWM, pin=p_green)
    ch.pulse_width_percent(yRef)
    
    p_blue = Pin('PA8') # PB10-D6 has TIM1, CH1
    tim = Timer(1, freq=4000)
    ch = tim.channel(1, Timer.PWM, pin=p_blue)
    if (blue_on):
        blue = 255
    else:
        blue = 0
    ch.pulse_width_percent(blue)
    
    sleep_ms(100)
