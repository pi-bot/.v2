
/*
 * Encoder.h
 *
 * Created: 25/02/2016 18:47:23
 *  Author: Olly
*
*	updated with new pin definitions by Jason 10/05/2016
 */ 

#ifndef _ENCODER_H_
#define _ENCODER_H_


// INTERRUPT PIN
#define NOT_AN_INTERRUPT  -1
#define digitalPinToInterrupt(p) ((p) == 2 ? 0 : ((p) == 3 ? 1 : NOT_AN_INTERRUPT))

// PINS
#define RIGHT_ENCODER_A		3
#define RIGHT_ENCODER_B		4

#define LEFT_ENCODER_A		2
#define LEFT_ENCODER_B		8



class ENCODER
{
	public:
		ENCODER();
		void init(int interruptPin, int dirPin, void (*interruptHandler)(void));
		double read(void);
		double readVelocity(void);
		
		void write(double val);
		void increment(void);
		void decrement(void);
		void reset(void);
		bool dirPinState(void);
		
		double tksPerPeriod = 0;
		
	private:
		int _interruptNum;
		int _dirPin;
		
		double posCount = 0;
		
};

void R_EncHandler(void);
void L_EncHandler(void);

void L_calcVel(void);
void R_calcVel(void);


extern ENCODER R_ENC;
extern ENCODER L_ENC;


#endif /*_ENCODER_H_*/
