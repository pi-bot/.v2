
## About 
**pssh** or **parallel SSH** can be used to control multiple systems at the same time.

See [pssh(1) - Linux man page](http://linux.die.net/man/1/pssh) for full details.
This guide covers the steps to get *pssh* up and running with a group of PiBots. 


SSH is installed on the Raspberry Pi's by default and we can implement a few other recommended steps:

####Using hotnames to connect over the network
 
**avahi** makes it possible to connect overnetworks by systems hostnnames and is already installed on the Raspberry Pi's.This is usefull as it means you can use **ssh** without needing to know the sytems I address. Instead of :
```
ssh pi@192.168.0.21
```
For example you can instead connect by:
```
ssh pi@raspberrypi.local 
```

####Give each robot a unique ID

Instead of the default hosname of **raspberrypi** it can be beneficial to have unique hostnames for each system.
This is perhaps the most time consuming part.(See future steps for way of automating). 

 Steps for changing the **hostname** are:
 
 The hostname is declared in two system files that will require editing.  These are:
 
 
 ```
/etc/hostname
```

and 
```
/etc/hosts 
```
Change these and update by: 

```
sudo /etc/init.d/hostnames.sh
```
then 
```
sudo reboot
```

####Removing the need for passwords
ok now we can push our ssh public key to each node so ssh can be used without password authentication
**sh-copy-id** can be used for that (install if you don't have it)
```
ssh-copy-id pi@yulu.local
```
do this for each node.

###Using PSSH 
Now we can use pssh:) First we need to install on your local system. 
On my MBP i did this with brew. when installed check details with:
```
pssh --help
```
This gives a list of arguments (otherwise known as options)
The key step is to make a file with the nodes listed e.g. a text file called **nodes.txt** that is a list as follows:
```
pi@dawn.local
pi@sputnik.local 
etc 
```
Now we can use the list with pssh
```
pssh -P -h nodes.txt -i "df -h"
```

The options we are using are:

- **-P** from the manual : **Print** Display output as it arrives. This option is of limited usefulness because output from different hosts are interleaved.
- **- h** - takes a host file that indicates the hosts. Requires hostfile nam/url (in our case nodes.txt)
- **-i**  from the manual : **Inline** Display standard output and standard error as each host completes.

#####Other useful options
Other options that have been used are:

- **-o** from the manual : **Outdir** Save standard output to files in the given directory. Filenames are of the form [user@]host[:port][.num] where the user and port are only included for hosts that explicitly specify them. The number is a counter that is incremented each time for hosts that are specified more than once.
- **-x** from the manual : **extra-args** Passes extra SSH command-line arguments (see the ssh(1) man page for more information about SSH arguments). This option may be specified multiple times. The arguments are processed to split on whitespace, protect text within quotes, and escape with backslashes. To pass arguments without such processing, use the -X option instead.

Following the options the command is finally declared within the parethesis. 

####Examples 

say we want to install vim on each :
```
pssh -P -h robots.txt -o foo -i "sudo apt-get -y install vim "
```
Here is a collections of commands used to set up the robots:

```
pssh -P -h robots.txt -o foo -i "bash /home/pi/v2/arduino-firmware/upload.sh"
pssh -P -h robots.txt -o foo -i "mv /home/pi/v2/misc/sample_data.json /home/pi/v2/python-code/sample_data.json"
```

This took an age to get write with the escapes etc!
```
pssh -P -h robots.txt -o foo -i 'echo export PYTHONPATH=\$PYTHONPATH:\~/v2/python-code >> ~/.profile'
pssh -P -h robots.txt -o foo -i "cat ~/.profile"
```

I had to use this if there was an error
```
pssh -P -h robots.txt -o foo -i "head -n -1 ~/.profile > temp.txt ; mv temp.txt ~/.profile"
```
When you see its good you can add to bash
```
pssh -P -h robots.txt -o foo -i "source ~/.profile"
```

###Testing 

Now time to test!

```
pssh -P -h robots.txt -i "python trainingtest.py"
```
This is what I used to update the repo on each system:
```
pssh -P -h nodes.txt -i "cd ~/.v2 && git pull"
```
Now we can reflash the firmware on each: 

```
pssh -P -h nodes.txt -i "cd ~/.v2/arduino-firmware/ && ./upload.sh"
```
Finally we can test each systems movement by: 
```
pssh -P -h nodes.txt -i "python ~/.v2/tests/NewMattTest.py"
```
Heres an example using the -x option with an additional step:
```
pssh -P -h robots.txt -o foo -x "cd /home/pi/v2/tests/; bash" -i "python testAll.py"
```


