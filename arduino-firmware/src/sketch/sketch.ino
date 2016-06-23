

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



String inputMessage = "";
boolean inputMessageComplete = false;

bool debug = false;



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
        
        if(inputMessage=="1"){
          Serial.println("-20, 50");
          movePos(-20, 50);
          inputMessage=0;
        
        }
        else if(inputMessage=="2"){
          Serial.println("20, 50");
          movePos(20, 20);
          inputMessage=0;
        
        }
        else if(inputMessage=="3"){
          Serial.println("-20, 80");
          movePos(-20, 80);
          inputMessage=0;
        
        }
        if(inputMessage=="4"){
          Serial.println("20, 80");
          movePos(20, 80);
          inputMessage=0;
        
        }
        else if(inputMessage=="5"){
          Serial.println("-20, 100");
          movePos(-20, 100);
          inputMessage=0;
        
        }
        else if(inputMessage=="6"){
          Serial.println("20, 100");
          movePos(20, 100);
          inputMessage=0;
        
        }
        else if(inputMessage=="7"){
          Serial.println("-20, 120");
          movePos(-20, 120);
          inputMessage=0;
        
        }
        else if(inputMessage=="8"){
          Serial.println("20, 120");
          movePos(20 ,120);
          inputMessage=0;
        
        }
        else if(inputMessage=="9"){
          Serial.println("-20 ,150");
          movePos(-20 ,150);
          inputMessage=0;
        
        }
        else if(inputMessage=="0"){
          Serial.println("20 ,150");
          movePos(20, 150);
          inputMessage=0;
        
        }
        else if(inputMessage=="q"){
        Serial.println("-90, 80");
        moveRotate(-90, 50);
        inputMessage=0;
        
        }
        else if(inputMessage=="w"){
        Serial.println("90, 80");
        moveRotate(90, 50);
        inputMessage=0;
        
        }
        else if(inputMessage=="e"){
        Serial.println("-90, 85");
        moveRotate(-90, 80);
        inputMessage=0;
        
        }
        if(inputMessage=="r"){
        Serial.println("90, 85");
        moveRotate(90, 80);
        inputMessage=0;
        
        }
        else if(inputMessage=="t"){
        Serial.println("-90, 90");
        moveRotate(-90, 100);
        inputMessage=0;
        
        }
        else if(inputMessage=="y"){
        Serial.println("90, 90");
        moveRotate(90, 100);
        inputMessage=0;
        
        }
        else if(inputMessage=="u"){
        Serial.println("-90, 95");
        moveRotate(-90, 120);
        inputMessage=0;
        
        }
        else if(inputMessage=="i"){
        Serial.println("90 ,95");
        moveRotate(90 ,120);
        inputMessage=0;
        
        }
        else if(inputMessage=="o"){
        Serial.println("-90 ,100");
        moveRotate(-90 ,150);
        inputMessage=0;
        
        }
        else if(inputMessage=="p"){
        Serial.println("90 ,100");
        moveRotate(90 ,150);
        inputMessage=0;
        
        }
        
        
   }

   if(get_movement()){
   
        calcPID();
   }
   if(debug == false){
     	if(!inputMessageComplete)
	return;
	
	//a message has been received
	//convert String to char array for parsing
	char inputMessageCharArray[MAX_MESSAGE_LENGTH];
	inputMessage.toCharArray(inputMessageCharArray, MAX_MESSAGE_LENGTH);

	//declare variables and parsing
	int command;
	int pin, value;
	sscanf(inputMessageCharArray,"%i,%i,%i",&command, &pin, &value);

  
//	if(!checkPinNumber(&pin))     // this has been removed to allow pos/rot speed to be sent as a pin value
//	{
//		inputMessage="";
//		inputMessageComplete=false;
//		return;
//	}


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
		movePos(pin,value);
		break;
		case ROTATE:
		moveRotate(pin,value);
		break;
		default:
		break;
	}
	Serial.print(answer+'\n');
	
	inputMessageComplete = false;
	inputMessage = "";
  
	
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
