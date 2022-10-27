int sender = 7;
char mensagem = 'C';

void delay_1(){
//for (int i = 0; i< 2186; i++){
//  asm("NOP");

//}
  delay(1000);
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
  delay(1100);
  for(int i =0; i<8; i++){
    int correcao = 7-i;
    digitalWrite(sender, mensagem >> i & 0x01);
    delay_1();
    Serial.println(mensagem >> i & 0x01);
  } 

  digitalWrite(sender, HIGH);
  Serial.println("--");
  delay(6000);
}


