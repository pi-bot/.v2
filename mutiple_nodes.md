
## About 
**pssh** can be used to control multiple robots in parrallel
avahi h is already installed on the Raspberry Pi's (This makes it possible to connect by systems hostnnames)
 make sure each node (or robot) has a unique host name that you know.  Steps for this are:
 ```
nano /etc/hostname
#change name 
nano /etc/hosts 
```

### change to hostname 
update with
```
sudo /etc/init.d/hostnames.sh
```
do the above command twice
then 
```
sudo reboot
```

ok now we can push our ssh public key to each node so ssh can be used without password authentication
**sh-copy-id** can be used for that (install if you don't have it)
```
ssh-copy-id pi@yulu.local
```
do this for each node.

Now we can use pssh:) First we need to install on your local system. 
On my MBP i did this with brew. when installed check details with:
```
pssh --help
```
This gives a list of arguments 
The key step is to make a file with the nodes listed e.g. a text file called **robots.txt** that is a list as follows:
```
pi@dawn.local
pi@sputnik.local 
etc 
```
Now we can use the list with pssh
```
pssh -P -h robots.txt -i "df -h"
```

say we want to install vim on each :
```
pssh -P -h robots.txt -o foo -i "sudo apt-get -y install vim "
```
Here is a collections of commands used to set up the robots:

```
pssh -P -h robots.txt -o foo -i "bash /home/pi/v2/arduino-firmware/upload.sh"
pssh -P -h robots.txt -o foo -i "mv /home/pi/v2/misc/sample_data.json /home/pi/v2/python-code/sample_data.json"
This took an age to get write with the escapes etc!
pssh -P -h robots.txt -o foo -i 'echo export PYTHONPATH=\$PYTHONPATH:\~/v2/python-code >> ~/.profile'
pssh -P -h robots.txt -o foo -i "cat ~/.profile"
```

I had to use this if there was an error
```
pssh -P -h robots.txt -o foo -i "head -n -1 ~/.profile > temp.txt ; mv temp.txt ~/.profile"
```

When you see its good you can add to bash
pssh -P -h robots.txt -o foo -i "source ~/.profile"
Now time to test!

```
pssh -P -h robots.txt -o foo -x -i "python trainingtest.py"
```
This is what I used before
```
cd ~/.v2 && git pull
```

pssh -P -h nodes.txt -i "cd ~/.v2 && git pull"


```
cd ~/.v2/arduino-firmware/ && ./upload.sh
```

```
python ~/.v2/tests/NewMattTest.py
```

```
pssh -P -h robots.txt -o foo -x "cd /home/pi/v2/tests/; bash" -i "python testAll.py"
```


