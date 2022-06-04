
#include <Wire.h> 
#include <SPI.h>
#include <MFRC522.h>
#include <LiquidCrystal_I2C.h>

#define pin_reset 0      
#define pin_ss 2  

LiquidCrystal_I2C lcd(0x27, 16, 2);

MFRC522 mfrc522(pin_ss,pin_reset);
//SoftwareSerial mySerial(0, 15); // RX, TX

void setup() {
//  Wire.pins(4,5); // SDA, SCL
//  Wire.begin();
  Serial.begin(9600);
  SPI.begin();
  mfrc522.PCD_Init();
  Serial.println("Put your card to the reader...");
  lcd.begin();
  lcd.backlight();
  printLcd("Sistem keamanan","laboratorium");
  delay(2000);
}

void loop() {
  printLcd("Scan","Kartu ...");
  if(!mfrc522.PICC_IsNewCardPresent()){
    return;
  }

  if(!mfrc522.PICC_ReadCardSerial()){
    return;
  }

  Serial.print("UID tag :");
  String content = "";
  byte letter;

  for(byte i = 0; i < mfrc522.uid.size; i++){
    Serial.print(mfrc522.uid.uidByte[i] < 0x10 ? " 0" : " ");
    Serial.print(mfrc522.uid.uidByte[i], HEX);
    content.concat(String(mfrc522.uid.uidByte[i] < 0x10 ? " 0" : " "));
    content.concat(String(mfrc522.uid.uidByte[i], HEX));
  }

  Serial.println();
  Serial.print("Pesan : ");
  content.toUpperCase();
  
  
  if(content.substring(1) == "D9 DF 60 B9"){
    Serial.println("Kartu cocok");
    Serial.println();
    printLcd("Akses","diizinkan ...");
    delay(1000);
  }

  else if(content.substring(1) == "79 D0 24 A3"){
    Serial.println("Kartu cocok");
    Serial.println();
    printLcd("Akses","diizinkan ...");
    delay(1000);
  }

  else{
    Serial.println("Kartu Tidak cocok");
    printLcd("Akses","tidak diizinkan ...");
    delay(1000);
  }

  delay(1000);

}


void printLcd(String teks, String teks2){
  lcd.clear();
  lcd.setCursor(0,0);
  lcd.print(teks);
  lcd.setCursor(0,1);
  lcd.print(teks2);
}
