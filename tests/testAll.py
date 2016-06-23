import time
from arduino import Commands, Arduino
from ultrasound import Ultrasound
from time import sleep
from motors import Motors
from mission import Mission
import RPi.GPIO as GPIO
import picamera
RED_LED_GPIO = 26
GREEN_LED_GPIO = 29
BUTTON = 36

GPIO.setmode(GPIO.BOARD)
board = Arduino()
move = Motors()
mission = Mission()

#variables to be set up for the test
power_f = 90
power_t = 90
del1 = 5
del2 = 3
speed = 50


def buttonWait():
	GPIO.output(GREEN_LED_GPIO,False)
	GPIO.output(RED_LED_GPIO,True)
	print("waiting for button...")
	while GPIO.input(BUTTON) == False:
		time.sleep(0.1)
	GPIO.output(RED_LED_GPIO,False)

print("Will now go through full hardware tests")
buttonWait()
board.connect()
print("Board connected")
sleep(0.5)

print "Now Testing Movement"
move.forward(power_f)
sleep(1.5)
move.stop()

sleep(2)    

print "Now Testing Camera"
buttonWait()
with picamera.PiCamera() as camera:
	camera.resolution = (1024,768)
	camera.capture("testCam1.jpg")
	print "successfully captured image testCam1.jpg ...please check!"

print "Now Testing RFID"
buttonWait()
mission.deleteData()
location=mission.getLocation()
sample=mission.takeSample(location)
mission.saveData(sample)

print "Now Testing Ultrasound"
buttonWait()
print("Getting ultrasound distance")
ultra=Ultrasound()
print(ultra.getDistance())

print "Now Testing Up and down camera tilt"
buttonWait()
#put code in here to test the servo


print "Testing now COMPLETE"
mission.endMission()
