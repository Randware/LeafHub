import network
import time

NETWORK_SCAN_TIMEOUT = 10

def get_networks():
    wifi = network.WLAN(network.STA_IF)
    wifi.active(True)
    networks = []
    start_time = time.time()

    while (time.time() - start_time) <= NETWORK_SCAN_TIMEOUT:
        scanned = wifi.scan()

        for net in scanned:
            ssid = net[0].decode('utf-8') if isinstance(net[0], bytes) else net[0]
            rssi = net[3]

            contained = False
            for saved in networks:
                if saved["ssid"] == ssid:
                    contained = True
                    break

            if not contained and ssid != "":
                networks.append({"ssid": ssid, "strength": rssi})

    return networks
