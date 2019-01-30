# This file is executed on every boot (including wake-boot from deepsleep)
import esp
import machine
import network
import utime

esp.osdebug(None)

# Pressing the button during startup will enable the WIFI
utime.sleep(.5)
enable_wifi = not machine.Pin(0, machine.Pin.IN).value()
current_ip = None

if enable_wifi:
    import secrets

    print("Starting the WIFI...")
    wifi = network.WLAN(network.STA_IF)
    wifi.active(True)
    wifi.connect(secrets.wifi.ssid, secrets.wifi.password)
    while not wifi.isconnected():
        machine.idle()
    current_ip = wifi.ifconfig()[0]
    print("WIFI connected at %s" % current_ip)
