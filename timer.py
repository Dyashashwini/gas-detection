from machine import Pin, Timer
from time import sleep

# A simple display function for Testing
def display(info):
    print("Working")

# Initialize the timer with callback to display function and a period of 1 second
tim = Timer(4)
print("Starting")
tim.init(mode=Timer.PERIODIC, period=2000, callback=display)
sleep(15)
print("Stopping")
tim.deinit()