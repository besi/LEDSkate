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
    print("Starting the WIFI...")
    import secrets
    wifi = network.WLAN(network.STA_IF)
    wifi.active(True)
    # Connect to the wifi (requires secrets.py to be present)
    wifi.connect(secrets.wifi.ssid, secrets.wifi.password)
    while not wifi.isconnected():
        utime.sleep(0.2)
    current_ip = wifi.ifconfig()[0]
    print("WIFI connected at %s" % current_ip)

    webrepl.start()
