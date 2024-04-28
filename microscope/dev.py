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
    
    update_sec = 0.1
    signal_sec = 0.001
    
    mouse = pyspacemouse.open()
    stepper = Stepper()
    
    base = time.time()

    try:    
        while True:            
            mouse_state = pyspacemouse.read()
            now = time.time()
            if now - base > update_sec:
                stepper.ns.val = mouse_state.roll
                base = time.time()
    except KeyboardInterrupt:
        stepper.disable()
    
if __name__ == '__main__':
    run()
