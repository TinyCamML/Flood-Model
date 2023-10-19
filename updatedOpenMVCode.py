# TinyFloodCamML OpenMV code - By: ebgoldstein - Mon Oct 2nd 2023

import sensor
import image
import time
import pyb
import tf

uart = machine.UART(3, baudrate=9600)  # UART3, adjust baudrate as needed
uart.init() #This initializes the uart pathway80

# Uncomment if you have an LCD
#import LCD


#setup LEDs and set into known off state
redLED   = pyb.LED(1)

sensor.reset() # Initialize the camera sensor.
sensor.set_pixformat(sensor.RGB565) # or sensor.GRAYSCALE
sensor.set_framesize(sensor.QVGA)
# Uncomment if you have an LCD
#sensor.set_framesize(sensor.QQVGA2) # Special 128x160 framesize for LCD Shield.
sensor.skip_frames(time = 2000)
# Uncomment if you have an LCD
#lcd.init() # Initialize the lcd screen.

#red light during setup
redLED.on()



#Load the TFlite model and the labels
net = tf.load('/MNv2Flood_cat.tflite', load_to_fb=True)
labels = ['Flood', 'NoFlood']

#turn led off when model is loaded
redLED.off()


#MAIN LOOP

while(True):

    img = sensor.snapshot()

    #Do the classification and get the object returned by the inference.
    TF_objs = net.classify(img)
    print(TF_objs)

    #The object has a output, which is a list of classifcation scores
    #for each of the output channels. this model only has 2 (flood, no flood).
    Flood = TF_objs[0].output()[0]
    NoFlood = TF_objs[0].output()[1]


    #This loop just prints to the serial terminal (and optionally the LCD screen),
    # but you could also blink an LED, write a number (or datetime), etc.

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
