int sender = 7;
char mensagem = 'B';

void delay_1(){
for (int i = 0; i< 2186; i++){
  asm("NOP");

}
//  delay(1000);
}

void setup() {
  // put your setup code here, to run once:
  
  Serial.begin(9600);
  pinMode(sender, OUTPUT);
  digitalWrite(sender, HIGH);
  delay(3000);
}


void loop() {
  // put your main code here, to run repeatedly:

  digitalWrite(sender,LOW);
  delay_1();
  for(int i =0; i<8; i++){
    digitalWrite(sender, mensagem >> i & 0x01);
    delay_1();
  } 

  digitalWrite(sender, HIGH);
  delay_1();
  digitalWrite(sender, HIGH);
  delay_1();
  Serial.println("enviou");
  delay(3000);
}


