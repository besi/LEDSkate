# This file is executed on every boot (including wake-boot from deepsleep)
import esp
import machine
import network
import utime
import webrepl

esp.osdebug(None)

# Pressing the button during startup will enable the WIFI

utime.sleep(1)
enable_wifi = not machine.Pin(0, machine.Pin.IN).value()
current_ip = None

if enable_wifi:
    # Connect to the wifi (requires wifi.txt with "ssid:password" to be present)
    ssid, password = open('wifi.txt').read().split(':')
    wifi = network.WLAN(network.STA_IF)
    wifi.active(True)
    wifi.connect(ssid, password)
    while not wifi.isconnected():
        pass
    current_ip = wifi.ifconfig()[0]

    webrepl.start()


def timed_function(f, *args, **kwargs):
    def new_func(*args, **kwargs):
        t = utime.ticks_us()
        result = f(*args, **kwargs)
        delta = utime.ticks_diff(utime.ticks_us(), t)
        print('Function {} Time = {:6.3f}ms'.format(f.__name__, delta / 1000))
        return result

    return new_func
