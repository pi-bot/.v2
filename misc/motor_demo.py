from arduino import Commands, Arduino
from time import sleep
from motors import Motors
from mission import Mission
board = Arduino()
board.connect()
move = Motors()

mission = Mission()

power_f = 100
power_t = 100

mission.startMission()
while True:
        
	
	print("Forward") 
	move.forward(power_f)
	sleep(4)
	move.stop()

	print("turn left")
	move.leftMotor(power_f, 0)
	move.rightMotor(power_f, 1)
	sleep(1)
	move.stop()
	sleep(1)

	print("turn right")
	move.leftMotor(power_f, 1)
	move.rightMotor(power_f, 0)
	sleep(1)
	move.stop()
	sleep(1)
	
	print("Back")
	move.backward(power_f)
	sleep(4)
	move.stop()
	sleep(1)

	



