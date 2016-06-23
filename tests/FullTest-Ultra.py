from arduino import Commands, Arduino
from ultrasound import Ultrasound
from time import sleep
from mission import Mission

board = Arduino()
mission = Mission()

mission.waitForButton()
board.connect()
print("Board connected")
sleep(0.5)

del1 = 5
del2 = 3
speed = 50

ultra = Ultrasound()

mission.waitForButton()
while True:
    print("Getting ultrasound distance")
    distance = int(ultra.getDistance())
    print(distance)
    sleep(1)
    



