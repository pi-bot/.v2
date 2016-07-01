#!/bin/bash
# this is a bash file intended to be run to install all the dependecies for the PiBot Code base
# TBC

# Notes for you to get code working 
# On command line in robot update the Python path:

# First we clone the repo with 

git clone https://github.com/pi-bot/v2
# now we can udate the firmware
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
