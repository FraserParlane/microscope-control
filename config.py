from pydantic import BaseModel


class Stepper(BaseModel):
    """The configuration of a stepper motor."""
    
    ena_pin: int
    dir_pin: int
    pul_pin: int
    
class Config(BaseModel):
    """The global configuration of the project."""
    
    update_sec: float
    signal_sec: float
    keep_engaged: bool
    mouse_timeout: float
    stepper_x: Stepper
    stepper_y: Stepper
    stepper_z: Stepper