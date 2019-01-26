import machine, neopixel
import time
import utime

change_rate = 1.963
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

        gamma = 1/1.8
        r = r ** gamma
        g = g ** gamma
        b = b ** gamma

        pixel[k] = (int(r * 255), int(g * 255), int(b * 255))

colors = initialize_pixel(led_count, dummy_np)
c=0
while True:
    led.value(proximity.value())

    if proximity.value() == 0 and old_proximity == 1:
        offset -= change_rate
        c += 1
        index = (int(offset) % led_count)
        idx_end = index + 40
        if idx_end > 80:
            idx_end = (idx_end-80)
            end_len = (80-index)
            print(c, index, idx_end, end_len)
            np.buf[0:end_len*3] = dummy_np.buf[index*3:80*3]
            np.buf[end_len*3:40*3] = dummy_np.buf[0:(40-end_len)*3]
        else:
            np.buf[0:40*3] = dummy_np.buf[index*3:idx_end*3]
            print(c, index)

        # not allowed in upy : -1 offset
        # np.buf[40*3:80*3] = np.buf[39*3::-1]

        for k in range(40):
            k3 = k*3
            np.buf[120+k3:123+k3] = np.buf[117-k3:120-k3]

        #for k in range(led_count):
        #    np[k] = colors[(k + offset) % led_count]

        np.write()

    old_proximity = proximity.value()
    time.sleep(0.0025)
