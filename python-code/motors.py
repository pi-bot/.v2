#
#  	New version for "PiBot v8.0" With improved motor control IC DRV8835
#	also updated with new pin definitions for new PCB
#
#		by Jason 10/05/2016
#

import arduino
from arduino import Commands
from arduino import Arduino
from time import sleep

LEFT_MOTOR_DIRECTION = 6   # Direction bit
LEFT_MOTOR_SPEED =10 	   #PWM speed control
RIGHT_MOTOR_DIRECTION = 5  # Direction bit
RIGHT_MOTOR_SPEED = 9      # PWM speed control
MOTOR_MODE = 7	    	   #Enable motor controller

DEFAULT_SPEED = 50

class Motors():
    def __init__(self):
        self.board = Arduino()
        self.board.connect()

    def enable(self):
        self.board.sendCommand(Commands.WRITE_DIGITAL,7,1)	# puts motor drive into Phase/Enable mode

    def disable(self):
        self.board.sendCommand(Commands.WRITE_DIGITAL,7,0)# puts motor drive into IN/IN mode

    def forward(self, speed):
        self.enable()
        commandL = self.speedToCommand(speed)
        commandR = self.speedToCommand(speed)
        self.board.sendCommand(Commands.WRITE_DIGITAL,LEFT_MOTOR_DIRECTION,1)
        self.board.sendCommand(Commands.WRITE_DIGITAL,RIGHT_MOTOR_DIRECTION,0)
        self.board.sendCommand(Commands.WRITE_PWM,LEFT_MOTOR_SPEED,commandR)
        self.board.sendCommand(Commands.WRITE_PWM,RIGHT_MOTOR_SPEED,commandL)


    def getLeft(self):
	value = self.board.sendCommand(Commands.READ_LEFT_ENCODER,0,0)
	return value

    def getRight(self):
	value = self.board.sendCommand(Commands.READ_RIGHT_ENCODER,0,0)
	return value

    def getRightDistance(self):
        value = self.board.sendCommand(Commands.READ_RIGHT_DISTANCE,0,0)
	return value
    def getLeftDistance(self):
        value = self.board.sendCommand(Commands.READ_LEFT_DISTANCE,0,0)
	return value

    def getAtPosition(self):
        value = self.board.sendCommand(Commands.AT_POSITION,0,0)
	return value

    def backward(self, speed):
        self.enable()
        commandL = self.speedToCommand(speed)
	commandR = self.speedToCommand(speed)

	self.board.sendCommand(Commands.WRITE_PWM,LEFT_MOTOR_SPEED,commandL)
        self.board.sendCommand(Commands.WRITE_PWM,RIGHT_MOTOR_SPEED,commandR)
        self.board.sendCommand(Commands.WRITE_DIGITAL,LEFT_MOTOR_DIRECTION,0)
        self.board.sendCommand(Commands.WRITE_DIGITAL,RIGHT_MOTOR_DIRECTION,1)


    def leftMotor(self, speed, direction):

        self.enable()
        command = self.speedToCommand(speed)
        if(direction==1):
            self.board.sendCommand(Commands.WRITE_DIGITAL,LEFT_MOTOR_DIRECTION,1)
            self.board.sendCommand(Commands.WRITE_PWM,LEFT_MOTOR_SPEED,command)
        else:
            self.board.sendCommand(Commands.WRITE_PWM,LEFT_MOTOR_SPEED,command)
            self.board.sendCommand(Commands.WRITE_DIGITAL,LEFT_MOTOR_DIRECTION,0)



    def rightMotor(self, speed, direction):

        self.enable()
        command = self.speedToCommand(speed)
        if(direction==1):
            self.board.sendCommand(Commands.WRITE_DIGITAL,RIGHT_MOTOR_DIRECTION,0)
            self.board.sendCommand(Commands.WRITE_PWM,RIGHT_MOTOR_SPEED,command)
        else:
            self.board.sendCommand(Commands.WRITE_PWM,RIGHT_MOTOR_SPEED,command)
            self.board.sendCommand(Commands.WRITE_DIGITAL,RIGHT_MOTOR_DIRECTION,1)



    def stop(self):

	self.board.sendCommand(Commands.WRITE_DIGITAL,LEFT_MOTOR_SPEED,0)
        self.board.sendCommand(Commands.WRITE_DIGITAL,RIGHT_MOTOR_SPEED,0)
        #self.position(0)
        #self.rotation(0)

    def speedToCommand(self,speed):
        #speed between 0-100
        command = int(speed * 2.55)
        if(command > 255):
            command = 255
        return command


    def position(self,pos,speed):
        self.board.sendCommand(Commands.POSITION,pos,speed)

    def goPosition(self,pos):
        self.board.sendCommand(Commands.POSITION,pos,speed)

        value = self.board.sendCommand(Commands.AT_POSITION,0,0)
	while(value==0):
		print("on my way")
		sleep(0.2)



    def moveForward(self,pos,speed=DEFAULT_SPEED):
        self.position(pos,speed)

    def moveBackward(self,pos,speed=DEFAULT_SPEED):
        self.position(-pos)

    def rotate(self,angle,speed):
        self.board.sendCommand(Commands.ROTATE,angle,speed)

    def turnLeft(self,angle,speed=DEFAULT_SPEED):
        self.rotation(-angle,speed)

    def turnRight(self,angle,speed=DEFAULT_SPEED):
        self.rotation(angle,speed)

    def __del__(self):
        self.stop()

