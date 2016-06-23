
/*
 * Movement.c
 *
 * Created: 25/02/2016 20:35:56
 *  Author: Olly						changed by Jason for PiBot v8.0 10/05/2016
 */ 


#include <Arduino.h>
#include "PID.h"
#include "Movement.h"
#include "Encoder.h"



int L_MotorPins[2] = {6,10};		
int R_MotorPins[2] = {5,9};	
int En_MotorPin = 7;  			// not an enable only a mode pin on PiBot v8.0
		
bool PID_Initialised = false;

bool R_prev_dir;
bool L_prev_dir;

bool Rotate = false;
bool Move = false;
// Position controllers

double Kp_Pos=4.5, Ki_Pos=0.5, Kd_Pos=0;

bool L_MotorEn = false;
bool R_MotorEn = false;

double L_TargPos, L_CurrPos, L_OutputPos;
double R_TargPos, R_CurrPos, R_OutputPos;

PID L_PID_Pos(&L_CurrPos, &L_OutputPos, &L_TargPos, Kp_Pos, Ki_Pos, Kd_Pos, DIRECT);
PID R_PID_Pos(&R_CurrPos, &R_OutputPos, &R_TargPos, Kp_Pos, Ki_Pos, Kd_Pos, DIRECT);




// Differential control
double Kp_Diff=3.5, Ki_Diff=0.1, Kd_Diff=0;

double TargDiff, CurrDiff, OutputDiff;


PID PID_Diff(&CurrDiff, &OutputDiff, &TargDiff, Kp_Diff, Ki_Diff, Kd_Diff, DIRECT);





void movePos(int deltaPos, int speed)
{
 
  L_PID_Pos.SetOutputLimits(-speed,speed);
  L_CurrPos = L_ENC.read();
  L_TargPos = L_CurrPos + DIST_TO_CLICKS(deltaPos);
  
  CurrDiff = 0;
  
  R_PID_Pos.SetOutputLimits(-speed,speed);
  R_CurrPos = -R_ENC.read();
  R_TargPos = R_CurrPos + DIST_TO_CLICKS(-deltaPos);

  Move = true;

  L_MotorEn = true;
  R_MotorEn = true;
}

void moveRotate(double deltaAngle, int speed)
{
  L_PID_Pos.SetOutputLimits(-speed,speed);
  L_CurrPos = L_ENC.read();
  L_TargPos = L_CurrPos + ANGLE_TO_CLICKS(deltaAngle);
 
  CurrDiff = 0;
 
  R_PID_Pos.SetOutputLimits(-speed,speed); 
  R_CurrPos = R_ENC.read();
  R_TargPos = R_CurrPos - ANGLE_TO_CLICKS(-deltaAngle);
  
  Rotate = true;
  
  L_MotorEn = true;
  R_MotorEn = true;
}

void initPID(void)
{
	L_PID_Pos.SetMode(AUTOMATIC);
	R_PID_Pos.SetMode(AUTOMATIC);
	L_PID_Pos.SetSampleTime(1);
	R_PID_Pos.SetSampleTime(1);
	L_PID_Pos.SetOutputLimits(-MAX_SPEED,MAX_SPEED);
	R_PID_Pos.SetOutputLimits(-MAX_SPEED,MAX_SPEED);
	
	PID_Diff.SetMode(AUTOMATIC);
	PID_Diff.SetSampleTime(1);
	PID_Diff.SetOutputLimits(-MAX_SPEED,MAX_SPEED);
	

	PID_Initialised = true;
}

void initMotors(void)
{
	for(int i=0;i<2;i++)
	{
		pinMode(L_MotorPins[i],OUTPUT);
		pinMode(R_MotorPins[i],OUTPUT);
	}
	pinMode(En_MotorPin,OUTPUT);
	digitalWrite(En_MotorPin,HIGH);
}

// converts vectorised speed to 2-pin-PWM control
void motorControl(signed int speed, int* pins)
{
	
	
	speed = constrain(speed,-MAX_SPEED,MAX_SPEED);
        
	if(speed==0 && pins[0]==6){
            analogWrite(10,speed);
        }
        else if(speed==0 && pins[0]==5){
            analogWrite(9,speed);
        }
        if(speed>0 && pins[0]==6){
            
            if(L_prev_dir == false){
              digitalWrite(6,HIGH);
              L_prev_dir = true;
              
            }
            analogWrite(10,speed);
            
         }
         else if(speed>0 && pins[0]==5){
           
            if(R_prev_dir == false){
              digitalWrite(5,HIGH);
              R_prev_dir = true;
              
            }
            analogWrite(9,speed);
           
         }
         if(speed<0 && pins[0]==6){
            speed = abs(speed);
            
            if(L_prev_dir == true){
              digitalWrite(6,LOW);
              L_prev_dir = false;
              
            }
            analogWrite(10,speed);
            
         }
         else if(speed<0 && pins[0]==5){
           
            speed = abs(speed);
            
            if(R_prev_dir == true){
              digitalWrite(5,LOW);
              R_prev_dir = false; 
            }
            analogWrite(9,speed);
            
         }
         
}

