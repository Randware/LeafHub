# This is an example template that can be used when writing a Hardware Abstraction Layer (HAL)
# for different microcontrollers and sensor sets.

# This module can be used to make writing HALs easier, although it is not required.
# It is important that the types and interfaces match up (which can be ensured using this module).
import hal

# Creating a custom sensor is possible by adhering to the interface requirements.
class MySensor(hal.SensorInterface):
    def __init__(self, name: str):
        # A name is required for every sensor.
        self.name = name

    # A "read" method, which reads the sensors data, is also required.
    # This method can return strings, integers or floats.
    def read(self) -> float:
        return 0

# If you were to do this without using the "hal" module, you can simply omit the inheritance,
# but make sure to implement the required fields and values:

# class MySensor:
#     def __init__(self, name: str):
#         self.name = name
#
#     def read(self) -> float:
#         return 0

# This "PINS" dictionary tells the firmware which pin numbers correspond to the desired pins.
# By specifying the "PINS" dictionary to be of type "PinsDict" we can ensure all required pins
# are provided. Once again, this is not mandatory, all that matters is that we implement the
# required values with the correct types.
PINS: hal.PinsDict = {
    # This specifies the pin corresponding to the onboard LED, which will be used for displaying,
    # the controllers status.
    "status_led": hal.LED(2)
}

# Here we define the "read_hum" function we use below
def read_hum() -> float:
    return 0

# In the "SENSORS" list we define all sensors we would like the microcontroller to read,
# while also telling it how to read them. Once again, typing is important, by specifying
# the lists type to be "SensorInterface" we can make sure everything is right.
SENSORS: list[hal.SensorInterface] = [
    # Here we can use our "MySensor" sensor implementation we defined above
    MySensor(name="my_sensor"),

    # The "hal" module also provides a default "Sensor" class, where
    # we only have to specify the function that will be used in order
    # to read the sensor, in case we don't want to write a custom sensor.
    hal.Sensor(name="humidity", read_func=read_hum),
]
