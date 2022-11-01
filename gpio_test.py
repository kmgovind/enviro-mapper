import RPi.GPIO as GPIO
from time import sleep
from signal import pause

# Set Pin Constants
led_pin = 11

# Setup Pins on board
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD) # using the board's numbering scheme
GPIO.setup(led_pin, GPIO.OUT)

# Main Logic

while True:
    GPIO.output(led_pin, True) 
    sleep(1) 
    GPIO.output(led_pin, False) 
    sleep(1) 