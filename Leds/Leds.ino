#include <Adafruit_NeoPixel.h>
 
 
#define PIN 8
#define NUMPIXELS 300
 
Adafruit_NeoPixel pixel = Adafruit_NeoPixel(NUMPIXELS, PIN, NEO_GRB + NEO_KHZ800);

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

// pines de cada color
const int redPin = 3;
const int greenPin = 5;
const int bluePin = 6;

// cantidad de juegos completados
//int juegosCompletados = 0;

// valor de cada color
int red = 0;
int green = 0;
int blue = 0;

void cambiarColor(int r, int g, int b){
  analogWrite(redPin, r); red = r;
  analogWrite(greenPin, g); green = g;
  analogWrite(bluePin, b); blue = b;
}

void cambiarColorSinGuardar(int r, int g, int b){
  analogWrite(redPin, r);
  analogWrite(greenPin, g);
  analogWrite(bluePin, b);
}

void rayo(){
  cambiarColorSinGuardar(61, 126, 255);
  delay(400);
  cambiarColorSinGuardar(0, 0, 0);
  delay(200);
  cambiarColorSinGuardar(61, 126, 255);
  delay(400);
  cambiarColorSinGuardar(red, green, blue);
}

void setup() {
  pinMode(redPin, OUTPUT);
  pinMode(greenPin, OUTPUT);
  pinMode(bluePin, OUTPUT);

  analogWrite(redPin, red);
  analogWrite(greenPin, green);
  analogWrite(bluePin, blue);

  pixel.begin(); 
  pixel.show();

  Serial.begin(9600);
}

void loop(){
  if (Serial.available() > 0) {
    String colores = Serial.readString();//Si tiene 2 caracteres es un efecto, Si tiene 3 es un color. El primer caracter define si es un efecto RGB (0) o si es un efecto de neo pixel (1). El segundo caracter de los efectos determina que efecto va a realizar
    if (colores.length() == 2 && colores[0] == 0 && colores[1] == 0) rayo();
    if (colores.length() == 2 && colores[0] == 1 && colores[1] == 0) cieloInfierno();
    if (colores.length() == 2 && colores[0] == 1 && colores[1] == 1) cielo();
    if (colores.length() == 3) cambiarColor(colores[0], colores[1], colores[2]);
  }
}