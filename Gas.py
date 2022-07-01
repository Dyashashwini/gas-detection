from machine import Pin, ADC
from time import sleep

# Declare the Sensor Pin for MQ-2 Sensor as Input
gas_analog = ADC(0)
gas_digital = Pin(5, Pin.IN)
led = Pin(2, Pin.OUT)
led.value(1)

try:
    while True:
        dgas_value = gas_digital.value()
        agas_value = gas_analog.read()
        # Print the sensor value
        print("Analog Value: " + str(agas_value))
        print("Digital Value: " + str(dgas_value))
        if dgas_value == 0 or agas_value > 500:
            print("Gas Leak Detected")
            led.value(0)
        else:
            led.value(1)
        # Delay next reading for 2 seconds
        sleep(1)
except Exception as e:
    print("Error: " + str(e))

### Output:
# Analog Value: 480
# Digital Value: 1
# Analog Value: 459
# Digital Value: 1
# Analog Value: 500
# Digital Value: 0
# Gas Leak Detected
# Analog Value: 499
# Digital Value: 0
# Gas Leak Detected
# Analog Value: 442
# Digital Value: 1
# Analog Value: 517
# Digital Value: 0
# Gas Leak Detected
# Analog Value: 561
# Digital Value: 0
# Gas Leak Detected
# Analog Value: 580
# Digital Value: 0
# Gas Leak Detected
# Analog Value: 582
# Digital Value: 0
# Gas Leak Detected
# Analog Value: 566
# Digital Value: 0
# Gas Leak Detected
# Analog Value: 556
# Digital Value: 0
# Gas Leak Detected
# Analog Value: 590
# Digital Value: 0
# Gas Leak Detected
# Analog Value: 606
# Digital Value: 0
# Gas Leak Detected
# Analog Value: 610
# Digital Value: 0
# Gas Leak Detected
# Analog Value: 562
# Digital Value: 0
# Gas Leak Detected
# Analog Value: 466
# Digital Value: 1
# Analog Value: 424
# Digital Value: 1