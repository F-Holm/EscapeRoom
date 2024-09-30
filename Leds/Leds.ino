#include <Adafruit_NeoPixel.h>

#define PIN_1 8
#define PIN_2 9
#define PIN_3 10
#define NUMPIXELS_1 300
#define NUMPIXELS_2 92
#define NUMPIXELS_3 200

#define RED 3
#define GREEN 5
#define BLUE 6


Adafruit_NeoPixel pixels_1 = Adafruit_NeoPixel(NUMPIXELS_1, PIN_1, NEO_GRB + NEO_KHZ800);
Adafruit_NeoPixel pixels_2 = Adafruit_NeoPixel(NUMPIXELS_2, PIN_2, NEO_GRB + NEO_KHZ800);
Adafruit_NeoPixel pixels_3 = Adafruit_NeoPixel(NUMPIXELS_3, PIN_3, NEO_GRB + NEO_KHZ800);

String color = String('\0') + String('\0') + String('\0');

unsigned long previousMillis = 0;
char efectoActual = "";
int etapaActual = -1;
bool efectoActivo = false;

// CAMBIAR COLORES RGB //

void cambiarColorIntRGB(int r, int g, int b){
  analogWrite(RED, r);
  analogWrite(GREEN, g);
  analogWrite(BLUE, b);
}

void cambiarColorRGB(String rgb) {
  analogWrite(RED, rgb[0]);
  analogWrite(GREEN, rgb[1]);
  analogWrite(BLUE, rgb[2]);
  color = rgb;
}

void cambiarColorSinGuardarRGB(String rgb) {
  analogWrite(RED, rgb[0]);
  analogWrite(GREEN, rgb[1]);
  analogWrite(BLUE, rgb[2]);
}

void defaultRGB(){
  analogWrite(RED, color[0]);
  analogWrite(GREEN, color[1]);
  analogWrite(BLUE, color[2]);
}

// CAMBIAR COLORES NEO PIXEL //

void cambiarColorUniformeNeoPixel(int _r, int _g, int _b){
  for(int i = 0; i < NUMPIXELS_1; i++){
    pixels_1.setPixelColor(i, _r, _g, _b);
  }
  pixels_1.show();

  for(int i = 0; i < NUMPIXELS_2; i++){
    pixels_2.setPixelColor(i, _r, _g, _b);
  }
  pixels_2.show();

  for(int i = 0; i < NUMPIXELS_3; i++){
    pixels_3.setPixelColor(i, _r, _g, _b);
  }
  pixels_3.show();
}

void defalutNeoPixel(){
  cambiarColorUniformeNeoPixel(0, 0 , 0);
}

void setEfecto(char e){
  efectoActual = e;
  efectoActivo = true;
  etapaActual = 0;
  previousMillis = millis();
}

void efecto(){
  switch (efectoActual){
  }
}

void setup() {
  pinMode(RED, OUTPUT);
  pinMode(GREEN, OUTPUT);
  pinMode(BLUE, OUTPUT);

  defaultRGB();

  pixels_1.begin();
  pixels_2.begin();
  pixels_3.begin();
  cambiarColorUniformeNeoPixel(0, 0, 0);

  Serial.begin(9600);

  /*while(true) {
    while (Serial.available() <= 0);
    int identificate = Serial.read();
    if (identificate == 5) Serial.print(8);
    else continue;
  }*/
}

void loop() {
  /*if (efectoActivo) efecto();
  if (Serial.available() > 0) {
    String colores = Serial.readString();//Si tiene 2 caracteres, si empieza en 0 es un efecto de luces RGB, si empieza en 1 es un efecto de neopixel. Si tiene 3 caracteres, cada caracter representa un color (RGB).
    if (colores.length() == 1) setEfecto(colores[0]);
    if (colores.length() == 3) cambiarColorRGB(colores);
  }*/
  cambiarColorUniformeNeoPixel(255, 0, 0);
}

/*void ambientacionNueva(){
  for(int i = 0; i < NUMPIXELS; i++){ 
    pixels.setPixelColor(i, _r, _g, _b);
  }
  pixels.show();
}*/
