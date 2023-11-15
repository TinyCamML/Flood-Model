# TinyFloodCamML OpenMV code - By: ebgoldstein - Mon Oct 2nd 2023

import sensor
import image
import time
import pyb
import tf

from pyb import UART
from pyb import Pin, ExtInt


uart = machine.UART(1, baudrate=9600)
uart = UART(1, 9600) # UART1, adjust baudrate as needed

#rtc = pyb.RTC()


redLED   = pyb.LED(1)

sensor.reset() # Initialize the camera sensor.
sensor.set_pixformat(sensor.RGB565) # or sensor.GRAYSCALE
sensor.set_framesize(sensor.QVGA)

sensor.skip_frames(time = 2000)


#red light during setup
redLED.on()


#Load the TFlite model and the labels, takes a lot of power.
net = tf.load('MNv2Flood_cat (3).tflite', load_to_fb=True)
labels = ['Flood', 'NoFlood']

#turn led off when model is loaded
redLED.off()


def callback(line):
    pass

led = pyb.LED(3)
pin = Pin("P0", Pin.IN, Pin.PULL_UP)
ext = ExtInt(pin, ExtInt.IRQ_FALLING, Pin.PULL_UP, callback)

# Enter Stop Mode. Note the IDE will disconnect.
machine.sleep()

while(True):

    img = sensor.snapshot()

    TF_objs = net.classify(img)
    print(TF_objs)


    Flood = TF_objs[0].output()[0]
    NoFlood = TF_objs[0].output()[1]

    if Flood > NoFlood:
        print('Flood')
        uart.write('Flood')
        #uart.read('Flood)
        # Uncomment if you have an LCD
        # img.draw_string(1,140, "Flood", color = (10,10,100), scale = 2,mono_space = False)
    else:
        print('No Flood')
        uart.write('No Flood')
        #uart.read('No Flood)
        # Uncomment if you have an LCD
        # img.draw_string(1,140, "No Flood", color = (10,10,100), scale = 2,mono_space = False)

