#!/bin/bash
# this is a bash file intended to be run to install all the dependecies for the PiBot Code base
# TBC
echo "export PYTHONPATH=$PYTHONPATH:~/v2/python-code" >> ~/.profile
source ~/.profile
mv /home/pi/v2/misc/sample_data.json /home/pi/v2/python-code/sample_data.json
