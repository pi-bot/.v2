
#The code repo for the Earth 2 Mars robots for @Bristol 

Instructions for getting code working on all robots.

##1. Download Repo.

First delete the old repo:

```
sudo rm -rf ~/v2
```
Now install the new repo:
```
git clone https://github.com/pi-bot/.v2
```
OK now we can place the python code deep into the system:

```
sudo mv .v/python-code  /usr/lib/python2.7/pibot
```
Now we must call modules in all python using a **pibot.modulename** convention.

Any questions/comments email **harry@pibot.org**

See License for details of copying and using the code.
