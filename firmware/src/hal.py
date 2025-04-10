# FIX: Use proper typing here

class PinInterface:
    pin: object

class LED(PinInterface):
    def __init__(self, pin: object):
        self.pin = pin

class PinsDict:
    status_led: LED

class SensorInterface:
    name: str
    def read(self) -> object:
        ...

class Sensor:
    def __init__(self, name: str, read_func):
        self.name = name
        self.read_func = read_func

    def read(self) -> object:
        return self.read_func()
    
