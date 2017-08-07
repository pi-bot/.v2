# Intro

This guide will:

1. Install the latest version of Raspbian and update
2. Set up networking to the Raspberry Pi for remote login over both a terminal interface (via SSH) and a remote desktop (via tightVNC).
3. Install and configure **AVR dude** to communicate and test the PiBot board.
4. Give tips and hints on starting the learning

## 1 Install latest Raspian.
 The latest version is: **Raspian Jessie with Pixel**

- **Version**:July 2017
- **Release date**:2017-07-05
- **Kernel version**:4.9

[Here](https://www.raspberrypi.org/documentation/installation/installing-images/) is the official guide for installing images.

Once you have a working Raspian OS on the Raspberry Pi and a working network connection you can finish by udpdating the system with:
```
sudo apt-get update && sudo apt-get upgrade
```

## 2 Remote User Interfacing with the Raspberry Pi 

The first thing to do is to set up a re

```
ssh-keygen -t rsa -C harry@Harrys-MacBook-Pro
```
You will then be given a prompt to save the generated keys. Save it in the default location (/home/pi/.ssh/id_rsa) by just hitting Enter.


cat ~/.ssh/id_rsa.pub | ssh <USERNAME>@<IP-ADDRESS> 'cat >> .ssh/authorized_keys'

cat ~/.ssh/id_rsa.pub | ssh pi@192.168.15.4 'cat >> .ssh/authorized_keys'


Remote desktop and command-line interfaces can be set up to access and control the Raspberry Pi remotely. This is the best way to control robots and means that we can eventually un-tether the system so that it can operate without any wire attachements whats-so-ever.  

### Remote Desktop
The Desktop interface of the Raspberry Pi can be accessed across a network by using a tecnhnology known as VNC (Virtual Network Computing).  In this example we will set up a VNC client on the Raspberry Pi's and access the desktops from an apple mac computer using its integrated remote desktop technology. Please see other guides for set up from windows and other linux machines ( https://www.raspberrypi.org/documentation/remote-access/vnc/

)   

Follow guide here:

https://www.raspberrypi.org/forums/viewtopic.php?t=123457


```
sudo apt-get install tightvncserver
```


3. Create a new file /etc/systemd/system/vncserver@.service with the following contents:

```
sudo vim /etc/systemd/system/vncserver@.service
```
Then put in the file: 

```
[Unit]
Description=Remote desktop service (VNC)
After=syslog.target network.target

[Service]
Type=forking
User=pi
PAMName=login
PIDFile=/home/pi/.vnc/%H:%i.pid
ExecStartPre=-/usr/bin/vncserver -kill :%i > /dev/null 2>&1
ExecStart=/usr/bin/vncserver -depth 24 -geometry 1280x800 :%i
ExecStop=/usr/bin/vncserver -kill :%i

[Install]
WantedBy=multi-user.target
```

By default a cross is shown in the remote desktop instead of a cursor.  This can be changed to the familiar arrow by changing a line in a vnc config. file: 

```
sudo vim ~/.vnc/xstartup
```

The line to change is:
```
xsetroot -solid grey -cursor_name left_ptr
```

OK now the services can be reloaded for the changes to take effect


```
sudo systemctl daemon-reload && sudo systemctl enable vncserver@1.service
sudo reboot
```



4. (Optional) Replace the parameters in the unit file, if you want to.
5. Run



### Remote Terminal Interface via SSH. 

See here:
https://www.raspberrypi.org/documentation/remote-access/ssh/passwordless.md




The sofware that we use to learn programming and control the robot is a modified version of the **Arduino IDE**. The next step is to install this.  

```
sudo apt-get install arduino
```

Then get avahi working and change the hostnames
 
 ```
 sudo vim /etc/hostname
```

and 
```
sudo vim /etc/hosts 
```


Change these and update by: 

```
sudo insserv avahi-daemon
```

```
sudo vim /etc/avahi/services/multiple.service
```

```
<?xml version="1.0" standalone='no'?>
<!DOCTYPE service-group SYSTEM "avahi-service.dtd">
<service-group>
        <name replace-wildcards="yes">%h</name>
        <service>
                <type>_device-info._tcp</type>
                <port>0</port>
                <txt-record>model=RackMac</txt-record>
        </service>
        <service>
                <type>_ssh._tcp</type>
                <port>22</port>
        </service>
</service-group>
```


The system can now be accessed acrossed the network without needing to know its IP address.  Therefore:
```
ssh pi@pibot-01.local
```
Works!





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













