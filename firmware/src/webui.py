import network
import json
import device
import socket
import time
import os

SSID = "LeafHubSmartPot"
PASSWORD = "00000000"
CHANNEL = 1

WEBSERVER_FILES_PATH = "public"
WEBSERVER_PORT = 80


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


def serve_not_found(socket, path):
    print(f"Path {path} not found")

    socket.send("HTTP/1.1 404 Not Found\r\n")
    socket.send("Content-Type: text/html\r\n")
    socket.send("Connection: close\r\n\r\n")
    socket.send(
        "<html><body><h1>404 Not Found</h1></body></html>"
    )

def serve_file(socket, path):
    if not path.startswith("/"):
        path = "/" + path

    if path == "/":
        path = "/index.html"

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

        socket.send("HTTP/1.1 200 OK\r\n")
        socket.send(f"Content-Type: {content_type}\r\n")
        socket.send("Connection: close\r\n\r\n")

        with open(file_path, "rb") as file:
            chunk = file.read(1024)
            while chunk:
                socket.write(chunk)
                chunk = file.read(1024)

    except OSError:
        serve_not_found(socket, path)
        return


def handle_request(socket, path):
    response = ""

    if path == "/networks/timeout":
        response = "{" + f'"timeout": {device.NETWORK_SCAN_TIMEOUT}' + "}"
    elif path == "/networks":
        print("Scanning networks ...")
        networks = device.get_networks()
        print(f"Finished scanning, found {len(networks)} networks")

        response = json.dumps(networks)

    else:
        serve_not_found(socket, path)
        return

    socket.send("HTTP/1.1 200 OK\r\n")
    socket.send("Content-Type: application/json\r\n")
    socket.send("Connection: close\r\n\r\n")
    socket.write(response)


def start_webserver():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", WEBSERVER_PORT))
    server_socket.listen(5)

    print(f"Web server running on port {WEBSERVER_PORT}")

    try:
        while True:
            client, addr = server_socket.accept()
            print(f"\nClient connected from {addr}")

            try:
                request = client.recv(1024).decode("utf-8")
                if not request:
                    continue

                request_lines = request.split("\r\n")
                if not request_lines:
                    continue

                first_line_parts = request_lines[0].split()
                if len(first_line_parts) < 3:
                    continue

                method, path, _ = first_line_parts
                print(f"Received {method} request for {path}")

                if path.startswith("/device"):
                    path = "/" + "/".join(path.split("/")[2:])

                    if path.endswith("/"):
                        path = path[:-1]

                    handle_request(client, path)
                else:
                    serve_file(client, path)



            except Exception as e:
                print(f"Error handling request: {e}")
            finally:
                client.close()

    except KeyboardInterrupt:
        print("Server stopped")
    finally:
        server_socket.close()


def start():
    open_access_point()
    start_webserver()
