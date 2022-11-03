import RPi.GPIO as GPIO
from time import sleep
from signal import pause

import constants as k

# Setup Pins on board
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD) # using the board's numbering scheme
GPIO.setup(k.led_pin, GPIO.OUT)

# Main Logic

while True:
    GPIO.output(k.led_pin, True) 
    sleep(1) 
    GPIO.output(k.led_pin, False) 
    sleep(1) 