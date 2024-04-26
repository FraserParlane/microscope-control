from dataclasses import dataclass
import RPi.GPIO as GPIO
import pyspacemouse
import logging
import time

logging.basicConfig(level=logging.DEBUG)

# Delay between reading the mouse
motion_update_sec = 0.1
update_steps = 100

# Speed parameters
speed_min = 1
speed_max = 10
speed_state = 5

    

def button_callback(state, buttons) -> None:
    """Called when left and right buttons pressed. Updates speed_state"""
    global speed_state
    if buttons[0]:
        speed_state = max(speed_min, speed_state - 1)
    elif buttons[-1]:
        speed_state = min(speed_max, speed_state + 1)
    else:
        return None
    logging.debug(f'speed_state: {speed_state}')

def run():
    
    # Instantiate the mouse
    mouse = pyspacemouse.open(
        button_callback=button_callback
    )
    
    # Define the stepper
    stepper = Stepper(ena_pin=8, dir_pin=10, pul_pin=12)
    
    
    try:
        while True:
            
            # Read the mouse
            state = mouse.read()
            print('a')
            
            for i in range(update_steps):
                pass
                            
            # Sleep before repolling the mouse            
    except KeyboardInterrupt:
        pass
    
if __name__ == '__main__':
    run()
