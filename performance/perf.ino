int counter = 0;

void setup() {
  // put your setup code here, to run once:
   Serial.begin(115200);

}

void loop() {
  counter += 1;
  if (counter % 140000 == 0) {  //140k on ESP8266
    Serial.println("tick");
    counter = 0;
  }
//  delay(1);
}