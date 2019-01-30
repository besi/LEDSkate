import time

import machine
import neopixel
import network

from microWebSrv import MicroWebSrv

change_rate = .9815
led_count = 80
sub_strip_count = 40

mode_switch_pin = 12
proximity_pin = 36
neopixel_pin = 4
led_pin = 5

led = machine.Pin(led_pin, machine.Pin.OUT)
np = neopixel.NeoPixel(machine.Pin(neopixel_pin), led_count, timing=True)
np_dummy = neopixel.NeoPixel(machine.Pin(neopixel_pin), led_count, timing=True)

proximity = machine.Pin(proximity_pin, machine.Pin.IN)
old_proximity = 1
offset = 1

mode_switch = machine.Pin(mode_switch_pin, machine.Pin.IN)

current_mode = 1
max_mode = 4

black_mode = lambda x: (0, 0, 0)

def disco_mode(x):
    if 0 <= x < 1 / 3:
        return (1, 0, 0)
    if 1 / 3 <= x < 2 / 3:
        return (0, 1, 0)
    if 2 / 3 <= x:
        return (0, 0, 1)


def rainbow_mode(x):
    r, g, b = 0, 0, 0
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
    return (r, g, b)


def disco_smooth_mode(x):
    r = max(0, 1 - abs(x - 1 / 6) * 6)
    g = max(0, 1 - abs(x - 3 / 6) * 6)
    b = max(0, 1 - abs(x - 5 / 6) * 6)
    return (r, g, b)


def initialize_pixel(count, pixel, mode):
    gamma = 1
    for k in range(count):
        r, g, b = (0, 0, 0)
        x = k / count
        if mode == 1:
            r, g, b = disco_mode(x)
            gamma = 1 / 1.8
        if mode == 2:
            r, g, b = rainbow_mode(x)
            gamma = 1 / 1.8
        if mode == 3:
            r, g, b = disco_smooth_mode(x)
            gamma = 1.6
        if mode == 4:
            # if followed by the cops
            r, g, b = black_mode(x)

        if gamma != 1:
            r = r ** gamma
            g = g ** gamma
            b = b ** gamma

        pixel[k] = (int(r * 255), int(g * 255), int(b * 255))


initialize_pixel(led_count, np_dummy, current_mode)
last_button = mode_switch.value()

wifi = network.WLAN(network.STA_IF)
ap = network.WLAN(network.AP_IF)


@MicroWebSrv.route('/mode')
def handlerFuncGet(httpClient, httpResponse):
    change_mode()
    httpResponse.WriteResponseOk(headers=None,
                                 contentType="text/html",
                                 contentCharset="UTF-8",
                                 content="HELLO HTTP")


def startWebserver():
    ip = wifi.ifconfig()[0] if wifi.active() else ap.ifconfig()[0]
    print('Starting Webserver at http://%s' % ip)
    mws = MicroWebSrv()
    mws.Start(threaded=True)


if wifi.active() or ap.active():
    startWebserver()


def updateStrip():
    global offset
    bytes = 3
    offset -= change_rate
    index = (int(offset) % led_count)
    idx_end = index + sub_strip_count
    if idx_end > led_count:
        idx_end = (idx_end - led_count)
        end_len = (led_count - index)
        np.buf[0:end_len * bytes] = np_dummy.buf[index * bytes:led_count * bytes]
        np.buf[end_len * bytes:sub_strip_count * bytes] = np_dummy.buf[0:(sub_strip_count - end_len) * bytes]
    else:
        np.buf[0:sub_strip_count * bytes] = np_dummy.buf[index * bytes:idx_end * bytes]

    for k in range(sub_strip_count):
        k3 = k * bytes
        np.buf[120 + k3:123 + k3] = np.buf[117 - k3:120 - k3]
    np.write()


def change_mode():
    global offset
    offset = 1
    global current_mode
    global max_mode
    old_mode = current_mode
    current_mode += 1
    if current_mode > max_mode:
        current_mode = 1
    print("Changed mode from %i to %i" % (old_mode, current_mode))
    initialize_pixel(led_count, np_dummy, current_mode)
    updateStrip()


while True:
    led.value(proximity.value())
    if last_button != mode_switch.value() and mode_switch.value() == 1:
        change_mode()

    last_button = mode_switch.value()

    if proximity.value() != old_proximity:
        updateStrip()
    old_proximity = proximity.value()
    time.sleep(0.0025)
