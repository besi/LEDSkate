import time

import machine
import neopixel

change_rate = 1
led_count = 80
proximity_pin = 36
neopixel_pin = 4
led_pin = 5

led = machine.Pin(led_pin, machine.Pin.OUT)  # create output pin on GPIO0
np = neopixel.NeoPixel(machine.Pin(neopixel_pin), led_count, timing=True)
dummy_np = neopixel.NeoPixel(machine.Pin(neopixel_pin), led_count, timing=True)

proximity = machine.Pin(proximity_pin, machine.Pin.IN)
old_proximity = 1
offset = 0


def initialize_pixel(count, pixel):
    for k in range(count):
        x = k / (count)
        if 0 <= x < 1 / 3:
            r = (1 - x) * 3
            g = x * 3
            b = 0
        if 1 / 3 <= x < 2 / 3:
            x = x - 1 / 3
            g = (1 / 3 - x) * 3
            b = x * 3
            r = 0
        if 2 / 3 <= x:
            x = x - 2 / 3
            b = (1 / 3 - x) * 3
            r = x * 3
            g = 0

        gamma = 1 / 1.8
        r = r ** gamma
        g = g ** gamma
        b = b ** gamma

        pixel[k] = (int(r * 255), int(g * 255), int(b * 255))


colors = initialize_pixel(led_count, dummy_np)

while True:
    led.value(proximity.value())

    if proximity.value() == 0 and old_proximity == 1:
        offset += change_rate
        index = (offset % led_count) * np.bpp
        np.buf = dummy_np.buf[index:] + dummy_np.buf[:index]
        np.write()

    old_proximity = proximity.value()
    time.sleep(0.0025)
