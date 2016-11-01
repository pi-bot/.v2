# Intro

This guide will:

1. Install the latest version of Raspbian and update
2. Install and configure **AVR dude** to communicate and test the PiBot board.
3. Give tips and hints on starting the learning

## 1 Install latest Raspian.
 The latest version is: **Raspian Jessie with Pixel**

- **Version**:September 2016
- **Release date**:2016-09-23
- **Kernel version**:4.4

[Here](https://www.raspberrypi.org/documentation/installation/installing-images/) is the official guide for installing images.

Once you have a working Raspian OS on the Raspberry Pi and a working network connection you can finish by udpdating the system with:
```
sudo apt-get update && sudo apt-get upgrade
```

The sofware that we use to learn programming and control the robot is a modified version of the **Arduino IDE**. The next step is to install this.  

```
sudo apt-get install arduino
```


## 2  Communicating with the PiBot Board

**avrdude** is a command-line interface for downloading and uploading to microcontrollers and enabling automation.  It has many features and is also used by the Arduiono IDE. See [here]( http://www.ladyada.net/learn/avr/avrdude.html) for a good overview:
We use it to automate the downloading and and uploading of code to the PiBot arduino compatible microcontroller (Atmel 328P)
This guide will help you:

- Configure your Raspberry Pi and Arduino IDE to work with the PiBot board (avrdude is included in the install)
- Configure the serial output of the Raspberry Pi to link with the Microcontroller (By default the linux kernal outputs to the Raspberry Pi's Serial port)
- Modify the setup with avrdude so that the Raspberry Pi can interface with it seamlessly (this involves setting up a unique reset pin instead of the typical reset pin normally used with arudinos)

** NB ** these setup instructions are different for the Raspberry Pi and other Pi versions.   Please look out for specific instructions relating to your speciific version.This set up is compatible with the new Raspain Jessie operating system only. 

OK here we go:


### Setting up the serial interface

By default kernal messages are sent to serial so the first step is to disable this.
For all Pi's apart from Pi 3 do:
```
sudo systemctl stop serial-getty@ttyAMA0.service
sudo systemctl disable serial-getty@ttyAMA0.service
```
If you have a Pi 3 you do the following instead (only do this if you have a Pi 3):
```
sudo systemctl stop serial-getty@ttyS0.service 
sudo systemctl disable serial-getty@ttyS0.service
```
Then add this line to the Raspberry Pi config file to enable serial on the GPIO pins:
```
sudo nano /boot/config.txt
```
add this line to the end:
```
enable_uart=1
```
### Edit cmdline.txt

Then we need to delete some data from the /boot/cmdline.txt file 
```
sudo nano /boot/cmdline.txt
```
remove the string 'console=serail0,115200'

###mapping
Then setup the mapping for linking the default arduiono serial interface with ours 
**N.B.** this step is not required for the Raspberry Pi 3 which already uses the arduino default.
```
sudo vim /etc/udev/rules.d/80-pibot.rules
```

### add these and close
KERNEL=="ttyAMA0", SYMLINK+="ttyS0",GROUP="dialout",MODE:=0666
KERNEL=="ttyACM0", SYMLINK+="ttyS1",GROUP="dialout",MODE:=0666

Now we need to alter the DTR reset pin for use with avrdude
many projects using the Raspberry Pi to program microcontrollers have used this approach
TO DO fork original files and include as PiBot install: (edit the autoreset file to include correct pin 7)
```
git clone  https://github.com/CisecoPlc/avrdude-rpi
cd avrdude-rpi
sudo cp autoreset /usr/bin
sudo cp avrdude-autoreset /usr/bin
sudo mv /usr/bin/avrdude /usr/bin/avrdude-original
sudo ln -s /usr/bin/avrdude-autoreset /usr/bin/avrdude
```

Then I am editing the /usr/bin/autoreset to use pin 7 instead and increase the time to 0.32.
:great then we can proceed to install the pibot firmware 
for the Raspberry Pi 3 the serial connection is given over /dev/ttyS0 
for all other raspberry pi's the connection is over /dev/ttyAMA0 

###Finally
I can add the Pibot as a board to be accessable from the arduiono IDE 

**The below did not work **
# following another guide we find that its should be is 
cd /usr/share/arduino/hardware/arduino
then instead edit the existing boards.txt to add the entry. 

```
mkdir /home/pi/sketchbook
mkdir /home/pi/sketchbook/hardware 
mkdir /home/pi/sketchbook/hardware/pi_bot
```

then create a board file in the pi_bot folder 
```
vim /home/pi/sketchbook/hardware/pi_bot/Boards.txt
```
```

##############################################################

pibot.name=Pi Bot

pibot.upload.protocol=arduino
pibot.upload.maximum_size=30720
pibot.upload.speed=57600

pibot.bootloader.low_fuses=0xFF
pibot.bootloader.high_fuses=0xDA
pibot.bootloader.extended_fuses=0x05
pibot.bootloader.path=arduino:atmega
pibot.bootloader.file=ATmegaBOOT_168_atmega328_pro_8MHz.hex
pibot.bootloader.unlock_bits=0x3F
pibot.bootloader.lock_bits=0x0F

pibot.build.mcu=atmega328p
pibot.build.f_cpu=8000000L
pibot.build.core=arduino:arduino
pibot.build.variant=arduino:standard

```
Reboot and the board should now be accessible in the dropdown menu in the IDE













