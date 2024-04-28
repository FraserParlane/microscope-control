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
        """
        # Defaults are for first motor. (Top controller.)
        ena_pin - engaged when low (will warm up when engaged).
        dir_pin - direction pin. Clockwise facing the motor when high.
        pul_pin - initates a step when changing from high to low.
        update_sec - 
        """
        
        self.ena_pin = ena_pin
        self.dir_pin = dir_pin
        self.pul_pin = pul_pin
        self.update_sec = update_sec
        self.signal_sec = signal_sec
        
        # Maximum number of steps in an update. Divided by two, to allow for on
        # and off
        self.n_update_max = int((update_sec/signal_sec)/2)
        
        # Configure the basic state of the namespace. The ns namespace can be 
        # read within the process, and updated from outsite of the process.
        # Only .val is used.
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

    def disable(self) -> None:
        """Disable the motor."""
        GPIO.output(self.ena_pin, GPIO.HIGH)
        
    def _run(self, ns) -> None:
        """Runs continuously to control stepper motor."""
        while True:
            
            # Get enable pin value
            ena_pin = GPIO.input(self.ena_pin)
            
            # If should be stationary
            if ns.val == 0:
                
                # If engaged, disengage
                if ena_pin == GPIO.LOW:
                    GPIO.output(self.ena_pin, GPIO.HIGH)
                
                # If no change, wait
                else:
                    time.sleep(0.1)
                
            # If should be moving
            else:
                
                # If disengaged, engage
                if ena_pin == GPIO.HIGH:
                    GPIO.output(self.ena_pin, GPIO.LOW)
                    
                # Determine direction
                dir_pin = GPIO.input(self.dir_pin)
                if ns.val < 0 and dir_pin == GPIO.HIGH:
                    GPIO.output(self.dir_pin, GPIO.LOW)
                elif ns.val > 0 and dir_pin == GPIO.LOW:
                    GPIO.output(self.dir_pin, GPIO.HIGH)
                                               
                # Calculate step size 
                n_steps = max(int(self.n_update_max * abs(ns.val)), 1)
                step_sec = (self.update_sec / n_steps) / 2
                
                # Perform movement
                for _ in range(n_steps):
                    GPIO.output(self.pul_pin, GPIO.HIGH)
                    time.sleep(step_sec)
                    GPIO.output(self.pul_pin, GPIO.LOW)
                    time.sleep(step_sec)