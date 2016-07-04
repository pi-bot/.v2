from arduino import Commands, Arduino
from time import sleep
from motors import Motors
from mission import Mission
board = Arduino()
board.connect()
move = Motors()
mission = Mission()
mission.startMission()

move.position(10,100)
there=int(move.getAtPosition())
#print(there)
while (there==0):
	print("waiting for desination")
	sleep(0.2)
	there=int(move.getAtPosition()) 

sleep(1)
print("Arrived there")
move.rotate(-90,100)
sleep(1)
move.position(-10,100)
