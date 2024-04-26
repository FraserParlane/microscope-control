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
        update_sec: float = 0.1,
        signal_sec: float = 0.001,
    ) -> None:
        
        self.ena_pin = ena_pin
        self.dir_pin = dir_pin
        self.pul_pin = pul_pin
        self.update_sec = update_sec
        self.signal_sec = signal_sec
        
        # Configure the basic state of the namespace
        manager = Manager()
        self.ns = manager.Namespace()
        self.ns.val = 0
        
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
            
            # If no value and enabled, disable.
            if ns.val == 0 and GPIO.input(self.ena_pin) == 0:
                GPIO.output(self.ena_pin, GPIO.HIGH)
                
            # If value and disabled, enable.
            else:
                if GPIO.input(self.ena_pin) == 0:
                    GPIO.output(self.ena_pin, GPIO.LOW)
                
                n_steps = ?
                step_sec = ?
                
                for _ in range(n_steps):
                    GPIO.output(self.pul_pin, GPIO.HIGH)
                    time.sleep(step_sec)
                    GPIO.output(self.pul_pin, GPIO.LOW)
                    time.sleep(step_sec)
    
if __name__ == '__main__':
    stepper = Stepper()
    while True:
        stepper.ns.val = input('Update:')