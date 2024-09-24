#include <Adafruit_NeoPixel.h>

#define PIN 8
#define NUMPIXELS 300

#define RED 3
#define GREEN 5
#define BLUE 6

Adafruit_NeoPixel pixels = Adafruit_NeoPixel(NUMPIXELS, PIN, NEO_GRB + NEO_KHZ800);

String color = String('\0') + String('\0') + String('\0');

unsigned long previousMillis = 0;
String efectoActual = "";
int etapaActual = -1;
bool efectoActivo = false;

// EFECTOS RGB //

const String RAYO = String('\0') + String('\0');

// EFECTO NEOPIXEL //

const String CIELO_INFIERNO = String('\1') + String('\0');
const String CIELO = String('\1') + String('\1');
const String RELAMPAGO = String('\1') + String('\2');

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
  for(int i = 0; i < NUMPIXELS; i++){ // apago todo los neopixel
    pixels.setPixelColor(i, _r, _g, _b);
  }
  pixels.show();
}

void defalutNeoPixel(){
  cambiarColorUniformeNeoPixel(0, 0 , 0);
}

// EFECTOS //

void relampago() {
  unsigned long currentMillis = millis();

  switch (etapaActual) {
    case 0:
      if (currentMillis > 0){
        cambiarColorUniformeNeoPixel(255, 0, 0);
        etapaActual++;
        previousMillis = currentMillis;
      }
      break;
    case 1:
      if (currentMillis - previousMillis >= 3000) {
        cambiarColorUniformeNeoPixel(255, 255, 255);
        etapaActual++;
        previousMillis = currentMillis;
      }
      break;
    case 2:
      if (currentMillis - previousMillis >= 25) {
        cambiarColorUniformeNeoPixel(255, 0, 0);
        etapaActual++;
        previousMillis = currentMillis;
      }
      break;
    case 3:
      if (currentMillis - previousMillis >= 50) {
        cambiarColorUniformeNeoPixel(255, 255, 255);
        etapaActual++;
        previousMillis = currentMillis;
      }
      break;
    case 4:
      if (currentMillis - previousMillis >= 25) {
        defalutNeoPixel();
        efectoActivo = false;
      }
      break;
  }
}

void cieloInfierno() {
  static unsigned long startMillis = 0;
  static int msegundos = 0;

  switch (etapaActual){
    case 0:
      msegundos = random(1000, 6000);
      startMillis = millis();
      break;
    case 1:
      if (millis() - startMillis > msegundos){
        setEfecto(RELAMPAGO);
      }
  }
}

void cielo() {
  cambiarColorUniformeNeoPixel(80, 255, 80);
  efectoActivo = false;
}

void rayo() {
  unsigned long currentMillis = millis();

  switch (etapaActual) {
    case 0:
      if (currentMillis > 0){
        cambiarColorIntRGB(61, 126, 255);
        etapaActual++;
        previousMillis = currentMillis;
      }
      break;
    case 1:
      if (currentMillis - previousMillis >= 400) {
        cambiarColorIntRGB(0, 0, 0);
        etapaActual++;
        previousMillis = currentMillis;
      }
      break;
    case 2:
      if (currentMillis - previousMillis >= 200) {
        cambiarColorIntRGB(61, 126, 255);
        etapaActual++;
        previousMillis = currentMillis;
      }
      break;
    case 3:
      if (currentMillis - previousMillis >= 400) {
        defaultRGB();
        efectoActivo = false;
      }
      break;
  }
}

void setEfecto(String e){
  efectoActual = e;
  efectoActivo = true;
  etapaActual = 0;
  previousMillis = millis();
}

void efecto(){
  if (efectoActual == RAYO) rayo();
  else if (efectoActual == CIELO) cielo();
  else if (efectoActual == CIELO_INFIERNO) cieloInfierno();
  else if (efectoActual == RELAMPAGO) relampago();
}

void setup() {
  pinMode(RED, OUTPUT);
  pinMode(GREEN, OUTPUT);
  pinMode(BLUE, OUTPUT);

  defaultRGB();

  pixels.begin();
  cambiarColorUniformeNeoPixel(0, 0, 0);

  Serial.begin(9600);
}

void loop() {
  if (efectoActivo) efecto();
  if (Serial.available() > 0) {
    String colores = Serial.readString();//Si tiene 2 caracteres, si empieza en 0 es un efecto de luces RGB, si empieza en 1 es un efecto de neopixel. Si tiene 3 caracteres, cada caracter representa un color (RGB).
    if (colores.length() == 2) setEfecto(colores);
    if (colores.length() == 3) cambiarColorRGB(colores);
  }
}
