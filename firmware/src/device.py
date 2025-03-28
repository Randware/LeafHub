import network
import time
import config
from machine import Pin

NETWORK_SCAN_TIMEOUT = 10
CONFIG = config.load()
LED = Pin("LED", Pin.OUT)

def led_on():
    LED.on()

def led_off():
    LED.off()

def get_networks():
    wifi = network.WLAN(network.STA_IF)
    wifi.active(True)
    networks = []
    start_time = time.time()

    while (time.time() - start_time) <= NETWORK_SCAN_TIMEOUT:
        scanned = wifi.scan()

        for net in scanned:
            ssid = net[0].decode("utf-8") if isinstance(net[0], bytes) else net[0]
            rssi = net[3]

            contained = False
            for saved in networks:
                if saved["ssid"] == ssid:
                    contained = True
                    break

            if not contained and ssid != "":
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
