#include <Adafruit_NeoPixel.h>
 
 
#define PIN 8
#define NUMPIXELS 300

#define RED = 3;
#define GREEN = 5;
#define BLUE = 6;
 
Adafruit_NeoPixel pixel = Adafruit_NeoPixel(NUMPIXELS, PIN, NEO_GRB + NEO_KHZ800);

unsigned int red = 0;
unsigned int green = 0;
unsigned int blue = 0;







struct EtapaEfecto
{
  unsigned int intervalo;
};

struct Efecto
{
  unsigned int anterior;
  EtapaEfecto rayo[] = {EtapaEfecto(r, g, b, i)};
  EtapaEfecto cielo[];
  EtapaEfecto cieloInfierno[];
};

void setup() {
  pinMode(RED, OUTPUT);
  pinMode(GREEN, OUTPUT);
  pinMode(BLUE, OUTPUT);

  analogWrite(RED, red);
  analogWrite(GREEN, green);
  analogWrite(BLUE, blue);

  pixel.begin(); 
  pixel.show();

  Serial.begin(9600);
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
  if(millis() - anterior >= 3000)  //delay(3000);
  blanco();
  delay(25);
  rojo();
  delay(50);
  blanco();
  delay(25);
  int anterior = millis();
}

void rojoVariable(int cantRojo){
  for (int i = 0; i < NUMPIXELS; i++) {
    pixel.setPixelColor(i, pixel.Color(cantRojo, 0, 0)); 
  }
  pixel.show(); 
}

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

void cambiarColor(int r, int g, int b){
  analogWrite(RED, r); red = r;
  analogWrite(GREEN, g); green = g;
  analogWrite(BLUE, b); blue = b;
}

void cambiarColorSinGuardar(int r, int g, int b){
  analogWrite(RED, r);
  analogWrite(GREEN, g);
  analogWrite(BLUE, b);
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



void loop(){
  if (Serial.available() > 0) {
    String colores = Serial.readString();//Si tiene 2 caracteres es un efecto, Si tiene 3 es un color. El primer caracter define si es un efecto RGB (0) o si es un efecto de neo pixel (1). El segundo caracter de los efectos determina que efecto va a realizar
    if (colores.length() == 2 && colores[0] == 0 && colores[1] == 0) rayo();
    if (colores.length() == 2 && colores[0] == 1 && colores[1] == 0) cieloInfierno();
    if (colores.length() == 2 && colores[0] == 1 && colores[1] == 1) cielo();
    if (colores.length() == 3) cambiarColor(colores[0], colores[1], colores[2]);
  }
}