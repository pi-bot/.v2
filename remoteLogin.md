Change username
Set u Avahi

```sudo vim /etc/hosts```

Then: 
```sudo vim /etc/hostname```

```sudo insserv avahi-daemon```

```sudo pico /etc/avahi/services/multiple.service```


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
###KEy Pair Authentication 
Now that avahi is set up we want to trasfer our shh public key from the mbp to the Raspi. First lets make the dir and file to contain the key (it may already exist). This also gives us the opportunity to test avahi. From a mac terminal i type:
``` ssh pi@piBot5.local
```
Now that I'm in I can make the directory and file
```
mkdir .ssh
touch .ssh/authorized_keys
exit
```
Notice that I've exited the ssh session so I should now be in my mbp userspace. I can now transfer the key by: 

```
cat ~/.ssh/id_rsa.pub | ssh pi>@piBot5.local 'cat >> .ssh/authorized_keys'
```
This will ask for a password and then should complete the operation.  Now when I ssh in it should do so without requesting a password. Test:
```
ssh pi@piBot5.local
```
I'm in! Hooray!:)


###Burning the bootloader
```
sudo avrdude -p atmega328p -P /dev/ttyS0 -c arduino -b 115200 -D -U flash:w:/usr/share/arduino/hardware/arduino/bootloaders/atmega/ATmegaBOOT_168_atmega328.hex:i -vv
```
This seemed to brick the micro:(  I think the -D switch may not have been appropriate

```
-p <partno>                Required. Specify AVR device.
  -b <baudrate>              Override RS-232 baud rate.
  -c <programmer>            Specify programmer type.
  -D                         Disable auto erase for flash memory
  -i <delay>                 ISP Clock Delay [in microseconds]
  -U <memtype>:r|w|v:<filename>[:format]
                             Memory operation specification.
                             Multiple -U options are allowed, each request
  -v                         Verbose output. -v -v for more.
```
This gives us a modified version:
```
sudo avrdude -p atmega328p -P /dev/ttyS0 -c arduino -U flash:w:/usr/share/arduino/hardware/arduino/bootloaders/atmega/ATmegaBOOT_168_atmega328.hex -vv
```
This seemed to be correct in that it flashed the chip however it did brick it.:(
