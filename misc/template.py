# these 4 lines import some libraries that the software uses
from pibot.arduino import Arduino
from pibot.motors import Motors
from pibot.mission import Mission
from time import sleep

# these 4 lines get the robot setup and ready to go
board = Arduino()
board.connect()
move = Motors()
mission = Mission()
