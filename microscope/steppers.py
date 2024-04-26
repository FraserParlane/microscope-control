from multiprocessing.managers import Namespace
from multiprocessing import Process, Manager
from dataclasses import dataclass
from typing import Optional
import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
    

class Stepper:
    def __init__(
        self,
        ena_pin: int = 8,
        dir_pin: int = 10,
        pul_pin: int = 12,
    ) -> None:
        
        self.ena_pin = ena_pin
        self.dir_pin = dir_pin
        self.pul_pin = pul_pin
        
        # Configure the basic state of the namespace
        manager = Manager()
        self.ns = manager.Namespace()
        self.ns.enable = False
        
        # Configure the GPIO pins
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.ena_pin, GPIO.OUT)
        GPIO.setup(self.dir_pin, GPIO.OUT)
        GPIO.setup(self.pul_pin, GPIO.OUT)
        
        # Start the continuous process
        process = Process(
            target=self._run,
            kwargs=dict(ns=self.ns),
        )
        process.start()

        
    def _run(
        self,
        ns,
    ) -> None:
        """Runs continuously to control stepper motor."""
        while True:
            if ns.enable:
                GPIO.output(self.ena_pin, GPIO.LOW)
                for i in range(500):
                    GPIO.output(self.pul_pin, GPIO.HIGH)
                    time.sleep(0.001)
                    GPIO.output(self.pul_pin, GPIO.LOW)
                    time.sleep(0.001)
                GPIO.output(self.ena_pin, GPIO.HIGH)
                ns.enable = False
            else:
                time.sleep(0.1)
    
if __name__ == '__main__':
    stepper = Stepper()
    for i in range(3):
        stepper.ns.enable = True
        time.sleep(2)