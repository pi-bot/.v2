from arduino import Commands, Arduino
from motors import Motors
from mission import Mission
import time
board = Arduino()
board.connect()
move = Motors()
mission = Mission()
mission.startMission()

# each command will wait (block) until the robot has finished moving
# speed is the default speed
move.moveForward(100) # move forwards 100cm
move.moveBackward(100) # move backwards 100cm
move.turnLeft(90) # turn left 90 degrees
move.turnRight(90) # turn right 90 degrees

# each command will block until robot has finished moving
# speed is the second argument
move.moveForward(100, speed=50) # move forwards 100cm
move.moveBackward(100, speed=50) # move backwards 100cm
move.turnLeft(90, speed=50) # turn left 90 degrees
move.turnRight(90, speed=50) # turn right 90 degrees

# advanced mode, drive and take samples at the same time
move.moveForward(100, speed=50, block=False) # start moving at 50 speed, don't block
# start a loop that keeps going until we arrive at the position
while not move.getAtPosition():
    # wait for a bit
    time.sleep(0.5) 
    # do something else, like take a sample
    rfid = mission.getLocation()
    sample = mission.takeSample(rfid)
    mission.saveData(sample)
