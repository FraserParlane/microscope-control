from sense_hat import SenseHat
import pyspacemouse
import time
import sys


def run():
    """
    A quick demo of the mouse controlling the LED display on the sensehat.
    """
    
    # Connect to the sensehat.
    sense = SenseHat()
    
    # Connect to the mouse.
    mouse = pyspacemouse.open()
    
    try:
    
        while True:
            
            # Get the current x, y position of the mouse.
            state = pyspacemouse.read()

            # Determine the pixel to color
            x = round(state.x * 4)
            y = round(state.y * 4)
    
            # Clear pixels
            sense.clear()
            
            # Set pixels
            for i in [0, 1]:
                for j in [0, 1]:
                    ix = max(min(3+x+i, 7), 0)
                    iy = max(min(3+y+j, 7), 0)
                    sense.set_pixel(ix, iy, 255, 255, 255)
            
            # Wait
            time.sleep(0.01)
    except KeyboardInterrupt:
        sense.clear()
        sys.exit(0)

if __name__ == '__main__':
    run()