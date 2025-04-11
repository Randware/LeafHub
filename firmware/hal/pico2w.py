import hal

PINS: hal.PinsDict = {
    "status_led": hal.LED("LED")
}

import machine
import dht

sen = dht.DHT11(machine.Pin(28))

def read_temp() -> float:
    sen.measure()

    return sen.temperature()

def read_hum() -> float:
    sen.measure()

    return sen.humidity()

def read_soil() -> int:
    adc = machine.ADC(machine.Pin(27))

    val = adc.read_u16()
    norm = (val / 65535 ) * 100
    inverted = 100 - norm

    print(inverted)

    return inverted


SENSORS: list[hal.SensorInterface] = [
    hal.Sensor(name="temperature", read_func=read_temp),
    hal.Sensor(name="humidity", read_func=read_hum),
    hal.Sensor(name="soil", read_func=read_soil)
]
