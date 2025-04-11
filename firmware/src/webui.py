import network
import json
import device
import socket
import time
import os
from util import Request

SSID = "LeafHubSmartPot"
PASSWORD = "00000000"
CHANNEL = 1

WEBSERVER_FILES_PATH = "public"
WEBSERVER_PORT = 80

WEBSERVER_RUNNING = True


def open_access_point():
    ap = network.WLAN(network.AP_IF)
    ap.config(essid=SSID, password=PASSWORD, channel=CHANNEL)
    ap.active(True)

    while not ap.active():
        print("Waiting for access point to become active ...")
        time.sleep(1)

    print(f"Access Point '{SSID}' opened")
    print(f"Password: {PASSWORD}")
    print(f"IP Address: {ap.ifconfig()[0]}")


def serve_not_found(sock, path):
    print(f"Path {path} not found")

    sock.send("HTTP/1.1 404 Not Found\r\n")
    sock.send("Content-Type: text/html\r\n")
    sock.send("Connection: close\r\n\r\n")
    sock.send("<html><body><h1>404 Not Found</h1></body></html>")


def serve_file(sock, path):
    if not path.startswith("/"):
        path = "/" + path

    if path == "/":
        path = "/index.html"

    try:
        os.stat(WEBSERVER_FILES_PATH)
    except OSError:
        print(f'"{WEBSERVER_FILES_PATH}" folder not found')
        print("Please ensure the webui was correctly flashed onto the device")
        return

    file_path = WEBSERVER_FILES_PATH + path

    try:
        os.stat(file_path)

        content_type = "text/plain"

        if path.endswith(".html"):
            content_type = "text/html"
        elif path.endswith(".css"):
            content_type = "text/css"
        elif path.endswith(".js"):
            content_type = "application/javascript"
        elif path.endswith(".json"):
            content_type = "application/json"

        sock.send("HTTP/1.1 200 OK\r\n")
        sock.send(f"Content-Type: {content_type}\r\n")
        sock.send("Connection: close\r\n\r\n")

        with open(file_path, "rb") as file:
            chunk = file.read(1024)
            while chunk:
                sock.write(chunk)
                chunk = file.read(1024)

    except OSError:
        serve_not_found(sock, path)
        return


def send_response(sock, code, response):
    sock.send(f"HTTP/1.1 {code}\r\n")
    sock.send("Content-Type: application/json\r\n")
    sock.send("Connection: close\r\n\r\n")
    sock.write(response)


def handle_request(sock, req):
    code = "200 OK"
    response = '{"message": "success"}'

    if req.method == "GET":
        if req.path == "/networks":
            print("Scanning networks ...")
            networks = device.get_networks()
            print(f"Finished scanning, found {len(networks)} networks")

            response = json.dumps(networks)

        elif req.path == "/config":
            updated = {}

            if "network_ssid" in req.params:
                device.save_network_ssid(req.params["network_ssid"])
                updated["network_ssid"] = req.params["network_ssid"]
            if "network_password" in req.params:
                device.save_network_password(req.params["network_password"])
                updated["network_password"] = req.params["network_password"]
            if "server_address" in req.params:
                device.save_server_address(req.params["server_address"])
                updated["server_address"] = req.params["server_address"]
            if "auth_token" in req.params:
                device.save_auth_token(req.params["auth_token"])
                updated["auth_token"] = req.params["auth_token"]

            response = json.dumps(
                {"message": "Config successfully updated", "updated": updated}
            )

        elif req.path == "/exit":
            global WEBSERVER_RUNNING
            WEBSERVER_RUNNING = False
            response = '{"message": "Exiting configuration mode"}'

        else:
            serve_not_found(sock, req.path)
            return

    else:
        serve_not_found(sock, req.path)
        return

    send_response(sock, code, response)


def start_webserver():
    global WEBSERVER_RUNNING
    WEBSERVER_RUNNING = True

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("0.0.0.0", WEBSERVER_PORT))
    server_socket.listen(5)

    print(f"Web server running on port {WEBSERVER_PORT}")

    while WEBSERVER_RUNNING:
        sock, addr = server_socket.accept()

        print(f"\nClient connected from {addr}")

        try:
            raw_request = sock.recv(1024).decode("utf-8")

            if not raw_request:
                continue

            req = Request(raw_request)

            print(f"Received {req.method} request for {req.path}")

            if req.path.startswith("/device"):
                parts = req.path.split("/")
                req.path = "/" + "/".join(parts[2:])

                if req.path.endswith("/"):
                    req.path = req.path[:-1]

                handle_request(sock, req)
            else:
                serve_file(sock, req.path)
        except Exception as e:
            print(f"Error handling request: {e}")
        finally:
            sock.close()
                
    server_socket.close()


def start():
    device.led_on()
    open_access_point()
    start_webserver()
