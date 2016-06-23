# these 3 lines import some libraries that the software uses
from arduino import Arduino
from motors import Motors
from time import sleep

# these 3 lines get the robot setup and ready to go
board = Arduino()
board.connect()
move = Motors()

# the rest of the program shows how to move the robot around
print("turn Left")
move.turnLeft(90) # 90 is the angle in degree
sleep(3) # 3 is the number of seconds to wait
move.stop()

sleep(1)


print("turn Right")
move.turnRight(90)
sleep(3)
move.stop()
