LED Skate
=========

![glow](http://res.cloudinary.com/mediacloud/image/upload/v1547704870/pqiinxky4pwugkchjsbx.jpg)

This is a glowing skateboard that animates colors underneath the board in relation to the speed of the board.


Setup
-----

- Setup your Micropython device such as an ESP32
- Upload `secrets.py` to the device if you want to use the WIFI
- Press the button (Pin 0) on your device within one second after reset to enable the WIFI


Development
-----------

Connect via Serial

    # brew install picocom
    picocom --baud 115200 /dev/cu.usbserial-DN02N1D8
    
    # On mac OS
    screen /dev/cu.usbserial-DN02N1D8 115200

Download and upload a file

    ampy --port /dev/cu.usbserial-DN02N1D8 get boot.py
    ampy --port /dev/cu.usbserial-DN02N1D8 put boot.py
    ampy --port /dev/cu.usbserial-DN02N1D8 ls


Ideas
-----

- Break light when negative acceleration is detected
- Turn indicator when curves are detected
- Remote control for special effects
- Auto Shut-off when the board is picked up
