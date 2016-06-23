from arduino import Commands, Arduino
from time import sleep
from motors import Motors
from mission import Mission
board = Arduino()
board.connect()
move = Motors()
mission = Mission()

mission.startMission()
board.connect()
print("Board connected")
sleep(0.5)

del1 = 5  # This is standard delay 1 in seconds
del2 = 3  # This is standard delay 2 in seconds
speed = 50  # This takes a value from 0 to 254 

print("Will now go forward speed 50 for 1S")
sleep(0.8)
move.forward(50)
sleep(1)
move.stop()
print("Will now go backwards speed 50 for 1S")
sleep(1)
move.backward(50)
sleep(1)
move.stop()

print("robot will now move forward by 60 cm  on button press")
sleep(1)
mission.startMission()
sleep(1)
move.position(60,100)
sleep(5)
move.stop()

print("leftMotor(speed,direction) and rightMotor (speed,direction) on button press")
sleep(1)
mission.startMission()
sleep(1)
move.leftMotor(50,1)
sleep(1)
print("moving right motor now")
move.rightMotor(50,0)
sleep(1)
print("now both motors together  now")
move.rightMotor(50,1)
move.leftMotor(50, 1)
sleep(1)

move.stop()

print("Will now turn around like crazy on button press")
print("Robot will now rotate by minus 90 degrees")
mission.startMission()
move.rotate(-90,100)
sleep(4)
move.stop()
print("Will not disable the motors")
#move.disable() # did not like this spun into a loop
