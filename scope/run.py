from stepper import Stepper
from config import Config
from pathlib import Path
import pyspacemouse
import time
import yaml


def run(
    config_path: Path,
):
    """Start controlling the stepper motors.

    Args:
        config_path (Path): The path to the config file.
    """
    
    # Read in the configuration file
    with open(config_path, 'r') as f:
        config_dict = yaml.safe_load(f)
    config = Config(**config_dict)
        
    
    # Create the stepper motors
    stepper_x = Stepper(**dict(config.stepper_x), **dict(config.steppers))
    stepper_y = Stepper(**dict(config.stepper_y), **dict(config.steppers))
    stepper_z = Stepper(**dict(config.stepper_z), **dict(config.steppers))
    
    try:
    
        # Create the mouse connection. Wait until the mouse is available.
        while True:
            try:
                mouse = pyspacemouse.open()
                break
            except Exception as _:
                time.sleep(config.mouse_timeout)
    
        base = time.time()
        while True:
            
            # Continuously poll the mouse, to have the latest position available
            mouse_state = mouse.read()
            now = time.time()
            
            # If it is time to update the motors
            if now - base > config.update_sec:
                stepper_x.ns.val = mouse_state.roll
                stepper_y.ns.val = mouse_state.pitch
                stepper_z.ns.val = mouse_state.yaw
                
                # Update time
                base = time.time()
                
    # If any error is thrown in the program, disable motors to prevent
    # overheating.
    except Exception as _:
        stepper_x.disable()
        stepper_y.disable()
        stepper_z.disable()
    
if __name__ == '__main__':
    run(config_path=Path(__file__).parent / 'config.yaml')
