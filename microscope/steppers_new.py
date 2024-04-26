from multiprocessing.managers import Namespace
from multiprocessing import Process, Manager
from typing import Optional
import RPi.GPIO as GPIO
import time


class Stepper:
    def __init__(
        self,
        ena_pin: Optional[int] = None,
        dir_pin: Optional[int] = None,
        pul_pin: Optional[int] = None,
    ) -> None:
        
        self.ena_pin = ena_pin
        self.dir_pin = dir_pin
        self.pul_pin = pul_pin
        self._action: float = 0
        
        # multiprocessing objects
        manager = Manager()
        self.ns = manager.Namespace()
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
            print(ns.val)
            print(self.dir_pin)
            time.sleep(0.25)
    
if __name__ == '__main__':
    stepper = Stepper(dir_pin=100)
    for i in range(10):
        stepper.ns.val = i
        stepper.dir_pin = 200
        time.sleep(1)
    while True:
        time.sleep(100)