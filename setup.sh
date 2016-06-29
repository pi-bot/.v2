#!/bin/bash
# this is a bash file intended to be run to install all the dependecies for the PiBot Code base
# TBC

# Notes for you to get code working 
# On command line in robot update the Python path:
  
echo "export PYTHONPATH=$PYTHONPATH:~/v2/python-code" >> ~/.profile
# then update bash to implement the change ins PYTHONPATH
source ~/.profile
# now we can udate the firmware
cd /home/pi/v2/arduino-firmware/
./upload.sh
#makesure the board power switch is on
# Then we can test
cd /home/pi/v2/tests/
sudo python testAll.py
# may need to move a dependent file see below
#moving a file to work the mission module
mv /home/pi/v2/misc/sample_data.json /home/pi/v2/python-code/sample_data.json
# now this test will test all teh hardware.  For minicome to work :
