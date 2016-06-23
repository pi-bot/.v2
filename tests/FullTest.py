from arduino import Commands, Arduino
from ultrasound import Ultrasound
from time import sleep
from motors import Motors
from mission import Mission
import picamera


board = Arduino()
move = Motors()
mission = Mission()
power_f = 90
power_t = 90


mission.waitForButton()
board.connect()
print("Board connected")
sleep(0.5)

del1 = 5
del2 = 3
speed = 50


while True:
    print "Now Testing Movement"
    move.forward(power_f)
    sleep(1.5)
    move.stop()

    sleep(2)    

    
    mission.waitForButton()
    print "Now Testing Camera"
    with picamera.PiCamera() as camera:
        camera.resolution = (1024,768)
        camera.capture("testCam1.jpg")

    mission.waitForButton()
    print "Now Testing RFID"
    mission.deleteData()
    location=mission.getLocation()
    sample=mission.takeSample(location)
    mission.saveData(sample)

    mission.waitForButton()
    print "Now Testing Ultrasound"

    mission.waitForButton()
    print("Getting ultrasound distance")
    ultra=Ultrasound()
    print(ultra.getDistance())

    mission.endMission()
    break
