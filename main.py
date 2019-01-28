import time

import machine
import neopixel

change_rate = .9815
led_count = 80
sub_strip_count = 40
proximity_pin = 36
neopixel_pin = 4
led_pin = 5

led = machine.Pin(led_pin, machine.Pin.OUT)
np = neopixel.NeoPixel(machine.Pin(neopixel_pin), led_count, timing=True)
np_dummy = neopixel.NeoPixel(machine.Pin(neopixel_pin), led_count, timing=True)

proximity = machine.Pin(proximity_pin, machine.Pin.IN)
old_proximity = 1
offset = 0

button = machine.Pin(0)

current_mode = 4
max_mode = 4


def initialize_pixel(count, pixel, mode):
    gamma = 1
    for k in range(count):
        x = k / count
        if mode == 1:
            if 0 <= x < 1 / 3:
                r = 1
                g = 0
                b = 0
            if 1 / 3 <= x < 2 / 3:
                r = 0
                g = 1
                b = 0
            if 2 / 3 <= x:
                r = 0
                g = 0
                b = 1
            gamma = 1 / 1.8

        if mode == 2:
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

        if mode == 3:
            r = max(0, 1 - abs(x - 1 / 6) * 6)
            g = max(0, 1 - abs(x - 3 / 6) * 6)
            b = max(0, 1 - abs(x - 5 / 6) * 6)
            gamma = 1

        if mode == 4:
            r = max(0, 1 - abs(x - 1 / 6) * 6)
            g = max(0, 1 - abs(x - 3 / 6) * 6)
            b = max(0, 1 - abs(x - 5 / 6) * 6)
            gamma = 1.6

        r = r ** gamma
        g = g ** gamma
        b = b ** gamma

        pixel[k] = (int(r * 255), int(g * 255), int(b * 255))


initialize_pixel(led_count, np_dummy, current_mode)
c = 0
last_button = button.value()

while True:
    led.value(proximity.value())

    if last_button != button.value() and button.value() == 0:
        current_mode += 1
        if current_mode > max_mode:
            current_mode = 1
        initialize_pixel(led_count, np_dummy, current_mode)

    last_button = button.value()

    if proximity.value() != old_proximity:
        bytes = 3
        offset -= change_rate
        c += 1
        index = (int(offset) % led_count)
        idx_end = index + sub_strip_count
        if idx_end > led_count:
            idx_end = (idx_end - led_count)
            end_len = (led_count - index)
            print(c, index, idx_end, end_len)
            np.buf[0:end_len * bytes] = np_dummy.buf[index * bytes:led_count * bytes]
            np.buf[end_len * bytes:sub_strip_count * bytes] = np_dummy.buf[0:(sub_strip_count - end_len) * bytes]
        else:
            np.buf[0:sub_strip_count * bytes] = np_dummy.buf[index * bytes:idx_end * bytes]
            print(c, index)

        for k in range(sub_strip_count):
            k3 = k * bytes
            np.buf[120 + k3:123 + k3] = np.buf[117 - k3:120 - k3]
        np.write()

    old_proximity = proximity.value()
    time.sleep(0.0025)
