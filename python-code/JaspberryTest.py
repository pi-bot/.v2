import RPi.GPIO as GPIO
import time
from servo import Servo
import servo 
from stepper import Stepper
from arduino import Arduino, Commands
from ultrasound import Ultrasound
import picamera
from motors import Motors
from time import sleep

#This program use the board numerotation for GPIOs, so up left is 1 and down right is 40
RED_LED_GPIO = 26
GREEN_LED_GPIO = 29
BLUE_LED_GPIO = 31
SERVO_A_GPIO = 25 #GPIO number, not board number
SERVO_B_GPIO = 26 #GPIO number, not board number
STEPPER_GPIOS = [16,33,32,18]#[16,33,32,18]


board=Arduino()
board.connect()
ultra=Ultrasound()
move = Motors()
power = 50


def main():
    try:
        init()
        print '---- test begin ----'
        testLEDs()
       #testServo()
       # testStepper()
        picture()
        testUTX()
        test_Motors()
    except KeyboardInterrupt:
        print 'Keyboard interrupt, exiting the test program'
    except Exception, e:
        print 'An error occured'
        print e
    finally:
        GPIO.cleanup()

def init():
    GPIO.setmode(GPIO.BOARD)

def picture():
    print '=== Camera Test ==='
    with picamera.PiCamera() as camera:
        camera.resolution = (1024, 768)
        camera.capture("photo.jpg")
        print 'Pic saved as photo.jpg'

def test_Motors():
    print("forward")
    move.forward(power)
    sleep(1)
    move.stop()
    sleep(1)
    print("backward")
    move.backward(power)
    sleep(1)
    move.stop()
    sleep(1)
    print("turn right")
    move.leftMotor(power, 1)
    move.rightMotor(power, 0)
    sleep(1)
    move.stop()
    sleep(1)
    print("turn left")
    move.leftMotor(power, 0)
    move.rightMotor(power, 1)
    sleep(1)
    move.stop()
	
    
def testLEDs():
    print '=== LED Test ==='
   # print 'to do: LED PINs to output'
    GPIO.setup(RED_LED_GPIO,GPIO.OUT)
    GPIO.setup(GREEN_LED_GPIO,GPIO.OUT)
    GPIO.setup(BLUE_LED_GPIO,GPIO.OUT)
    print 'to do: LEDs off'
    GPIO.output(RED_LED_GPIO,False)
    GPIO.output(GREEN_LED_GPIO,False)
    GPIO.output(BLUE_LED_GPIO,False)
    print 'to do: Blue LED on for 1 second'
    switchOnLED(BLUE_LED_GPIO,1)
    print 'to do: Green LED on for 1 second'
    switchOnLED(GREEN_LED_GPIO,1)
    print 'to do: Red LED on for 1 second'
    switchOnLED(RED_LED_GPIO,1)

def switchOnLED(LED, duration):
    GPIO.output(LED,True)
    time.sleep(1)
    GPIO.output(LED,False)

def testServo():
    print '=== Servo Test ==='
    print 'to do: servo Turn each 0.5 second'
    for servoPin in SERVO_A_GPIO, SERVO_B_GPIO :
        type = servo.SERVO_ANGLE
        if servoPin == SERVO_B_GPIO:
            type = servo.SERVO_CONTINUOUS
        servoMotor = Servo(servoPin,type)
        for i in range(0,11,1):
            print 0.1*i
    	    servoMotor.set_normalized(0.1*i)
    	    time.sleep(0.5)
        servoMotor.set_normalized(0.5)

def testStepper():
    print '=== Stepper Test ==='
    print 'to do: Stepper PINs to output'
    stepper = Stepper()
    stepper.turn(45,100)
    stepper.turnAsync(-45,50)
    while(not stepper.isMovementFinished()):
        time.sleep(0.02)
    #stepper.stop()

def testUTX():
    print("testing ltrasound")
    x=0
    while  x<10:
        distance=ultra.getDistance()
        print(distance)
        time.sleep(0.5)
        x+=1


if __name__ == '__main__':
    main()
