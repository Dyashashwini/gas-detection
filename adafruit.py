# Importing required modules
from machine import Pin, reset, Timer
import network
from time import sleep
from umqtt.robust import MQTTClient
import os
import sys
from ubinascii import hexlify

# Function to initialize a connection
def do_connect():
    import network
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect("SSID", "PASSWORD")
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())

# Connect to Wifi from Function
do_connect()

# Important Credentials
MQTT_CLIENT_ID = bytes(hexlify(machine.unique_id()), 'utf-8')
# MQTT server and serverport=1883 needs to be added in adafruit for mqtt connection
ADAFRUIT_IO_URL = b'io.adafruit.com'
ADAFRUIT_USERNAME = b'***********'
ADAFRUIT_IO_KEY = b'aio_unwx86YFKwP3nPl4i*********'

# Assigning the values for the client function
client = MQTTClient(client_id=MQTT_CLIENT_ID,
                    server=ADAFRUIT_IO_URL,
                    user=ADAFRUIT_USERNAME,
                    password=ADAFRUIT_IO_KEY,
                    keepalive=3600,
                    ssl=False)

# Feeds required for us
mqtt_temp = bytes('{:s}/feeds/flame'.format(ADAFRUIT_USERNAME), 'utf-8')
mqtt_humid = bytes('{:s}/feeds/gas'.format(ADAFRUIT_USERNAME), 'utf-8')
mqtt_log = bytes('{:s}/feeds/log'.format(ADAFRUIT_USERNAME), 'utf-8')

# Setting the last will function
client.set_last_will(mqtt_log,bytes(str('ESP Disconnected'), 'utf-8'), retain=False, qos=0)

try:
    # Initialize connection with the given credentials
    client.connect()
    print('Connected to MQTT Server.')
except Exception as e:
    # If unable to connect then restart the device.
    print('Could not connect to MQTT server {}{}'.format(type(e).__name__, e))
    sleep(5)
    reset()

# Callback function for Timer
def update(info):
    try:
        # Check for sensor values
        # If smoke or flame detected :
            # Send an sms to user
            # Upload the current data
        #else:
            # Compare the previous data and upload if necessary
        print("Working")
    except Exception as e:
        return('Failed to read sensor.')

# function to upload data to Adafruit
def set_value(feed_name, value):
    return client.publish(feed_name, bytes(str(value), 'utf-8'), qos=1)

# Initialize a timer
tim = Timer(4)
# Assigning callback and period to it
tim.init(mode=Timer.PERIODIC, period=2000, callback=update)
