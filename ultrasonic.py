#Libraries
import RPi.GPIO as GPIO
import time
from constants import *





def setup_ultrasonic():
    #GPIO Mode (BOARD / BCM)
    GPIO.setmode(GPIO.BCM)
    
    #set GPIO direction (IN / OUT)
    GPIO.setup(LEFT_GPIO_TRIGGER, GPIO.OUT)
    GPIO.setup(LEFT_GPIO_ECHO, GPIO.IN)
    GPIO.setup(RIGHT_GPIO_TRIGGER, GPIO.OUT)
    GPIO.setup(RIGHT_GPIO_ECHO, GPIO.IN)
    GPIO.setup(CENTER_GPIO_TRIGGER, GPIO.OUT)
    GPIO.setup(CENTER_GPIO_ECHO, GPIO.IN)

def get_all_distance():
    right_distance  = distance(RIGHT_GPIO_TRIGGER,RIGHT_GPIO_ECHO)
    left_distance = distance(LEFT_GPIO_TRIGGER,LEFT_GPIO_ECHO)
    center_distance = distance(CENTER_GPIO_TRIGGER,CENTER_GPIO_ECHO)
    return {"center": center_distance,"right": right_distance, "left": left_distance}
 
def distance(GPIO_TRIGGER, GPIO_ECHO):
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
 
    return distance
 
if __name__ == '__main__':
    try:
        while True:
            dist = get_all_distance()
            print ("Measured Distance = " , dist)
            time.sleep(1)
 
        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()