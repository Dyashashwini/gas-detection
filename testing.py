# Importing required modules
from machine import Pin, reset, Timer, ADC, unique_id
import network
from time import sleep
from umqtt.robust import MQTTClient
import os
import sys
from dht import DHT22
from ubinascii import hexlify
from functions import sms

# Initializing the variables
flame = Pin(12, Pin.IN)
gas_analog = ADC(0)
sensor = DHT22(Pin(14))
gas_digital = Pin(13, Pin.IN)
buzzer = Pin(4, Pin.OUT)
buzzer.value(0)

fire = False
gas_leak = False

def connect(ssid, password):
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(ssid, password)
        while not sta_if.isconnected():
            print(".",end="")
            sleep(1)
    print('network config:', sta_if.ifconfig())

# Function to initialize a connection
connect("********", "*********")

# Important Credentials
MQTT_CLIENT_ID = bytes(hexlify(unique_id()), 'utf-8')
ADAFRUIT_IO_URL = b'io.adafruit.com'
ADAFRUIT_USERNAME = b'*********'
ADAFRUIT_IO_KEY = b'aio_leSY317*****************'

# Assigning the values for the client function
client = MQTTClient(client_id=MQTT_CLIENT_ID,
                    server=ADAFRUIT_IO_URL,
                    user=ADAFRUIT_USERNAME,
                    password=ADAFRUIT_IO_KEY,
                    keepalive=3600,
                    ssl=False)

# Feeds required for us
mqtt_analog = bytes('{:s}/feeds/analog'.format(ADAFRUIT_USERNAME), 'utf-8')
mqtt_fire = bytes('{:s}/feeds/fire'.format(ADAFRUIT_USERNAME), 'utf-8')
mqtt_log = bytes('{:s}/feeds/log'.format(ADAFRUIT_USERNAME), 'utf-8')
mqtt_gas = bytes('{:s}/feeds/gas'.format(ADAFRUIT_USERNAME), 'utf-8')
mqtt_temp = bytes('{:s}/feeds/temp'.format(ADAFRUIT_USERNAME), 'utf-8')
mqtt_hum = bytes('{:s}/feeds/hum'.format(ADAFRUIT_USERNAME), 'utf-8')

# Setting the last will function
client.set_last_will(mqtt_log,bytes(str('ESP Disconnected'), 'utf-8'), retain=False, qos=2)

try:
    # Initialize connection with the given credentials
    client.connect()
    print('Connected to MQTT Server.')
except Exception as e:
    # If unable to connect then restart the device.
    print('Could not connect to MQTT server {}{}'.format(type(e).__name__, e))
    sleep(5)
    reset()

def update(info):
    try:
        sensor.measure()
        gas = gas_analog.read()
        client.publish(mqtt_analog, bytes(str(gas), 'utf-8'), qos=0)
        client.publish(mqtt_temp, bytes(str(sensor.temperature()), 'utf-8'), qos=0)
        client.publish(mqtt_hum, bytes(str(sensor.humidity()), 'utf-8'), qos=0)
        print("Analog Gas Value: " + str(gas))
    except Exception as e:
        return('Failed to read sensor.')
        print(str(e))

def handle_interrupt(info):
    global fire, gas_leak
    try:
        gas_val = gas_digital.value()
        flame_val = flame.value()
        if gas_val == 0 and gas_leak == False:
            gas_leak = True
            print("Gas Leak Detected!!!")
            client.publish(mqtt_log, bytes(str("Gas Leak Detected"), 'utf-8'), qos=0)
            client.publish(mqtt_gas, bytes(str(0), 'utf-8'), qos=0)
            sms("Gas Leak Detected!!!!")
            buzzer.value(1)
        elif gas_val == 1 and gas_leak == True:
            gas_leak = False
            buzzer.value(0)
            client.publish(mqtt_gas, bytes(str(1), 'utf-8'), qos=0)
        if flame_val == 0 and fire == False:
            fire = True
            print("Fire Detected!!!")
            client.publish(mqtt_log, bytes(str("Fire Detected"), 'utf-8'), qos=0)
            client.publish(mqtt_fire, bytes(str(0), 'utf-8'), qos=0)
            sms("Fire Detected!!!!")
            buzzer.value(1)
        elif flame_val == 1 and fire == True:
            fire = False
            buzzer.value(0)
            client.publish(mqtt_fire, bytes(str(1), 'utf-8'), qos=0)
    except Exception as err:
        print("Error: "+ str(err))

try:
    analog = Timer(4)
    digital = Timer(2)
    analog.init(mode=Timer.PERIODIC, period=10000, callback=update)
    digital.init(mode=Timer.PERIODIC, period=1000, callback=handle_interrupt)
except Exception as err:
    print("Error: " + str(err))
