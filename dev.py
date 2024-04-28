from microscope.steppers import Stepper
import pyspacemouse
import time


# Delay between reading the mouse
motion_update_sec = 0.1
update_steps = 100

def run():
    
    # How often to update the motors, max signal speed
    update_sec=0.1
    signal_sec=0.001
    kwargs = dict(
        update_sec=update_sec,
        signal_sec=signal_sec,
    )

    # Create the steppers    
    stepper_x = Stepper(ena_pin=8, dir_pin=10, pul_pin=12)
    stepper_y = Stepper(ena_pin=22, dir_pin=24, pul_pin=26)
    stepper_z = Stepper(ena_pin=36, dir_pin=38, pul_pin=40)
    
    try:
    
    # Create the mouse connection
    mouse = pyspacemouse.open()
    
    try:    
        base = time.time()
        while True:
            # Continuously poll the mouse, to have the latest position available
            mouse_state = mouse.read()
            now = time.time()
            
            # If it is time to update the motors
            if now - base > update_sec:
                stepper_x.ns.val = mouse_state.roll
                stepper_y.ns.val = mouse_state.pitch
                stepper_z.ns.val = mouse_state.yaw
                
                # Update time
                base = time.time()
            else:
                time.sleep(update_sec)
                
    # Disable motors to prevent overheating.
    except KeyboardInterrupt:
        stepper_x.disable()
        stepper_y.disable()
        stepper_z.disable()
    
if __name__ == '__main__':
    run()
