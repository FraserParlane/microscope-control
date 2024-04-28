import pyspacemouse
import logging
import time


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
    print(speed_state)

mouse = pyspacemouse.open(button_callback=button_callback)
counter = 0
if mouse:
    while True:
        state = pyspacemouse.read()
        print(state.roll)
        # if counter % 10 == 0:
            # print(state.x, state.y, state.z, state.pitch, state.roll, state.yaw)
        counter += 1
        # time.sleep(0.01)