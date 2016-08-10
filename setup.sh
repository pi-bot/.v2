#!/bin/bash
# this is a bash file intended to be run to install all the dependecies for the PiBot Code base
# For now its a collection of steps to help get this set up.  Will probably make sense to core team only.
# TBC

#steps for successfull set up of Arduino IDE connected to the PiBoard and python libraries
# Step 1 download and burn latest Raspian image to SD card  (may 27 2016)
# Step 2 connect sd card to Raspberry PI v3 with monitor, keyboard, and ethernet (ie internet)
# Step 3 update the OS
# boot and then open termainal
# Step 4 update the OS:
sudo apt-get update 
sudo apt-get upgrade 
# need this to get seriel interface with the pi
#http://spellfoundry.com/sleepy-pi/setting-arduino-ide-raspbian/
# Step 5 
replace hostname automatically 
sudo sed -i -- 's/raspberrypi/bot7/g' /etc/hosts; sudo sed -i -- 's/raspberrypi/bot7/g' /etc/hostname
#alternatively this can be done manually ( I like to use vim)
sudo apt-get install vim -y 

# replace raspberry with the name of your choosing:
sudo vim /etc/hosts 
sudo vim /etc/hostname
# then implement:
sudo /etc/init.d/hostname.sh; sudo reboot

# install arduino and dependencies
sudo apt-get install arduino

#Arduino IDE does not recognise this port. It prefers to use /dev/ttyS0. 
#To get round this we link /dev/ttyS0 to /dev/ttyAMA0 and make sure this link is permanent. 
#To do this, we need to create a file called /etc/udev/rules.d/99-tty.rules using a text editor.

# We communicate and program the PiBots microchip overseriel.  
# To do this we need to set up the 
# 1 disable normal output to serial:


sudo systemctl stop serial-getty@ttyS0.service
sudo systemctl disable serial-getty@ttyS0.service
# now we configure the pi with :
sudo vim /boot/config.txt
# to the end of the file add:
enable_uart=1
# we also need to update the /boot/
sudo vim /boot/cmdline.txt
# remove console=serail0,115200

# alternatively this can be done through raspberry config.
#Please verify this works the same . (best to ingnore for now!)
sudo raspi-config
# 9 advanced options
# A7 Serial Enable/Disable shell and kernal messages over serial
# Would you like a login shell to be accessible oer serial?
# NO  

# The next step is to rename the serial device name for arduiono
# this is not neccessary for Raspberry Pi 3.
#apparently this is not true for the raspberry pi 3 so this is not required:

#
sudo vim /etc/udev/rules.d/99-tty.rules
# Add this 
KERNEL==”ttyAMA0″,SYMLINK+=”ttyS0″ GROUP=”dialout”
KERNEL==”ttyACM0″,SYMLINK+=”ttyS1″ GROUP=”dialout”
# then reboot 
sudo reboot


# this is what I did for RPI3:
sudo systemctl stop serial-getty@ttyS0.service 
sudo systemctl disable serial-getty@ttyS0.service
# also in Jessie enable uart
sudo vim /boot/config.txt
# then add:
enable_uart=1
# When Raspbian boots up it outputs boot information to the serial port
# To disable this we need to edit the /boot/cmdline.txt
sudo vim /boot/cmdline.txt

# update avr dude so we can use a GPIO pin for reset

# /dev/ttyS0
# No such file or directory avrdude-original done.  Thank you.

git clone  https://github.com/CisecoPlc/avrdude-rpi

cd avrdude-rpi
sudo cp autoreset /usr/bin
sudo cp avrdude-autoreset /usr/bin
sudo mv /usr/bin/avrdude /usr/bin/avrdude-original
sudo ln -s /usr/bin/avrdude-autoreset /usr/bin/avrdude

# Just to be sure everything is as it should be open the file /usr/bin/autoreset and look at line 15. It should look like this:
sudo vim /usr/bin/autoreset

#Change line 15 to :
     pin = 7

# currently issues here so chcking Jasons version!UPDATE pin number 7 works on Pi 2
# BUT !! Pin 4 works for RASPI Pi 4 makes no sense!?

# The above did not work so trying another way from Adafruit
sudo rm /usr/bin/autoreset ; sudo rm /usr/bin/avrdude-autoreset
sudo mv  /usr/bin/avrdude-original /usr/bin/avrdude


# now install ino to push firmware to Atmega328P
sudo pip install ino


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
# Final question is how do we find the right settings for the PID 
# values I've tried 2,0,2,0 this does not respond 
# values 9, 0.4, 0.3 seem to be better but not perfect. 
# How do we find the perfect solutions?
#First tune P and D 
#Set all to Zero and increase P by 0.5 ~ 1 untill it overshoots 
#Then up D by ~0.1 untill it doesn't over shoot any more
#Record the values and then repeat the cycle of upping P untill it over shoots again
#and D intill it counters that.
#You'll do this to the point where it doesn't improve
#Go back to where it was most optimal
#Then add some I to compensate uphill/downhill and do this ~0.1
# Now test all bots!
sudo rm -rf v2
git clone -b callback https://github.com/pi-bot/v2
cd ~/v2/arduino-firmware/ ;./upload.sh
python ~/v2/tests/td2.py
