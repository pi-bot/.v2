It is possible to run the Atmel 328P microcontroller at various frequencies.  The datasheet recommends maximum limits for this depending on the voltage given to the system. Most arduino systems are run at 5V and at a frequency of 16Mhz and by default the firmware, libraries, and software operate at this frequency by default.

##3.3V @ 12MHz
The new pibot version has dropped the voltage of the micro to 3.3v to give better compatibility with the raspberry pi as well as the trend of 3.3v for new sensors.  The data sheet suggests that at 3.3V 12Mhz is an appropriate maximum speed.  This said, several products are running the Atmel 328p at 16Mhz on 3.3v like the Seeeduino 4.2.  It will be therefore easiest if we try and run at this speed.


##Running at 12Mhz 
To operate at 12MHz a few changes need to be made
-bootloader
-Boards.txt
-SoftwareSerial.cpp

###bootloader
See [here](http://ceptimus.co.uk/?p=102) for details of changes to the bootloader

###Boards.txt
There are a couple of changes to be made here : **/usr/share/arduino/hardware/arduino/boards.txt**

```
sudo vim /usr/share/arduino/hardware/arduino/boards.txt
```
 Then

```
atmega328bb12.bootloader.file=optiboot_atmega328_12.hex
atmega328bb12.build.f_cpu=12000000L
```

###SoftwareSerial.cpp
The file is found **/usr/share/arduino/libraries/SoftwareSerial/SoftwareSerial.cpp**

The Software Serial Library is one that does not have support for 12Mhz operation by default it can be added by add the following before **#elif F_CPU == 8000000** in the code about line 128:

```
sudo vim /usr/share/arduino/libraries/SoftwareSerial/SoftwareSerial.cp
```

Then 
```
#elif F_CPU == 12000000
static const DELAY_TABLE PROGMEM table[] =
{
// baud rxcenter rxintra rxstop tx
  { 115200, 1, 11, 11, 8, },
  { 57600, 6, 26, 26, 23, },
  { 38400, 14, 41, 42, 39, },
  { 31250, 19, 51, 52, 49, },
  { 28800, 23, 56, 56, 53, },
  { 19200, 37, 86, 86, 83, },
  { 14400, 52, 116, 116, 113, },
  { 9600, 82, 175, 175, 173, },
  { 4800, 172, 354, 354, 351, },
  { 2400, 350, 711, 711, 708, },
  { 1200, 707, 1425, 1425, 1422, },
  { 300, 2850, 5711, 5711, 5708, },
};
 
const int XMIT_START_ADJUSTMENT = 5;
```

N.B. I'm still getting timeouts when trying to upload a sketch so I will investigate this further now.

