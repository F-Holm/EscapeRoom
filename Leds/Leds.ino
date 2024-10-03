#include <Adafruit_NeoPixel.h>

#define PIN_1 11
#define PIN_2 10
#define PIN_3 9
#define NUMPIXELS_1 300
#define NUMPIXELS_2 208
#define NUMPIXELS_3 92

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

class RGB{
  public:
    static void cambiarColor(int r, int g, int b){
      analogWrite(RED, r);
      analogWrite(GREEN, g);
      analogWrite(BLUE, b);
    }

    static void cambiarColor(String rgb) {
      analogWrite(RED, rgb[0]);
      analogWrite(GREEN, rgb[1]);
      analogWrite(BLUE, rgb[2]);
      color = rgb;
    }

    static void cambiarColorSinGuardar(String rgb) {
      analogWrite(RED, rgb[0]);
      analogWrite(GREEN, rgb[1]);
      analogWrite(BLUE, rgb[2]);
    }

    static void defaultColor(){
      analogWrite(RED, color[0]);
      analogWrite(GREEN, color[1]);
      analogWrite(BLUE, color[2]);
    }
};

class NEOPIXEL{
  public:
    static void cambiarColorUniforme(int _r, int _g, int _b){
      cambiarColorUniforme1(_r, _g, _b);
      cambiarColorUniforme2(_r, _g, _b);
      cambiarColorUniforme3(_r, _g, _b);
    }

    static void cambiarColorUniforme1(int _r, int _g, int _b){
      for(int i = 0; i < NUMPIXELS_1; i++){
        pixels_1.setPixelColor(i, _r, _g, _b);
      }
      pixels_1.show();
    }

    static void cambiarColorUniforme2(int _r, int _g, int _b){
      for(int i = 0; i < NUMPIXELS_2; i++){
        pixels_2.setPixelColor(i, _r, _b, _g);
      }
      pixels_2.show();
    }

    static void cambiarColorUniforme3(int _r, int _g, int _b){
      for(int i = 0; i < NUMPIXELS_3; i++){
        pixels_3.setPixelColor(i, _r, _b, _g);
      }
      pixels_3.show();
    }

    static void defalutNeoPixel(){
      cambiarColorUniforme(0, 0 , 0);
    }
    
    static void cambiarColorCantidad1(int pinInicial, int cantidad, int _r, int _g, int _b){
      for(int i = pinInicial; i < pinInicial+cantidad; i++){
        pixels_1.setPixelColor(i, _r, _b, _g);
      }
      pixels_1.show();
    }
    static void cambiarColorCantidad2(int pinInicial, int cantidad, int _r, int _g, int _b){
      for(int i = pinInicial; i < pinInicial+cantidad; i++){
        pixels_2.setPixelColor(i, _r, _b, _g);
      }
      pixels_2.show();
    }
    static void cambiarColorCantidad3(int pinInicial, int cantidad, int _r, int _g, int _b){
      for(int i = pinInicial; i < pinInicial+cantidad; i++){
        pixels_3.setPixelColor(i, _r, _b, _g);
      }
      pixels_3.show();
    }

    static void rojoVariado1(){
      int segmento=30;
      for(int i=0; i<NUMPIXELS_1;i=i+segmento){
        if(i ){
          cambiarColorCantidad1(i, segmento, 255,0,0);
        }
      }
    }
};

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

  RGB::defaultColor();

  pixels_1.begin();
  pixels_2.begin();
  pixels_3.begin();
  NEOPIXEL::cambiarColorUniforme(0, 0, 0);

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
  NEOPIXEL::cambiarColorUniforme(255, 0, 0);
  //RGB::cambiarColor(255, 0, 0);
}
