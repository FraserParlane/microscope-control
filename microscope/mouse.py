import pyspacemouse
import time

mouse = pyspacemouse.open()
minx = 0
maxx = 0
miny = 0
maxy = 0
if mouse:
    while 1:
        state = pyspacemouse.read()
        # minx = min(minx, state.x)
        # maxx = max(maxx, state.x)
        # miny = min(miny, state.y)
        # maxy = max(maxy, state.y)
        print(state.x, state.y, state.z)
        # print(minx, maxx, miny, maxy)
        time.sleep(0.01)

