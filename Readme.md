LED Skate
=========

Connect via Serial

    picocom --baud 115200 /dev/cu.usbserial-DN02N1D8


Download and upload a file

    ampy --port /dev/cu.usbserial-DN02N1D8 get boot.py
    ampy --port /dev/cu.usbserial-DN02N1D8 put boot.py
    ampy --port /dev/cu.usbserial-DN02N1D8 ls
