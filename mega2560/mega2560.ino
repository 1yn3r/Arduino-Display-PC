#include <Wire.h>
#include <LiquidCrystal_I2C.h>

LiquidCrystal_I2C lcd(0x27, 20, 4);  // LCD 20x4

String incomingData = "";
String lastDisplayedData = "";  // Để kiểm tra dữ liệu trùng
unsigned long lastReceivedTime = 0;
unsigned long lastUpdate = 0;
int progress = 0;

void setup() {
  byte square[8] = {
    B11111, B11111, B11111, B11111,
    B11111, B11111, B11111, B11111
  };
  byte heart[8] = {
    B00000, B01010, B11111, B11111,
    B01110, B00100, B00000, B00000
  };

  lcd.createChar(0, square);
  lcd.createChar(1, heart);

  Serial.begin(9600);
  lcd.init();
  lcd.backlight();

  lcd.setCursor(0, 0);
  lcd.print("Start the system...");
  lcd.setCursor(12, 3);
  lcd.print("Lyner");
  lcd.write(1);
  progress++;
}

void loop() {
  // Nhận dữ liệu từ Serial
  while (Serial.available()) {
    char ch = Serial.read();
    if (ch == '\n') {
      incomingData = chomp(incomingData);
      
      // Chỉ cập nhật màn hình nếu dữ liệu thay đổi
      if (incomingData != lastDisplayedData) {
        displayData(incomingData);
        lastDisplayedData = incomingData;
      }

      incomingData = "";
      lastReceivedTime = millis();
    } else {
      incomingData += ch;
    }
  }

  // Sau 6 giây không có dữ liệu → loading
  if (millis() - lastReceivedTime > 6000) {
    loadingEffect();
  }
}

String chomp(String s) {
  s.trim();  // Loại bỏ khoảng trắng dư thừa và newline
  return s;
}

void displayData(String data) {
  lcd.clear();
  int line = 0, startIndex = 0, sepIndex;

  while ((sepIndex = data.indexOf('|', startIndex)) != -1 && line < 4) {
    lcd.setCursor(0, line++);
    lcd.print(data.substring(startIndex, sepIndex));
    startIndex = sepIndex + 1;
  }

  if (line < 4 && startIndex < data.length()) {
    lcd.setCursor(0, line);
    lcd.print(data.substring(startIndex));
  }
}

void loadingEffect() {
  unsigned long currentMillis = millis();
  static int loadingState = 0;

  if (currentMillis - lastUpdate >= 500) {
    lastUpdate = currentMillis;

    lcd.clear();
    int startPos = (20 - 7) / 2;
    lcd.setCursor(startPos, 1);
    lcd.print("Loading");

    switch (loadingState) {
      case 0: lcd.print(" ."); break;
      case 1: lcd.print(" .."); break;
      case 2: lcd.print(" ..."); break;
      case 3: lcd.print(" .."); break;
      default: lcd.print(" ."); break;
    }

    loadingState = (loadingState + 1) % 5;
    displayProgress();
  }
}

void displayProgress() {
  int pos = progress % 20;
  lcd.setCursor(0, 3);
  for (int i = 0; i < 20; i++) {
    if (i <= pos) lcd.write(0);
    else lcd.print(" ");
  }
  progress++;
}
