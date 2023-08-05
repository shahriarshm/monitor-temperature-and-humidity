import dht
import time
import urequests
import network
from machine import Pin

P5 = Pin(5, Pin.IN)
LED = Pin(16, Pin.OUT)

WIFI_SSID = ""
WIFI_PASSWORD = ""

API_URL = "http://192.168.1.101:8000/sensors_data"

d = dht.DHT11(P5)

# Connect to WiFi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
if not wlan.isconnected():
    print('connecting to network...')
    wlan.connect(WIFI_SSID, WIFI_PASSWORD)
    while not wlan.isconnected():
        pass
print('network config:', wlan.ifconfig())

# Upload DHT data priodically
while True:
    LED.value(0)  # ON
    time.sleep(0.5)
    LED.value(1)  # OFF
    time.sleep(0.5)
    
    try:
        print("getting dht data...")
        d.measure()
        temperature = d.temperature()
        humidity = d.humidity()
        print(f"temperature: {temperature}")
        print(f"humidity: {humidity}")

        urequests.post(API_URL, json={"temperature": temperature, "humidity": humidity})
    except OSError as e:
        print("Error:", e)

    time.sleep(9)