#sleep(1)
#print board.sendCommand(Commands.READ_ULTRASOUND,17,19)







'''
class Motors():
    def __init__(self):
        self.board = Arduino()
        self.board.connect()

    def enable(self): #arduino.A2
        self.board.sendCommand(Commands.WRITE_DIGITAL,7,1)

    def disable(self):
        self.board.sendCommand(Commands.WRITE_DIGITAL,7,0)

    def forward(self, speed):
        self.disable()
        command = self.speedToCommand(speed)
        self.board.sendCommand(Commands.WRITE_PWM,LEFT_MOTOR_DIRECTION,0)
        self.board.sendCommand(Commands.WRITE_PWM,RIGHT_MOTOR_DIRECTION,0)
        self.board.sendCommand(Commands.WRITE_PWM,LEFT_MOTOR_SPEED,command)
        self.board.sendCommand(Commands.WRITE_PWM,RIGHT_MOTOR_SPEED,command)
        #commands are set, enable the motors
        self.enable()

	def getLeft(self):
		value = self.board.sendCommand(Commands.READ_LEFT_ENCODER,0,0)
		return value

	def getRight(self):
		value = self.board.sendCommand(Commands.READ_RIGHT_ENCODER,0,0)
		return value

    def backward(self, speed):
        self.disable()
        command = self.speedToCommand(speed)
        self.board.sendCommand(Commands.WRITE_PWM,LEFT_MOTOR_SPEED,0)
        self.board.sendCommand(Commands.WRITE_PWM,RIGHT_MOTOR_SPEED,0)
        self.board.sendCommand(Commands.WRITE_PWM,LEFT_MOTOR_DIRECTION,command)
        self.board.sendCommand(Commands.WRITE_PWM,RIGHT_MOTOR_DIRECTION,command)
        #commands are set, enable the motors
        self.enable()

    def leftMotor(self, speed, direction):
        self.disable()
        command = self.speedToCommand(speed)
        if(direction==1):
            self.board.sendCommand(Commands.WRITE_PWM,LEFT_MOTOR_DIRECTION,0)
            self.board.sendCommand(Commands.WRITE_PWM,LEFT_MOTOR_SPEED,command)
        else:
            self.board.sendCommand(Commands.WRITE_PWM,LEFT_MOTOR_SPEED,0)
            self.board.sendCommand(Commands.WRITE_PWM,LEFT_MOTOR_DIRECTION,command)
        self.enable()

    def rightMotor(self, speed, direction):
        self.disable()
        command = self.speedToCommand(speed)
        if(direction==1):
            self.board.sendCommand(Commands.WRITE_PWM,RIGHT_MOTOR_DIRECTION,0)
            self.board.sendCommand(Commands.WRITE_PWM,RIGHT_MOTOR_SPEED,command)
        else:
            self.board.sendCommand(Commands.WRITE_PWM,RIGHT_MOTOR_SPEED,0)
            self.board.sendCommand(Commands.WRITE_PWM,RIGHT_MOTOR_DIRECTION,command)
        self.enable()

    def stop(self):
        #self.disable()
        self.board.sendCommand(Commands.WRITE_DIGITAL,LEFT_MOTOR_DIRECTION,0)
        self.board.sendCommand(Commands.WRITE_DIGITAL,RIGHT_MOTOR_DIRECTION,0)
        self.board.sendCommand(Commands.WRITE_DIGITAL,LEFT_MOTOR_SPEED,0)
        self.board.sendCommand(Commands.WRITE_DIGITAL,RIGHT_MOTOR_SPEED,0)
        self.position(0)
        self.rotation(0)

    def speedToCommand(self,speed):
        #speed between 0-100
        command = int(speed * 2.55)
        if(command > 255):
            command = 255
        return command


    def position(self,pos,speed)
        speed = speedToCommand(speed)
        self.disable()
        self.board.sendCommand(Commands.POSITION,speed,pos)
        self.enable()

    def position(self,pos):
        position(pos,DEFAULT_SPEED)


    def moveForward(self,pos,speed):
	self.position(pos,speed)

    def moveForward(self,pos):
	self.position(pos)


    def moveBackward(self,pos,speed):
	self.position(-pos)

    def moveBackward(self,pos):
	self.position(-pos)


    def rotation(self,angle,speed):
        speed = speedToCommand(speed)
        self.disable()
        self.board.sendCommand(Commands.ROTATE,speed,angle)
        self.enable()

    def rotation(self,angle):
        rotation(angle,DEFAULT_SPEED)


    def turnLeft(self,angle,speed):
	self.rotation(angle,speed)

    def turnLeft(self,angle):
	self.rotation(angle)


    def turnRight(self,angle,speed):
	self.rotation(-angle,speed)

    def turnRight(self,angle):
	self.rotation(-angle)

    def __del__(self):
        self.stop()

#sleep(1)
#print board.sendCommand(Commands.READ_ULTRASOUND,17,19)
'''
