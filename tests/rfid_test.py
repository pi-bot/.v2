from arduino import Commands, Arduino
from time import sleep
from motors import Motors
from mission import Mission

mission = Mission()
board = Arduino()
board.connect()
move = Motors()

print("ok")

move.stop()
sleep(2)
print("sampling")
location = mission.getLocation()
sample = mission.takeSample(location)

print(sample)

mission.endMission()
