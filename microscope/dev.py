from steppers import Stepper
import RPi.GPIO as GPIO
import pyspacemouse
import numpy as np
import logging
import time

logging.basicConfig(level=logging.DEBUG)

# Delay between reading the mouse
motion_update_sec = 0.1
update_steps = 100

def run():
    
    stepper = Stepper()
    while True:
        for i in np.linspace(0, 1, 10):
            stepper.ns.val = i
            time.sleep(1)

    
    
    
    
if __name__ == '__main__':
    run()
