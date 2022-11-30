#!/usr/bin/env python3
from signal import pause
from time import sleep

import constants as k
import numpy as np
import RPi.GPIO as GPIO

posR = 0
posL = 0
lastencodedR = 0
lastencodedL = 0
rrv = 0
rfw = 0
lrv = 0
lfw = 0


def setup_dt():
    global rrv, rfw, lrv, lfw

# Setup Pins
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)  # using the board's numbering scheme

    # Pins
    GPIO.setup(k.R_MOTOR_ACTV, GPIO.OUT)
    GPIO.setup(k.R_MOTOR_FW, GPIO.OUT)
    GPIO.setup(k.R_MOTOR_RV, GPIO.OUT)
    GPIO.setup(k.R_MOTOR_ENC, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(k.R_MOTOR_VAL, GPIO.IN)
    GPIO.setup(k.L_MOTOR_ACTV, GPIO.OUT)
    GPIO.setup(k.L_MOTOR_FW, GPIO.OUT)
    GPIO.setup(k.L_MOTOR_RV, GPIO.OUT)
    GPIO.setup(k.L_MOTOR_ENC, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(k.L_MOTOR_VAL, GPIO.IN)

    # Enable PWM
    rrv = GPIO.PWM(k.R_MOTOR_RV, k.PWM_FREQ)
    rfw = GPIO.PWM(k.R_MOTOR_FW, k.PWM_FREQ)
    lrv = GPIO.PWM(k.L_MOTOR_RV, k.PWM_FREQ)
    lfw = GPIO.PWM(k.L_MOTOR_FW, k.PWM_FREQ)

    # Encoder Interrupts
    GPIO.add_event_detect(k.R_MOTOR_ENC, GPIO.RISING, callback=updateR)
    GPIO.add_event_detect(k.L_MOTOR_ENC, GPIO.RISING, callback=updateL)


def drive_forward(cm):
    global posR, posL
    posR = 0
    posL = 0
    # 0.225 * 2.54 is cm per step of encoder
    distcomp = np.floor(cm/(0.225 * 2.54))
    
    # Activate Motors
    GPIO.output(k.R_MOTOR_ACTV, True)
    GPIO.output(k.L_MOTOR_ACTV, True)
    
    while ((posR < distcomp) or (posL < distcomp)):

        # Compute necessary powers
        moveratioR = ((distcomp - posR)/distcomp) * 100
        moveratioL = ((distcomp - posL)/distcomp) * k.LR_BIAS_forward * 100
        # spdR = np.interp(moveratioR, [0, 105], [70, 200])
        # spdL = np.interp(moveratioL, [0, 105], [70, 200])
        # np.clip(spdR, 50, 200, out=spdR)
        # np.clip(spdL, 50, 200, out=spdL)

        # Turn off reverse
        GPIO.output(k.R_MOTOR_RV, False)
        GPIO.output(k.L_MOTOR_RV, False)

        # Drive forward pins
        if (moveratioL > 100):
            moveratioL = 100
        if (moveratioL < 10):
            moveratioL = 10
        if (moveratioR > 100):
            moveratioR = 100
        if (moveratioR < 10):
            moveratioR = 10
        rfw.start(moveratioR)
        lfw.start(moveratioL)
        
    rfw.stop()
    lfw.stop()

    # Deactivate Motors
    GPIO.output(k.R_MOTOR_ACTV, False)
    GPIO.output(k.L_MOTOR_ACTV, False)

def turn_to_readings(degrees,wall_tracker):
    degrees_to_measure = list(range(0,degrees,k.TURN_GRADIENT))
    degrees_to_measure.append(degrees)
    lastDegree = 0
    for i in degrees_to_measure:
        degreeChange = i - lastDegree
        turn_to(degreeChange)
        wall_tracker.take_reading_turn(degreeChange)
        lastDegree = i

def turn_to(degrees):
    
    global posR, posL
    posR = 0
    posL = 0
    degree = (((degrees/360) * (17.687 * 2.54))/(0.225 * 2.54))
    degreesteps = np.floor(degree)
    
    # Activate Motors
    GPIO.output(k.R_MOTOR_ACTV, True)
    GPIO.output(k.L_MOTOR_ACTV, True)
    
    while ((posR < degreesteps) or (posL < degreesteps)):
        moveratioR = ((degreesteps - posR)/degreesteps) * 100
        moveratioL = ((degreesteps - posL)/degreesteps) * k.LR_BIAS * 100
        if (moveratioL > 85):
            moveratioL = 85
        if (moveratioL < 25):
            moveratioL = 25
        if (moveratioR > 85):
            moveratioR = 85
        if (moveratioR < 25):
            moveratioR = 25
        GPIO.output(k.R_MOTOR_RV, False)
        GPIO.output(k.L_MOTOR_FW, False)
        rfw.start(moveratioR)
        lrv.start(moveratioL)

    rfw.stop()
    lrv.stop()
    
    # Deactivate Motors
    GPIO.output(k.R_MOTOR_ACTV, False)
    GPIO.output(k.L_MOTOR_ACTV, False)


def brake(seconds):
    # Deactivate Motors
    GPIO.output(k.R_MOTOR_ACTV, False)
    GPIO.output(k.L_MOTOR_ACTV, False)
   
    #Stop Motor Control Singal
    GPIO.output(k.R_MOTOR_RV, False)
    GPIO.output(k.R_MOTOR_FW, False)
    GPIO.output(k.L_MOTOR_RV, False)
    GPIO.output(k.L_MOTOR_FW, False)
    sleep(seconds)


def close_pins():
    GPIO.cleanup()


def updateR(dummy):
    global lastencodedR, posR
    encodedR = GPIO.input(k.R_MOTOR_ENC)
    # encodedR = GPIO.input(k.R_MOTOR_VAL)
    if (encodedR != lastencodedR):
        posR += 1
    lastencodedR = encodedR


def updateL(dummy):
    global lastencodedL, posL
    encodedL = GPIO.input(k.L_MOTOR_ENC)
    # encodedL = GPIO.input(k.L_MOTOR_VAL)
    if (encodedL != lastencodedL):
        posL += 1
    lastencodedL = encodedL
