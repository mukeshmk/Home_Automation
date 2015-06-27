const int Temp = A0;
const int Humid = A1;
const int LDR = A2;

void setup() 
{
  
pinMode(Temp, INPUT);
pinMode(Humid, INPUT);
pinMode(LDR, INPUT);
Serial.begin(9600);

}

void loop() 
{
  
  Serial.print(analogRead(Temp)*(5.0/1023.0)*100);
  Serial.print("\t");
  Serial.print(analogRead(Humid)*(5.0/1023.0));
  Serial.print("\t");
  Serial.println(analogRead(LDR)*(5.0/1023.0)*100.0); 
  delay(5000);

}
