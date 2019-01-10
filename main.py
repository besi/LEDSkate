import machine, neopixel
count = 80
np = neopixel.NeoPixel(machine.Pin(4), count)
np.write()
