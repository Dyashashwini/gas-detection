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

class Detect:
    # Initializing the variables
    flame = Pin(12, Pin.IN)
    gas_analog = ADC(0)
    sensor = DHT22(Pin(14))
    gas_digital = Pin(13, Pin.IN)
    buzzer = Pin(4, Pin.OUT)
    fire = False
    gas_leak = False
    # Important Credentials
    MQTT_CLIENT_ID = bytes(hexlify(unique_id()), 'utf-8')
    ADAFRUIT_IO_URL = b'io.adafruit.com'
    ADAFRUIT_USERNAME = b'**********'
    ADAFRUIT_IO_KEY = b'aio_leSY317n****************'
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

    def connect(self, ssid, password):
        sta_if = network.WLAN(network.STA_IF)
        if not sta_if.isconnected():
            print('connecting to network...')
            sta_if.active(True)
            sta_if.connect(ssid, password)
            while not sta_if.isconnected():
                print(".",end="")
                sleep(1)
        print('network config:', sta_if.ifconfig())
        
    def initialize(self):
        while True:
            try:
                # Function to initialize a connection
                self.connect("SSID", "PASSWORD")
                # Initialize connection with the given credentials
                self.client.connect()
                print('Connected to MQTT Server.')
                break
            except Exception as e:
                # If unable to connect then restart the device.
                print('Could not connect to MQTT server {}{}'.format(type(e).__name__, e))
                sleep(5)
                
    def __init__(self):
        self.buzzer.value(0)
        self.initialize()
        # Setting the last will function
        self.client.set_last_will(mqtt_log,bytes(str('ESP Disconnected'), 'utf-8'), retain=False, qos=2)

    def update(self, info):
        try:
            self.sensor.measure()
            gas = self.gas_analog.read()
            self.client.publish(self.mqtt_analog, bytes(str(gas), 'utf-8'), qos=0)
            self.client.publish(self.mqtt_temp, bytes(str(self.sensor.temperature()), 'utf-8'), qos=0)
            self.client.publish(self.mqtt_hum, bytes(str(self.sensor.humidity()), 'utf-8'), qos=0)
            print("Analog Gas Value: " + str(gas))
        except Exception as e:
            return('Failed to read sensor.')
            print(str(e))

    def handle_interrupt(self, info):
        try:
            gas_val = self.gas_digital.value()
            flame_val = self.flame.value()
            if gas_val == 0 and self.gas_leak == False:
                self.gas_leak = True
                print("Gas Leak Detected!!!")
                self.client.publish(self.mqtt_log, bytes(str("Gas Leak Detected"), 'utf-8'), qos=0)
                self.client.publish(self.mqtt_gas, bytes(str(0), 'utf-8'), qos=0)
                sms("Gas Leak Detected!!!!")
                self.buzzer.value(1)
            elif gas_val == 1 and self.gas_leak == True:
                self.gas_leak = False
                self.buzzer.value(0)
                self.client.publish(self.mqtt_gas, bytes(str(1), 'utf-8'), qos=0)
            if flame_val == 0 and self.fire == False:
                self.fire = True
                print("Fire Detected!!!")
                self.client.publish(self.mqtt_log, bytes(str("Fire Detected"), 'utf-8'), qos=0)
                self.client.publish(self.mqtt_fire, bytes(str(0), 'utf-8'), qos=0)
                sms("Fire Detected!!!!")
                self.buzzer.value(1)
            elif flame_val == 1 and self.fire == True:
                self.fire = False
                self.buzzer.value(0)
                self.client.publish(self.mqtt_fire, bytes(str(1), 'utf-8'), qos=0)
        except Exception as err:
            print("Error: "+ str(err))
    
    def main(self):
        try:
            analog = Timer(4)
            digital = Timer(2)
            analog.init(mode=Timer.PERIODIC, period=10000, callback=update)
            digital.init(mode=Timer.PERIODIC, period=2000, callback=handle_interrupt)
        except Exception as err:
            print("Error: " + str(err))
            analog.deinit()
            digital.deinit()
            self.initialize()

if __name__ == "__main__":
    Detect().main()
