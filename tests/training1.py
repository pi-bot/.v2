# these 3 lines import some libraries that the software uses
from pibot.arduino import Arduino
from pibot.motors import Motors
from time import sleep

# these 3 lines get the robot setup and ready to go
board = Arduino()
board.connect()
move = Motors()

# the rest of the program shows how to move the robot around
print("forward")
move.moveForward(50) # 50 is the distance in cm
sleep(4) # 4 is the number of seconds to wait
move.stop()

sleep(1)

print("backward")
move.moveBackward(50)
sleep(4)
move.stop()
