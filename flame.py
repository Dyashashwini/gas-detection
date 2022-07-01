# Importing required Modules
from machine import Pin
from time import sleep

flame = Pin(4, Pin.IN) # D2
led = Pin(2, Pin.OUT) # D4
led.value(1) # Led Off


# Forever Loop
while True:
    # Reading flame sensor pin value
    flame_value = flame.value()
    # Checking the flame sensor pin value
    if flame_value == 0:
        # turning led on and displaying appropriate message.
        print("Flame Detected!")
        led.value(0)
    else:
        led.value(1)
    # Putting to sleep for 1 second
    sleep(1)