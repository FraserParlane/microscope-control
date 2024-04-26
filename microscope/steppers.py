from multiprocessing.managers import Namespace
from multiprocessing import Process, Manager
import RPi.GPIO as GPIO
import time


class Stepper:
    def __init__(
        self,
        ena_pin: int,
        dir_pin: int,
        pul_pin: int,
    ) -> None:
        
        self.ena_pin = ena_pin
        self.dir_pin = dir_pin
        self.pul_pin = dir_pin
        self._action: float = 0
        
        # multiprocessing objects
        manager = Manager()
        self.ns = manager.Namespace()
        
    def _run(
        self,
        ns,
    ) -> None:
        
        pass


        


def run():
    
    # Pin 6 - ground
    # Pin 8 - (GPIO 14, UART TX) -> ENA+
    # Pin 10 - (GPIO 15, UART RX) -> DIR+
    # Pin 12 - (GPIO 18, PCM CLK) -> PUL+
    
    ENA = 8
    DIR = 10
    PUL = 12
    
    # Set up board
    GPIO.setmode(GPIO.BOARD)
    
    # Establish pin types
    GPIO.setup(ENA, GPIO.OUT)
    GPIO.setup(DIR, GPIO.OUT)
    GPIO.setup(PUL, GPIO.OUT)
    
    # Confirm that the motor is enabled
    GPIO.output(ENA, GPIO.LOW)

    try:
        # Turn
        while True:
            
            GPIO.output(PUL, GPIO.HIGH)
            
            time.sleep(0.001)
            
            GPIO.output(PUL, GPIO.LOW)

            time.sleep(0.001)
            
    # Disable the motor on exit
    except KeyboardInterrupt:
        GPIO.output(ENA, GPIO.HIGH)


if __name__ == '__main__':
    run()