import config
import network
import time

NETWORK_CONNECT_ATTEMPTS = 3

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

    
def start():
    connect_network()
    
    print("Monitoring is running ...")
    while True:
        pass
