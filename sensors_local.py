import dht
import gc
import json
import machine
import network
import re

try:
  import usocket as socket
except:
  import socket

gc.collect()

# Pins
P5 = machine.Pin(5)

# WIFI
WIFI_SSID = ""
WIFI_PASSWORD = ""

# Last DHT Data
last_temprature = 0
last_humidity = 0


def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)
        while not wlan.isconnected():
            pass
    print('network config:', wlan.ifconfig())


def get_dht():
    global last_temprature, last_humidity
    d = dht.DHT11(P5)
    print("getting dht data...")
    d.measure()
    last_temprature = d.temperature()
    last_humidity = d.humidity()
    print(f"temprature: {last_temprature}")
    print(f"humidity: {last_humidity}")
    return d


def html_response(conn, content):
    conn.send("HTTP/1.1 200 OK\n")
    conn.send("Content-Type: text/html\n")
    conn.send("Connection: close\n\n")
    conn.send(content)
    conn.close()


def json_response(conn, content):
    conn.send("HTTP/1.1 200 OK\n")
    conn.send("Content-Type: application/json\n")
    conn.send("Connection: close\n\n")
    conn.send(json.dumps(content))
    conn.close()


connect_wifi()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)

while True:
    get_dht()

    try:
        conn, addr = s.accept()
        conn.settimeout(3)
        print(f"received http connection request from {addr}")
        
        request = conn.recv(1024).decode()
        conn.settimeout(None)
        
        match = re.match(r'^(?:GET|POST)\s+(\S+)\s+HTTP/\d\.\d', request)
        if not match:
            html_response(conn, "Not found")
            continue
        
        path = match.group(1)
        if path == "/":
            html_response(conn, "Index page")
        elif path == "/data":
            json_response(conn, {"temprature": last_temprature, "humidity": last_humidity})
        else:
            html_response(conn, "Not found")
            
  
    except OSError as e:
        conn.close()
        print("connection closed")

