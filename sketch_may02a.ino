void setup() {
Serial.begin(9600);
for (int i = 2; i <= 6; i++) {
pinMode(i, OUTPUT);
}
}

void loop() {
if (Serial.available()) {
char ch = Serial.read();
int count = ch - '0';

for (int i = 0; i < 5; i++) {
if (i < count) {
digitalWrite(2 + i, HIGH);
} else {
digitalWrite(2 + i, LOW);
}
}
}
}
