#! /bin/bash
# Script must be run as sudo fail if not.



REVISION="$(cat /proc/cpuinfo | grep 'Revision' | awk '{print $3}' | sed 's/^1000//')"
SERIAL="$(cat /proc/cpuinfo | grep Serial | cut -d ':' -f 2)"
if [ "$REVISION" = "a02082" ]
then
  echo $REVISION
  echo "Board is Raspberry Pi version 3. Serial number is:"
  echo  $SERIAL
  echo "Will now configure the board Serial Interface:"
echo "stopping serial services"
  systemctl stop serial-getty@ttyS0.service
  systemctl disable serial-getty@ttyS0.service
  echo "adding lines to config.txt file"
  echo "enable_uart=1" >> /boot/config.txt
  echo "editing cmdline.txt."
  sed -e "s/console=serial0,115200//g" -i /boot/cmdline.txt
  echo "downloading and installing modified avrdude script"
  cd /tmp
  git clone  https://github.com/CisecoPlc/avrdude-rpi
  cd avrdude-rpi
  cp autoreset /usr/bin
  cp avrdude-autoreset /usr/bin
  mv /usr/bin/avrdude /usr/bin/avrdude-original
  ln -s /usr/bin/avrdude-autoreset /usr/bin/avrdude
#  cd ../
#  rm -rf avrdude-rpi
  echo "now changing the reset pin to 07 and altering timings to 0.32 s"
  sed -e "s/pin = 22/pin = 7/g" -i /usr/bin/autoreset
  sed -e "s/time.sleep(0.12)/time.sleep(0.32)/g" -i /usr/bin/autoreset
  echo "avrdude customisation complete. Now setting up the boards.txt"
  wget https://github.com/pi-bot/.v2/blob/master/boards.txt
  wget https://github.com/pi-bot/.v2/blob/master/programmers.txt
  mv programmers.txt programmers.txt.bak
  cd /usr/share/arduino/hardware/arduino
  mv boards.txt boards.txt.bak
  mv /tmp/boards.txt .
  mv programmers.txt programmers.txt.bak
  mv /tmp/programmers.txt .
  echo "Setup complete now. Launch the Arduino IDE and check that you can use it."
else 
  echo $REVISION
  echo  $SERIAL
fi