void calcPID(void)
{
        
	L_CurrPos = L_ENC.read();
	R_CurrPos = R_ENC.read();
        
        if(Move == true){
          CurrDiff = L_CurrPos+R_CurrPos;
        }
        else if(Rotate == true){
          CurrDiff = L_CurrPos-R_CurrPos; 
        }
        else{
          CurrDiff = 0;
        }
        PID_Diff.Compute();
       //OutputDiff = 0;

	if(L_PID_Pos.Compute() && L_MotorEn)
	{
          
          if(Move == true){
             if(OutputDiff<0 && L_OutputPos>0 || OutputDiff>0 && L_OutputPos<0){
                motorControl(L_OutputPos+OutputDiff,L_MotorPins);
             }
              else{
                motorControl(L_OutputPos,L_MotorPins);
              }
          }
          if(Rotate == true){
            Serial.print("L");
            Serial.print(L_CurrPos);
            Serial.print("Lo");
            Serial.print(L_OutputPos);
            Serial.print("LT");
            Serial.print(L_TargPos);
            Serial.print("diff");
            Serial.print(OutputDiff);
            Serial.print("Cdiff");
            Serial.print(CurrDiff);
//            if(OutputDiff<0 && L_OutputPos>0 || OutputDiff>0 && L_OutputPos<0){
//                motorControl(L_OutputPos+OutputDiff,L_MotorPins);
//            }
//            else{
//                motorControl(L_OutputPos,L_MotorPins);
//            
//            }
          
	  }
        }

	if(R_PID_Pos.Compute() && R_MotorEn)
	{
          
          if(Move == true){
            if(OutputDiff>0 && R_OutputPos<0 || OutputDiff<0 && R_OutputPos>0){
             motorControl(R_OutputPos+OutputDiff,R_MotorPins);
            }
            else{
              motorControl(R_OutputPos,R_MotorPins);
            }
          }
  
          if(Rotate == true){
            Serial.print("R");
            Serial.print(R_CurrPos);
            Serial.print("Ro");
            Serial.print(R_OutputPos);
            Serial.print("RT");
            Serial.print(R_TargPos);
            Serial.println("");
            while(1){}
            if(OutputDiff>0 && R_OutputPos>0 || OutputDiff<0 && R_OutputPos<0){
               motorControl(R_OutputPos-OutputDiff,R_MotorPins);
            }
            else{
              motorControl(R_OutputPos,R_MotorPins);
            }
          }
          
	        
		
	}

//L further -
//R         +
// Serial.print("Lcurr ");
// Serial.print(L_CurrPos);
// Serial.print("targ ");
// Serial.print(L_TargPos);
// Serial.print("\t error ");
// Serial.print(L_TargPos-L_CurrPos);
// Serial.print("  ");
// Serial.print(CLICKS_TO_DIST(L_TargPos-L_CurrPos));
// Serial.print("\tVel curr ");
// Serial.print(L_CurrVel);
// Serial.print("\t targ ");
// Serial.print(L_TargVel);
// Serial.print("\t out ");
// Serial.print(L_OutputPos);
//
// Serial.print("R Pos curr ");
// Serial.println(R_CurrPos);
// Serial.print("\ttarg ");
// Serial.print(R_TargPos);
// Serial.print("\t error ");
// Serial.print(R_TargPos-R_CurrPos);
// Serial.print("  ");
// Serial.print(CLICKS_TO_DIST(R_TargPos-R_CurrPos));
// Serial.print("\tVel curr ");
// Serial.print(R_CurrVel);
// Serial.print("\t targvel ");
// Serial.print(R_TargVel);
// Serial.print("\t motorpins");
// Serial.print(R_MotorPins[0]);
//   Serial.print("Diff");
//  Serial.println(OutputDiff);
// Serial.print("\t Difference");

checkPosReached();
}



void disableControlLoop(void)
{
  L_MotorEn = false;
  R_MotorEn = false;
  motorControl(0,L_MotorPins);
  motorControl(0,R_MotorPins);
  L_TargPos = L_ENC.read();
  R_TargPos = R_ENC.read();
  Move = false;
  Rotate = false;
}



void checkPosReached(void)
{
    if(L_reachedPos()&& R_reachedPos()&& L_MotorEn==true)
  {
    Serial.println("Reached position");
    disableControlLoop();
  }
}


bool L_reachedPos(void)
{
   if(abs(L_TargPos-L_CurrPos)<=POS_TOLERANCE)
    return 1;
   else
    return 0;
}


bool R_reachedPos(void)
{
  if(abs(R_TargPos-R_CurrPos)<=POS_TOLERANCE)
    return 1;
   else
    return 0;
}

bool get_movement(void){
  if(L_MotorEn == false && R_MotorEn == false){
    
    return 0;
    
  }
  else{
    return 1;
  }
  
}
