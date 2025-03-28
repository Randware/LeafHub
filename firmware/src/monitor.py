import config
import requests
import network
import device
import time
import urequests

NETWORK_CONNECT_ATTEMPTS = 3
PROBING_INTERVAL = 1

def connect_network():
    wlan = network.WLAN(network.STA_IF)

    wlan.active(True)

    conf = config.load()
        
    for i in range(NETWORK_CONNECT_ATTEMPTS):
        if i > 0:
            print(f"Retrying with {NETWORK_CONNECT_ATTEMPTS - i} attempts left ...")

        wlan.connect(conf.network_ssid, conf.network_password)

        while wlan.status() == network.STAT_CONNECTING:
            time.sleep(0.1)
            pass

        status = wlan.status()

        if status == network.STAT_WRONG_PASSWORD:
            print("Wrong password detected, aborting ...")
            break
        elif status ==  network.STAT_NO_AP_FOUND:
            print("Network not found")
        elif status == network.STAT_CONNECT_FAIL:
            print("Failed connecting to network")
        else:
            print("Successfully connected to network")
            return
        
    print("Failed connecting to network")
    raise ConnectionError

    
def take_probe():
    # Sample data 
    #  TODO: Measure sensors
    data = {"temperature": 34, "humidity": 60}

    return data

def send_probe(url, headers):
    data = take_probe()

    response = requests.post(url, json=data, headers=headers)

    code = response.status_code
    text = response.text

    if code < 300:
        print(f"Successfully sent probe ({code})")
    else:
        print(f"Failed sending probe ({code}): {text}")

    response.close()


def start_sending():
    conf = config.load()

    headers = {
        "Content-Type": "application/json",
        "X-Auth-Token": conf.auth_token
    }

    url = conf.server_address

    while True:
        send_probe(url, headers)
        time.sleep(PROBING_INTERVAL)

def start():
    device.led_off()
    connect_network()
    start_sending()
