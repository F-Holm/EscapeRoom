#include <Adafruit_NeoPixel.h>

#define PIN 8
#define NUMPIXELS 300

#define RED 3
#define GREEN 5
#define BLUE 6

Adafruit_NeoPixel pixel = Adafruit_NeoPixel(NUMPIXELS, PIN, NEO_GRB + NEO_KHZ800);

unsigned int red = 0;
unsigned int green = 0;
unsigned int blue = 0;

unsigned long previousMillis = 0;  // Almacena el tiempo anterior
int relampagoState = 0;            // Estado para el efecto relámpago
int cieloInfiernoState = 0;        // Estado para cielo infierno
int rayoState = 0;                  // Estado para rayo

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

void rojo() {
  for (int i = 0; i < NUMPIXELS; i++) {
    pixel.setPixelColor(i, pixel.Color(255, 0, 0));
  }
  pixel.show();
}

void blanco() {
  for (int i = 0; i < NUMPIXELS; i++) {
    pixel.setPixelColor(i, pixel.Color(255, 255, 255));
  }
  pixel.show();
}

void relampago() {
  unsigned long currentMillis = millis();

  switch (relampagoState) {
    case 0:
      rojo();
      if (currentMillis - previousMillis >= 3000) {
        previousMillis = currentMillis;
        relampagoState = 1;
      }
      break;
    case 1:
      blanco();
      if (currentMillis - previousMillis >= 25) {
        previousMillis = currentMillis;
        relampagoState = 2;
      }
      break;
    case 2:
      rojo();
      if (currentMillis - previousMillis >= 50) {
        previousMillis = currentMillis;
        relampagoState = 3;
      }
      break;
    case 3:
      blanco();
      if (currentMillis - previousMillis >= 25) {
        previousMillis = currentMillis;
        relampagoState = 0; // Reinicia el ciclo
      }
      break;
  }
}

void cieloInfierno() {
  static unsigned long startMillis = 0;
  static int segundos = 0;
  static bool running = false;

  if (!running) {
    segundos = random(1000, 6000);
    Serial.println(segundos);
    startMillis = millis();
    running = true;
  }

  if (millis() - startMillis >= segundos) {
    relampago();
    running = false; // Finaliza la ejecución del efecto
  }
}

void cielo() {
  static unsigned long currentMillis = 0;
  static int cieloState = 0;
  static unsigned long lastChange = 0;

  switch (cieloState) {
    case 0:
      rojo();
      lastChange = millis();
      cieloState = 1;
      break;
    case 1:
      if (millis() - lastChange >= 1000) { // Mantiene el rojo por 1 segundo
        blanco();
        lastChange = millis();
        cieloState = 2;
      }
      break;
    case 2:
      if (millis() - lastChange >= 1000) { // Mantiene el blanco por 1 segundo
        cieloState = 0; // Reinicia el ciclo
      }
      break;
  }
}

void cambiarColor(int r, int g, int b) {
  analogWrite(RED, r); red = r;
  analogWrite(GREEN, g); green = g;
  analogWrite(BLUE, b); blue = b;
}

void cambiarColorSinGuardar(int r, int g, int b) {
  analogWrite(RED, r);
  analogWrite(GREEN, g);
  analogWrite(BLUE, b);
}

void rayo() {
  static unsigned long rayoMillis = 0;
  static int rayoState = 0;

  switch (rayoState) {
    case 0:
      cambiarColorSinGuardar(61, 126, 255);
      rayoMillis = millis();
      rayoState = 1;
      break;
    case 1:
      if (millis() - rayoMillis >= 400) {
        cambiarColorSinGuardar(0, 0, 0);
        rayoMillis = millis();
        rayoState = 2;
      }
      break;
    case 2:
      if (millis() - rayoMillis >= 200) {
        cambiarColorSinGuardar(61, 126, 255);
        rayoMillis = millis();
        rayoState = 3;
      }
      break;
    case 3:
      if (millis() - rayoMillis >= 400) {
        cambiarColorSinGuardar(red, green, blue);
        rayoState = 0; // Reinicia el ciclo
      }
      break;
  }
}

void loop() {
  if (Serial.available() > 0) {
    String colores = Serial.readString();
    if (colores.length() == 2 && colores[0] == '0' && colores[1] == '0') rayo();
    if (colores.length() == 2 && colores[0] == '1' && colores[1] == '0') cieloInfierno();
    if (colores.length() == 2 && colores[0] == '1' && colores[1] == '1') cielo();
    if (colores.length() == 3) cambiarColor(colores[0], colores[1], colores[2]);
  }
  
  relampago(); // Llama a relampago en el loop
  cielo(); // Llama a cielo en el loop
}
