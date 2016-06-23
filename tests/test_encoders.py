from pibot.arduino import Arduino
from pibot.encoder import Encoder
from time import sleep

board = Arduino()
board.connect()
enc = Encoder()

print("testing encoders")
#previous_rightrev = enc.getRevsright()
#previous_leftrev =  enc.getRevsleft()
while True:
    
    #rightrevs = enc.getRevsright()
    leftrevs =  enc.getRevsleft()
    #if rightrevs!=previous_rightrev:
        #print rightrevs
        #previous_rightrev = rightrevs

    #if leftrevs!=previous_leftrev:
    print "blah"
        #previous_leftrev = leftrevs
   
