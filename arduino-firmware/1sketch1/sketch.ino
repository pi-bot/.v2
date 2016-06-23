

#include <Arduino.h>
#include <SoftwareSerial.h>

#include "PID.h"
#include "Encoder.h"
#include "Commands.h"
#include "Movement.h"
#include "EarthToMars.h"
#include "Ultrasound.h"

#define MAX_MESSAGE_LENGTH 50
#define MAX_RESPONSE_LENGTH 20


ENCODER R_ENC;
ENCODER L_ENC;

bool doOnce = true;

String inputMessage = "";
boolean inputMessageComplete = false;
int pid_engage=0;
bool debug = true;
int prev = 3;


void setup()
{
	// start serial port at 115200 bps:
	Serial.begin(115200);
	// reserve 200 bytes for the inputMessage:
	inputMessage.reserve(MAX_MESSAGE_LENGTH);

	setupETM();
	
	R_ENC.init(RIGHT_ENCODER_A,RIGHT_ENCODER_B,R_EncHandler);
	L_ENC.init(LEFT_ENCODER_A,LEFT_ENCODER_B,L_EncHandler);
	
	// initalise motor pins
	initMotors();
	
	//turn the PID on
	initPID();
	if(debug == true){
	    Serial.println("Started");
        }
       
}

void loop()
{
	serialRecieve();
   if(debug == true){
        if(inputMessage=="go"){
        Serial.println("Moving forward");
        movePos(-10, 50);
        inputMessage=0;
        
        }
        else if(inputMessage=="rot"){
        Serial.println("Rotating");
        moveRotate(90, 50);
        inputMessage=0;
        
        }
        
   }

   if(get_movement()){
   
        calcPID();
   }
   if(debug == false){
	if(!inputMessageComplete){
	
	//a message has been received
	//convert String to char array for parsing
	char inputMessageCharArray[MAX_MESSAGE_LENGTH];
	inputMessage.toCharArray(inputMessageCharArray, MAX_MESSAGE_LENGTH);

	//declare variables and parsing
	int command;
	int pin, value;
	sscanf(inputMessageCharArray,"%i,%i,%i",&command, &pin, &value);

	//call the method corresponding to the command
	String answer = "";
	answer.reserve(MAX_RESPONSE_LENGTH);
	switch (command)
	{
		case READ_RFID:
		answer += getRFID();
		break;
		case READ_DIGITAL:
		answer =+ readDigital(pin) ? "1" : "0";
		//answer += String(readDigital(pin));
		break;
		case READ_ANALOG:
		char analogValue[5];
		sprintf(analogValue,"%i",readAnalog(pin));
		answer =+ analogValue;
		break;
		case WRITE_DIGITAL:
		writeDigital(pin,value);
		break;
		case WRITE_PWM:
		writePWM(pin,value); 
		//disableControlLoop();
		break;
		case READ_ULTRASOUND:
		char distanceValue[5];
		sprintf(distanceValue,"%i",readUltrasound(pin));
		answer =+ distanceValue;
		break;
		case READ_LEFT_ENCODER:
		if(value<0){
			char leftEncoderValue[7];
			sprintf(leftEncoderValue,"%i",L_ENC.read());
			answer =+ leftEncoderValue;
		}
		else{
			L_ENC.write(value);
                        
		}
		break;
		case READ_RIGHT_ENCODER:
		if(value<0){
			char rightEncoderValue[7];
			sprintf(rightEncoderValue,"%i",R_ENC.read());
			answer =+ rightEncoderValue;
		}
		else{
			R_ENC.write(value);
		}
		break;
		case WRITE_NEO_PIXEL:
		//int redValue;
		//int greenValue;
		//int blueValue;
		//sscanf(inputMessageCharArray,"%i,%i,%i,%i,%i,%i",&command, &pin, &value, &redValue, &greenValue, &blueValue);
		//writeNeoPixel(value,redValue,greenValue,blueValue);
		break;
		case RESET_NEO_PIXELS:
		//clearNeoPixels();
		break;
		case POSITION:
		movePos(value,pin);
                answer =+ "GO";
		break;
		case ROTATE:
		moveRotate(value,pin);
		break;
		default:
		break;
	}
	Serial.print(answer+'\n');
	
	inputMessageComplete = false;
	inputMessage = "";
    }
   }
 
  
}

void serialRecieve() {
	while (Serial.available())
	{
		char inChar = (char)Serial.read();
		inputMessage += inChar;
		if (inChar == '\n')
		inputMessageComplete = true;
	}
}

bool checkPinNumber(int *pin)
{
	int analogPins[6][2] = { {A0,500}
	,{A1,501}
	,{A2,502}
	,{A3,503}
	,{A4,504}
	,{A5,505}
};
if(*pin<0)
return false;
else if(*pin>13 && *pin<500)
return false;
else if(*pin > 505)
return false;

for(int i=0;i<6;i++)
{
	if(*pin == analogPins[i][1])
	*pin = analogPins[i][0];
}
return true;
}
