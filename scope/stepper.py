from multiprocessing import Process, Manager
# import RPi.GPIO as GPIO
from RPi import GPIO
from enum import Enum
import time

class Dir(Enum):
    """Direction of stepper motor."""
    
    FORWARD = 'forward'
    BACKWARD = 'backward'

# Silence warnings
GPIO.setwarnings(False)
    

class Stepper:
    def __init__(
        self,
        id: str = 'none',
        ena_pin: int = 8,
        dir_pin: int = 10,
        pul_pin: int = 12,
        update_sec: float = 0.1,
        signal_sec: float = 0.001,
        keep_engaged: bool = False,
    ) -> None:
        """
        The control interface for a single stepper motor. Upon class
        instantiation, a continuously running process is started that watches
        for changes to self.ns.val. Val can range from -1 (full speed backward)
        to 1 (full speed forward).

        Args:
            id (str, optional): The name of the motor. Used in logging.
            Defaults to 'none'.
            ena_pin (int, optional): The GPIO pin to engage the motor. LOW:
            engaged. HIGH: disengaged. Defaults to 8.
            dir_pin (int, optional): Direction pin. Clockwise facing the motor:
            HIGH. Counterclockwise facing the motor: LOW. Defaults to 10.
            pul_pin (int, optional): Initiates a step when toggled. Defaults to
            12.
            update_sec (float, optional): The frequency at which to look for
            updated data (seconds). Defaults to 0.1.
            signal_sec (float, optional): The fastest rate at which the stepper
            motor pul_pin (movement) will be toggled (sec) when val is set to -1
            or 1. Defaults to 0.001.
            keep_engaged (bool, optional): Should the motor be kept engaged when
            the movement value is set to 0. If False, the motor will freely move
            and will have a jerk upon new movement. If True, the motor will
            remained locked in place when not moving, and might heat up
            slightly. Defaults to False.
        """

        
        # Define the pins
        self.ena_pin = ena_pin
        self.dir_pin = dir_pin
        self.pul_pin = pul_pin
        
        # Define the configuration
        self.update_sec = update_sec
        self.signal_sec = signal_sec
        self.keep_engaged = keep_engaged
        self.id = id
        
        # Maximum number of steps, or motor toggles, in an update period.
        # Divided by two, to allow for on and off.
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
        
        # Track if the motor is enabled or not.
        # If the ena pint is low, the motor is engaged
        self.ns.engaged = GPIO.input(self.ena_pin) == GPIO.LOW
        
        # Determine the direction of the motor. Set forward by default.
        # Forward - GIPO.HIGH
        # Backward - GPIO.LOW
        GPIO.output(self.dir_pin, GPIO.HIGH)
        self.ns.dir = Dir.FORWARD
        
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
            
            # If should be stationary.
            if ns.val == 0:
                
                # If engaged and not keeping engaged, disenage.
                if self.ns.engaged and not self.keep_engaged:
                    GPIO.output(self.ena_pin, GPIO.HIGH)
                    self.ns.engaged = False
                time.sleep(self.update_sec)
                continue
                
            # If disengaged, engage.
            if not self.ns.engaged:
                GPIO.output(self.ena_pin, GPIO.LOW)
                self.ns.engaged = True
                
            # Update direction, if needed.
            if ns.val < 0 and self.ns.dir == Dir.FORWARD:
                GPIO.output(self.dir_pin, GPIO.LOW)
                self.ns.dir = Dir.BACKWARD
            if ns.val > 0 and self.ns.dir == Dir.BACKWARD:
                GPIO.output(self.dir_pin, GPIO.LOW)
                self.ns.dir = Dir.FORWARD

            # Calculate the number of steps to perform.
            n_steps = max(int(self.n_update_max * abs(ns.val)), 1)
            
            # Determine how long to wait between steps.
            step_sec = (self.update_sec / n_steps) / 2
            
            # Perform movement.
            for _ in range(n_steps):
                GPIO.output(self.pul_pin, GPIO.HIGH)
                time.sleep(step_sec)
                GPIO.output(self.pul_pin, GPIO.LOW)
                time.sleep(step_sec)
                
