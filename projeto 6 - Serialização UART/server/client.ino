int server = 7;
bool received = true;
void delay() {
for (int i =0; i < 1089, i++;) {
  asm("NOP");
}
}

void delay_2() { 
for (int i =0; i < 544, i++;) {
  asm("NOP");
}
}

void setup() {
  // put your setup code here, to run once:
  pinMode(server, INPUT);
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:

  while(received){
    received = digitalRead(server);
  }
  delay();
  delay_2();
  unsigned char mask = 0x00;
  for (int i =0; i<8, i++;) {
    unsigned char mensagem = digitalRead(server);
    mask = mask | mensagem;
    mask = mask << i;
    delay();
  }
  Serial.print(mask);

}
