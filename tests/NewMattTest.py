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
move.moveForward(20) # move forwards 100cm
move.moveBackward(20) # move backwards 100cm
#move.turnLeft(90) # turn left 90 degrees
#move.turnRight(90) # turn right 90 degrees
