from machine import Pin
import time

p0 = Pin(5, Pin.OUT)    # create output pin on GPIO0
delay = 0.25
while True:
    p0.value(1)                 # set pin to "on" (high) level
    time.sleep(delay)
    p0.value(0)                # set pin to "off" (low) level
    time.sleep(delay)
