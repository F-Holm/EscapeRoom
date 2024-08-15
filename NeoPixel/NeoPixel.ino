#include <Adafruit_NeoPixel.h>
 
 
#define PIN 8
#define NUMPIXELS 300
 
Adafruit_NeoPixel pixel = Adafruit_NeoPixel(NUMPIXELS, PIN, NEO_GRB + NEO_KHZ800);
 
void setup() {
  Serial.begin(9600);

  pixel.begin(); 
  pixel.show();
}

void rojo(){
  for (int i = 0; i < NUMPIXELS; i++) {
    pixel.setPixelColor(i, pixel.Color(255, 0, 0)); 
  }
  pixel.show(); 
}

void blanco(){
  for (int i = 0; i < NUMPIXELS; i++) {
    pixel.setPixelColor(i, pixel.Color(255, 255, 255)); 
  }
  pixel.show(); 
}

void relampago(){
  rojo();
  delay(3000);
  blanco();
  delay(25);
  rojo();
  delay(50);
  blanco();
  delay(25);
}
void rojoVariable(int cantRojo){
  for (int i = 0; i < NUMPIXELS; i++) {
    pixel.setPixelColor(i, pixel.Color(cantRojo, 0, 0)); 
  }
  pixel.show(); 
}
//190
//140
//100
//50
void apagado(){
    for (int i = 0; i < NUMPIXELS; i++) {
    pixel.setPixelColor(i, pixel.Color(0, 0, 0)); 
  }
  pixel.show();

}
void cieloInfierno(){
  rojo();
  int segundos = random(1000, 6000);
  Serial.println(segundos);
  delay(segundos);
  relampago();
}

void cielo(){
  for (int i = 0; i < NUMPIXELS; i++) {
    pixel.setPixelColor(i, pixel.Color(80, 255, 80)); 
  }
  pixel.show(); 
}
 
void loop() { 
  if (Serial.available() > 0) {
      int num = Serial.read();
      Serial.println(num);
      switch(num){
        case 0:
          cieloInfierno();
          break;
        case 1:
          cielo();
          break;
      }
  }
}