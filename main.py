import machine, neopixel
import time
count = 80
proximity_pin = 36
neopixel_pin = 4
led_pin = 5

led = machine.Pin(led_pin, machine.Pin.OUT)    # create output pin on GPIO0
np = neopixel.NeoPixel(machine.Pin(neopixel_pin), count, timing=True)

proximity = machine.Pin(proximity_pin, machine.Pin.IN)
old_proximity = 1
o = 0
while True:
    led.value(proximity.value())
    if proximity.value() == 0 and old_proximity == 1:

        o += 1
        print(o)
        for k in range(count):
            i = (k+o) % count
            np[k] = ((i*1), 255 - i*13, 255 - i*6)
        np.write()
    old_proximity = proximity.value()
    time.sleep(0.01)
