#include <SPI.h>
#include <MFRC522.h>
#include <Servo.h>
#include <SoftwareSerial.h>
#define RST_PIN         9          // Configurable, see typical pin layout above
#define SS_PIN          10         // Configurable, see typical pin layout above
int pos1 = 0;
int pos2 = 0;
MFRC522 mfrc522(SS_PIN, RST_PIN); // Create MFRC522 instance.
Servo myservo1;
Servo myservo2;

int incomingByte = 0; // for incoming serial data
String content = "";
String buff;
void setup()
{
  Serial.begin(9600); // Initiate a serial communication

  SPI.begin();     // Initiate  SPI bus
  mfrc522.PCD_Init(); // Initiate MFRC522
  myservo1.attach(8);
  myservo2.attach(7);
}

void control_servo1() {
  for (pos1 = 0; pos1 < 180; pos1 += 1) {

    myservo1.write(pos1);
    delay(5);
  }

  for (pos1 = 180; pos1 >= 1; pos1 -= 1) {
    myservo1.write(pos1);
    delay(5);
  }
}
void control_servo2() {
  for (pos2 = 0; pos2 < 180; pos2 += 1) {

    myservo2.write(pos2);
    delay(5);
  }

  for (pos2 = 180; pos2 >= 1; pos2 -= 1) {
    myservo2.write(pos2);
    delay(5);
  }
}
void loop()
{
  if (!mfrc522.PICC_IsNewCardPresent())
  {
    return;
  }
  if (!mfrc522.PICC_ReadCardSerial())
  {
    return;
  }
  //Show UID on serial monitor
  String content = "";
  for (byte i = 0; i < mfrc522.uid.size; i++)
  {
    //Serial.print(mfrc522.uid.uidByte[i]<0x10?" 0":" ");
    //Serial.print(mfrc522.uid.uidByte[i],HEX);
    content.concat(String(mfrc522.uid.uidByte[i] < 0x10 ? " 0" : " "));
    content.concat(String(mfrc522.uid.uidByte[i], HEX));
  }
  content.toUpperCase();
  
  Serial.println(content);
  delay(200);
  if (Serial.available() > 0) {
    buff = Serial.readStringUntil('\r');
    Serial.print(buff);
    if (buff == "IN") {
      control_servo1();
    }
    if (buff == "OUT") {
      control_servo2();
    }
  }
  delay(200);
}
