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
  delay(100);
}

void setup() {
  // put your setup code here, to run once:
  pinMode(server, INPUT);
  Serial.begin(9600);
}
int a = 1;
void loop() {
  // put your main code here, to run repeatedly:

  while(a==1){  
    a = digitalRead(server);
  }
  delay_1();
  delay_2();
  byte resultado = 0x00;
  for (int i =0; i<8; i++) {
    
    resultado |=  digitalRead(server)<<(i-1);
    delay_1();
    Serial.println(digitalRead(server));
  }
  delay_1();
  Serial.println("--");
  Serial.println(resultado);
  
  a = 1;
}
