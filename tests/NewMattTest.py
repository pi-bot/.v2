from pibot.arduino import Commands, Arduino
from pibot.motors import Motors
from pibot.mission import Mission
import time
board = Arduino()
board.connect()
move = Motors()
mission = Mission()
mission.startMission()

# each command will wait (block) until the robot has finished moving
# speed is the default speed
move.moveForward(20) # move forwards 20cm
move.moveBackward(20) # move backwards 20cm
move.turnLeft(90) # turn left 90 degrees
move.turnRight(90) # turn right 90 degrees
