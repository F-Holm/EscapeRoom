#include <FastLED.h>
FASTLED_USING_NAMESPACE

#define LED_TYPE    WS2812
#define COLOR_ORDER GRB
#define NUM_LEDS    300
CRGB leds[300];
#define BRIGHTNESS          255
#define FRAMES_PER_SECOND  200

#define RED 3
#define GREEN 5
#define BLUE 6

class RGB{
  public:

    static String color;

    static void cambiarColorSinGuardar(int r, int g, int b){
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
}; String RGB::color = String('\255') + String('\0') + String('\0');

class Efectos{
  public:

    static unsigned int previousMillis;
    static int efectoActual;
    static int etapaActual;

    static void efecto(){
      switch (efectoActual){
        case 0:
          Efectos::apagado();
          break;
        case 1:
          Efectos::confetti();
          break;
        case 2:
          Efectos::lightning();
          break;
        case 3:
          Efectos::rayito();
          break;
        case 4:
          Efectos::encendidoGradual();
          break;
      }
    }

    static void setEfecto(int e){
      efectoActual = e;
      etapaActual = 0;
      previousMillis = millis();
    }

    static void apagado() {
      for(int i = 0; i < NUM_LEDS;i++){
        leds[i] = CRGB(0, 0, 0);
      }
      FastLED.show();
    }

    static void confetti() {
      fadeToBlackBy( leds, NUM_LEDS, 20);
      for (int veces=0;veces<random(0,15);veces++)
      {
        int pos = random16(NUM_LEDS);
        leds[pos] += CRGB( 255, random(0,60), 0);
      }
      FastLED.show(); 
    }

    static void encendidoGradual() {
      static int n = 0;
      unsigned int tiempo = millis();

      for (int veces=0;veces<random(0,15);veces++)
      {
        int pos = random16(NUM_LEDS);
        leds[pos] = CRGB( 255, random(0,60), 0);
      }
      FastLED.show();
      
      if (n == 0) RGB::cambiarColorSinGuardar(n, 0, 0);
      if (previousMillis + n*(5670/255) <= millis()){
        n++;
        RGB::cambiarColorSinGuardar(n, 0, 0);
        if (n == 255) n = 0;
      }
      if (previousMillis + 5670 <= millis()) setEfecto(1);

    }

    static void lightning(){
      unsigned int tiempo = millis();

      switch (etapaActual){
        case 0:
          if(true /*tiempo >= previousMillis + 800*/){
            for(int i=0; i<NUM_LEDS ;i++){
              if(i<100) leds[i] = CRGB(160, 160, 255);
              else leds[i] = CRGB(70, 70, 255);
            }
            FastLED.show();
            RGB::cambiarColorSinGuardar(125, 90, 100);
            etapaActual++;
            previousMillis = tiempo;
          }
          break;
        case 1:
          if(tiempo >= previousMillis + 800){
            for(int i = 0; i < NUM_LEDS ;i++){
              leds[i] = CRGB(0, 0, 0);
            }
            FastLED.show();
            RGB::cambiarColorSinGuardar(0, 0, 0);
            previousMillis = tiempo;
            etapaActual++;
          }
          break;
        case 2:
          if(tiempo >= previousMillis + 200){
            for(int i=0; i<NUM_LEDS ;i++){
              if(i<100) leds[i] = CRGB(160, 160, 255);
              else leds[i] = CRGB(70,70,255);
            }
            FastLED.show();
            RGB::cambiarColorSinGuardar(125, 90, 100);
            previousMillis = tiempo;
            etapaActual++;
          }
          break;
        case 3:
          if(tiempo >= previousMillis + 800){
            for(int i=0; i<NUM_LEDS ;i++){
              leds[i] = CRGB(0, 0, 0);
            }
            FastLED.show();
            RGB::cambiarColorSinGuardar(0, 0, 0);
            previousMillis = tiempo;
            etapaActual++;
          }
          break;
        case 4:
          Efectos::apagado();
          RGB::defaultColor();
          delay(3000);
          setEfecto(2);//default
          break;
      }
    }

    static void rayito() {int pos = random16(NUM_LEDS);
        leds[pos] += CRGB( 255, 255, 255);
      fadeToBlackBy( leds, NUM_LEDS, 20);
      for (int veces=0;veces<random(0,15);veces++)
      {
        int pos = random16(NUM_LEDS);
        leds[pos] += CRGB( 255, 255, 255);
      }
      FastLED.show(); 
    }
}; unsigned int Efectos::previousMillis = 0; int Efectos::efectoActual = -1; int Efectos::etapaActual = -1;



void setup() {
  FastLED.addLeds<LED_TYPE,11,BRG>(leds, NUM_LEDS).setCorrection(TypicalLEDStrip);
  FastLED.addLeds<LED_TYPE, 9, COLOR_ORDER>(leds, NUM_LEDS).setCorrection( TypicalLEDStrip );  
  FastLED.addLeds<LED_TYPE, 10, COLOR_ORDER>(leds, NUM_LEDS).setCorrection( TypicalLEDStrip );

  FastLED.setBrightness(BRIGHTNESS);

  pinMode(RED, OUTPUT);
  pinMode(GREEN, OUTPUT);
  pinMode(BLUE, OUTPUT);

  RGB::defaultColor();

  Serial.begin(9600);
  /*while(true) {
    while (Serial.available() <= 0);
    int identificate = Serial.read();
    if (identificate == 5) Serial.print(8);
    else continue;
  }*/
  Efectos::setEfecto(2);
}

void loop() {
  /*if (Serial.available() > 0) {
    String color = Serial.readString();//Si tiene 2 caracteres, si empieza en 0 es un efecto de luces RGB, si empieza en 1 es un efecto de neopixel. Si tiene 3 caracteres, cada caracter representa un color (RGB).
    if (color.length() == 1) Efectos::setEfecto(colores[0]);
    if (color.length() == 3) RGB::cambiarColor(colores);
  }*/
  Efectos::efecto();

}
