int sender = 7;
char mensagem = 'z';


void delay(){
for (int i = 0; i< 1089; i++){
  asm("NOP");
}
}



void setup() {
  // put your setup code here, to run once:
  pinMode(sender, OUTPUT);

}

void loop() {
  // put your main code here, to run repeatedly:

  digitalWrite(sender,LOW);
  delay();
  for(int i =0; i<8, i++;){
    unsigned char mask= 0x01<<i;
    unsigned char bit = mensagem & mask;
    digitalWrite(sender, bit);
    delay();
  }
    
    
 
}


