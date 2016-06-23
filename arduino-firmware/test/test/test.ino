void setup(){
  Serial.begin(9600)
}

void loop(){
  if(Serial.available()){
    number = Serial.read();
    Serial.print("Character recieved");
    Serial.println(number,DEC);
  }
}
