#
#   New version for "PiBot v8.0" With improved motor control IC DRV8835
#   also updated with new pin definitions for new PCB
#
#       by Jason 10/05/2016
#

import arduino
from arduino import Commands
from arduino import Arduino
from time import sleep

LEFT_MOTOR_DIRECTION = 6   # Direction bit
LEFT_MOTOR_SPEED =10       #PWM speed control
RIGHT_MOTOR_DIRECTION = 5  # Direction bit
RIGHT_MOTOR_SPEED = 9      # PWM speed control
MOTOR_MODE = 7             #Enable motor controller

DEFAULT_SPEED = 50

class Motors():
    def __init__(self):
        self.board = Arduino()
        self.board.connect()

    def enable(self):
        self.board.sendCommand(Commands.WRITE_DIGITAL,7,1)  # puts motor drive into Phase/Enable mode

    def disable(self):
        self.board.sendCommand(Commands.WRITE_DIGITAL,7,0)# puts motor drive into IN/IN mode

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

    def stop(self):

        self.board.sendCommand(Commands.WRITE_DIGITAL,LEFT_MOTOR_SPEED,0)
        self.board.sendCommand(Commands.WRITE_DIGITAL,RIGHT_MOTOR_SPEED,0)
        #self.position(0)
        #self.rotation(0)


    # lower level command to move
    def position(self,pos,speed,block):
        self.board.sendCommand(Commands.POSITION,pos,speed)

        if block:
            while not self.getAtPosition():
                print("on my way")
                sleep(0.2)

    # lower level command to rotate
    def rotate(self,angle,speed,block):
        self.board.sendCommand(Commands.ROTATE,angle,speed,block)

        if block:
            while not self.getAtPosition():
                print("on my way")
                sleep(0.2)

    # helper commands to move
    def moveForward(self,pos,speed=DEFAULT_SPEED,block=True):
        self.position(pos,speed,block)

    def moveBackward(self,pos,speed=DEFAULT_SPEED,block=True):
        self.position(-pos,speed,block)

    # helper commands to rotate
    def turnLeft(self,angle,speed=DEFAULT_SPEED,block=True):
        self.rotation(-angle,speed,block)

    def turnRight(self,angle,speed=DEFAULT_SPEED,block=True):
        self.rotation(angle,speed,block)

    def __del__(self):
        self.stop()

