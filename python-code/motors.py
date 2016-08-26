#  	New version for "PiBot v8.0" With improved motor control IC DRV8835
#	also updated with new pin definitions for new PCB
#
#		by Harry / Matt  10/08/2016
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

DUMMY_PIN = arduino.A3  # Let the pin value be accepted for the pos/ rotation functions

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

     # lower level command to move
    def position(self,pos,speed=DEFAULT_SPEED,block=True):
        self.board.sendCommand(Commands.POSITION,DUMMY_PIN,pos)
                
        if block:
            there=int(self.getAtPosition())
            while int(self.getAtPosition()) == 0:
                print("on my way")
                sleep(0.2)
            print("got there! - Now I'll do  next command")



    def rotate(self,angle,speed=DEFAULT_SPEED,block):
        self.board.sendCommand(Commands.ROTATE,DUMMY_PIN,angle)

        if block:
            there=int(self.getAtPosition())
            while int(self.getAtPosition()) == 0:
                print("on my way")
                sleep(0.2)
            print("got there! - Now I'll do  next command")



    def moveForward(self,pos,speed=DEFAULT_SPEED, block=True):
        self.position(pos)

    def moveBackward(self,pos,speed=DEFAULT_SPEED, block=True):
        self.position(-pos)

    def turnLeft(self,angle,speed=DEFAULT_SPEED, block=True):
        self.rotate(speed, -angle)

    def turnRight(self,angle,speed=DEFAULT_SPEED, block=True):
        self.rotate(speed, angle)

    def __del__(self):
        self.stop()
