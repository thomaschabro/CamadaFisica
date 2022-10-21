int server = 7;
void delay_1() {
//for (int i =0; i < 2186, i++;) {
//  asm("NOP");
//}
  delay(1000);
}

void delay_2() { 
//for (int i =0; i < 1093, i++;) {
//  asm("NOP");
//}
  delay(500);
}

void setup() {
  // put your setup code here, to run once:
  pinMode(server, INPUT);
  Serial.begin(9600);
}
int a = 1;
void loop() {
  // put your main code here, to run repeatedly:

  while(a!=0){  
    a = digitalRead(server);
  }
  delay_1();
  delay_2();
  byte resultado = 0x00;
  for (int i =0; i<8; i++) {
  //  unsigned char mensagem = digitalRead(server);
  //  mask = mask | mensagem;
  //  mask = mask << i;
    
    resultado |=  digitalRead(server)<<i;
    delay_1();
  }
  Serial.println("--");
  Serial.println(resultado);
  
  a = 1;
}
