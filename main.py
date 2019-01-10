import machine, neopixel
count = 80
np = neopixel.NeoPixel(machine.Pin(4), count, timing=True)
np.write()
