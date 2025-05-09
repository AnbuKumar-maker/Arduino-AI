char receivedChar;

const int segmentPins[7] = {2, 3, 4, 5, 6, 7, 8}; // a to g

// Segment patterns for digits 1 to 5
// a b c d e f g
const byte digitPatterns[6][7] = {
  {1, 1, 1, 1, 1, 1, 1}, // [0] → all off (no finger)
  {1, 0, 0, 1, 1, 1, 1}, // [1]
  {0, 0, 1, 0, 0, 1, 0}, // [2]
  {0, 0, 0, 0, 1, 1, 0}, // [3]
  {1, 0, 0, 1, 1, 0, 0}, // [4]
  {0, 1, 0, 0, 1, 0, 0}  // [5]
};

void setup() {
  Serial.begin(9600);
  for (int i = 0; i < 7; i++) {
    pinMode(segmentPins[i], OUTPUT);
    digitalWrite(segmentPins[i], HIGH); // start with all segments off
  }
}

void loop() {
  if (Serial.available()) {
    receivedChar = Serial.read();

    if (receivedChar >= '0' && receivedChar <= '5') {
      int digit = receivedChar - '0';

      for (int i = 0; i < 7; i++) {
        digitalWrite(segmentPins[i], digitPatterns[digit][i]);
      }
    }
  }
}
