import arduino
from arduino import Commands
from arduino import Arduino
from time import sleep

class Encoder():

    def __init__(self):
        self.board = Arduino()
        self.board.connect()

    def getRevsright(self):
        rightrevs = self.board.sendCommand(Commands.READ_RIGHT_ENCODER,0,-1)
        return rightrevs

    def getRevsleft(self):
        leftrevs = self.board.sendCommand(Commands.READ_LEFT_ENCODER,0,-1)
        return leftrevs

                       
