const int R = 2;  // Substituir pelos pinos corretos do ESP
const int G = 3;
const int B = 4;

void setup() {
  Serial.begin(9600);
  pinMode(R, OUTPUT);
  pinMode(G, OUTPUT);
  pinMode(B, OUTPUT);
}

void loop() {
  if (Serial.available() > 0) {
    int num_fingers = Serial.parseInt();  // Lê o número de dedos da porta serial
    
    if (num_fingers == 1) {
      analogWrite(R, 255);
      analogWrite(G, 255);
      analogWrite(B, 0);
    }
    else if (num_fingers == 2) {
      analogWrite(R, 0);
      analogWrite(G, 255);
      analogWrite(B, 0);
    }
    else if (num_fingers == 3) {
      analogWrite(R, 255);
      analogWrite(G, 0);
      analogWrite(B, 0);
    }
  }
  else{
    analogWrite(R, 255);
    analogWrite(G, 255);
    analogWrite(B, 255);
  }
}