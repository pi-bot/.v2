
#The code repo for the Earth 2 Mars robots for @Bristol 

Instructions for getting code working on all robots.

##1 Download Repo

First delete the old repo and pibot folder:

```
sudo rm -rf ~/v2 ~/pibot 
```
Now install the new repo:
```
git clone https://github.com/pi-bot/.v2
```


##2 Update the firmware
This pushes the fixed code to the microcontroller:
```
cd ~/.v2/arduino-firmware 
./upload.sh
```
Messages onscreen will show that this is successfull

##3 Install the python modules
OK now we can place the python code deep into the system:

```
sudo mkdir /usr/lib/python2.7/pibot
sudo cp ~/.v2/python-code/*  /usr/lib/python2.7/pibot/
```
Now we must call modules in all python using a **pibot.modulename** convention.

##4 Use the new movement functions

The new movement functions are demonstrated in a new test:

```
cd ~/.v2/tests
python NewMattTest.py
```
All documents and test codes can now be updated! 

Any questions/comments email **harry@pibot.org**

See License for details of copying and using the code.
