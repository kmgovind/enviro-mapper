import RPi.GPIO as GPIO
from time import sleep
from signal import pause
import constants as k

# Setup Pins
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD) # using the board's numbering scheme
GPIO.setup(k.RMotorFW, GPIO.OUT)

# Main Logic
while True:
	# Toggle RMotorFW On/Off
	GPIO.output(k.RMotorFW, True)
	sleep(1)
	GPIO.output(k.RMotorFW, False)
	sleep(1)

def drive_forward(inches):
	pass
def turn_to(degrees):
	pass
