LED Skate
=========

Connect via Serial

    picocom --baud 115200 /dev/cu.usbserial-DN02N1D8


Download and upload a file

    ampy --port /dev/cu.usbserial-DN02N1D8 get boot.py
    ampy --port /dev/cu.usbserial-DN02N1D8 put boot.py
    ampy --port /dev/cu.usbserial-DN02N1D8 ls



## Ideas

- Break light when negative acceleration is detected
- Turn indicator when curves are detected
- Remote control for special effects
- Auto Shut-off when the board is picked up
- Start a webserver using picoweb. See [picoweb#46](https://github.com/pfalcon/picoweb/issues/46)
