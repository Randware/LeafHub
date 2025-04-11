import hal

PINS: hal.PinsDict = {
    "status_led": hal.LED(2)
}

import machine
import dht
sen = dht.DHT11(machine.Pin(23))
machine.Pin(4, machine.Pin.OUT).on()

def read_temp() -> float:
    sen.measure()

    return sen.temperature()

def read_hum() -> float:
    sen.measure()

    return sen.humidity()

SENSORS: list[hal.SensorInterface] = [
    hal.Sensor(name="temperature", read_func=read_temp),
    hal.Sensor(name="humidity", read_func=read_hum)
]
