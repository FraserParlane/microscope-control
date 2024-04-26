import pyspacemouse
import time

mouse = pyspacemouse.open()
counter = 0
if mouse:
    while True:
        state = pyspacemouse.read()
        if counter % 10 == 0:
            print(state.x, state.y, state.z, state.pitch, state.roll, state.yaw)
        counter += 1
        # time.sleep(0.01)