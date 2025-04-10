import network
import time
import hardware
import config
from machine import Pin

CONFIG = config.load()
LED = Pin(hardware.PINS["status_led"].pin, Pin.OUT)

def led_on():
    LED.on()

def led_off():
    LED.off()

def get_networks():
    wifi = network.WLAN(network.STA_IF)
    wifi.active(True)
    networks = []

    scanned = wifi.scan()

    for net in scanned:
        ssid:str = net[0].decode("utf-8") if isinstance(net[0], bytes) else net[0]
        rssi = net[3]

        if ssid != "":
            networks.append({"ssid": ssid, "strength": rssi})

    return networks


def save_network_ssid(network_ssid: str):
    CONFIG.network_ssid = network_ssid
    CONFIG.save()


def save_network_password(network_password: str):
    CONFIG.network_password = network_password
    CONFIG.save()


def save_server_address(server_address: str):
    CONFIG.server_address = server_address
    CONFIG.save()


def save_auth_token(auth_token: str):
    CONFIG.auth_token = auth_token
    CONFIG.save()
