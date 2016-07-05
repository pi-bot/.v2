#!/bin/bash
# this is a bash file intended to be run to install all the dependecies for the PiBot Code base
# TBC

# Notes for you to get code working 
# On command line in robot update the Python path:

# First we clone the repo with 

git clone https://github.com/pi-bot/v2
# now we can udate the firmware
git clone -b callback https://github.com/pi-bot/v2
# The above is alternative branch
cd /home/pi/v2/arduino-firmware/
./upload.sh
#makesure the board power switch is on
#before we test we need to tell the system where the modules are:
echo "export PYTHONPATH=\$PYTHONPATH:~/v2/python-code" >> ~/.profile
# then update bash profile to implement the change ins PYTHONPATH
source ~/.profile
# Then we can test
cd /home/pi/v2/tests/
sudo python testAll.py
# may need to move a dependent file see below
#moving a file to work the mission module
mv /home/pi/v2/misc/sample_data.json /home/pi/v2/python-code/sample_data.json
# now this test will test all teh hardware.  For minicome to work :
cd ~/v2/arduino-firmware/src/sketch
nano sketch.ino
#now change debug line from false to true
# then repeat above steps to uploand the firmware
# then install mini com
sudo apt-get install -y minicom 
# then run it 
minicom  -b 115200 -o -D /dev/ttyAMA0
# To make things really easy why not add minicom and vnc to all the bots also make sure idle runs as root
#install vnc
sudo apt-get install  tightvncserver
#making vnc persistent
cd /home/pi/.config

mkdir /home/pi/.config/autostart

sudo vim /home/pi/.config/autostart/tightvnc.desktop

#Then add this in the file:

[Desktop Entry]
Type=Application
Name=TightVNC
Exec=vncserver :1
StartupNotify=false

#then reboot for changes to take effect

sudo reboot

# then connect from mac:

open vnc://192.168.0.13:5901

#general details for connecting to rebot over wireless
#network ssid and pw are stored here.  This is set up from desktop in a shell environment.
sudo cat /etc/wpa_supplicant/wpa_supplicant.conf

# error when we run the code:
pi@maven:~/pibot/tests $ python td2.py
connected
waiting for button...
waiting for desination
waiting for desination
waiting for desination
waiting for desination
waiting for desination
waiting for desination
waiting for desination
Traceback (most recent call last):
  File "td2.py", line 17, in <module>
    there=int(move.getAtPosition())
ValueError: invalid literal for int() with base 10: 'Reached position\r\n'

# This seems to be because after the position is reached the function move.getAtPosition() is returning 'Reached position\r\n' (as this is not an Int it is therefore throwing an error
#) This seems to me odd because 'Reached Position' is coming from the check checkPosReached(void)function in Movement.cpp. 
# I cant see where that is being called and why the print(L is being returned.)
