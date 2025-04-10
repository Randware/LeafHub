# This file provides typing for writing a Hardware Abstraction Layer (HAL)

from typing import Callable, Protocol, Union, TypedDict

class PinInterface(Protocol):
    pin: Union[str, int]
    

class LED(PinInterface):
    def __init__(self, pin: Union[str, int]):
        self.pin = pin

class PinsDict(TypedDict):
    status_led: LED

class SensorInterface(Protocol):
    name: str
    def read(self) -> Union[str, int, float]:
        ...

class Sensor:
    def __init__(self, name: str, read_func: Callable[[], Union[str, float, int]]):
        self.name = name
        self.read_func = read_func

    def read(self) -> Union[str, float, int]:
        return self.read_func()
    
