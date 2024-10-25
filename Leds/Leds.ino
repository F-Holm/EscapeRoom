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

#define AGUA 7

class RGB{
  public:

    static int r;
    static int g;
    static int b;

    static void cambiarColor(int _r, int _g, int _b) {
      if (r != _r || g != _g || b != _b) {
        analogWrite(RED, _r); r = _r;
        analogWrite(GREEN, _g); g = _g;
        analogWrite(BLUE, _b); b = _b;
      }
    }

    static void cambiarColor(){
      analogWrite(RED, r);
      analogWrite(GREEN, g);
      analogWrite(BLUE, b);
    }
}; int RGB::r = 0; int RGB::g = 0; int RGB::b = 0;

class Efectos{
  public:

    static unsigned int previousMillis;
    static int efectoActual;
    static int etapaActual;
    static unsigned int n;

    static void set(int e){
      efectoActual = e;
      etapaActual = 0;
      previousMillis = millis();
      n = previousMillis;
    }

    static void apagado() {
      for(int i = 0; i < NUM_LEDS;i++){
        leds[i] = CRGB(0, 0, 0);
      }
      FastLED.show();
      RGB::cambiarColor(0, 0, 0);
      set(-1);
    }

    static void confetti() {
      static bool prendiendo = true;
      
      fadeToBlackBy( leds, NUM_LEDS, 20);
      for (int veces=0;veces<random(0,15);veces++)
      {
        int pos = random16(NUM_LEDS);
        leds[pos] += CRGB( 255, random(0,60), 0);
      }
      FastLED.show();
      
      if (RGB::r == 255 && prendiendo) prendiendo = false;
      else if (RGB::r == 0 && !prendiendo) prendiendo = true;
      RGB::cambiarColor((prendiendo ? RGB::r + 1 : RGB::r - 1), 0, 0);
    }

    static void encendidoGradual() {
      unsigned int tiempo = millis();

      for (int veces=0;veces<random(0,15);veces++)
      {
        int pos = random16(NUM_LEDS);
        leds[pos] = CRGB( 255, random(0,60), 0);
      }
      FastLED.show();
      
      if (previousMillis + RGB::r*(5670/255) <= millis()) RGB::cambiarColor((RGB::r <= 255 ? RGB::r + 1 : 255), RGB::g, RGB::b);
      if (previousMillis + 5670 <= millis()) set(1);
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
            RGB::cambiarColor(125, 90, 100);
            etapaActual++;
            previousMillis = tiempo;
          }
          break;
        case 1:
          if(tiempo >= previousMillis + 300){
            for(int i = 0; i < NUM_LEDS ;i++){
              leds[i] = CRGB(0, 0, 0);
            }
            FastLED.show();
            RGB::cambiarColor(0, 0, 0);
            previousMillis = tiempo;
            etapaActual++;
          }
          break;
        case 2:
          if(tiempo >= previousMillis + 100){
            for(int i=0; i<NUM_LEDS ;i++){
              if(i<100) leds[i] = CRGB(160, 160, 255);
              else leds[i] = CRGB(70,70,255);
            }
            FastLED.show();
            RGB::cambiarColor(125, 90, 100);
            previousMillis = tiempo;
            etapaActual++;
          }
          break;
        case 3:
          if(tiempo >= previousMillis + 300){
            for(int i=0; i<NUM_LEDS ;i++){
              leds[i] = CRGB(0, 0, 0);
            }
            FastLED.show();
            RGB::cambiarColor(0, 0, 0);
            previousMillis = tiempo;
            etapaActual++;
          }
          break;
        case 4:
          if(tiempo >= previousMillis + 100){
            for(int i=0; i<NUM_LEDS ;i++){
              if(i<100) leds[i] = CRGB(160, 160, 255);
              else leds[i] = CRGB(70, 70, 255);
            }
            FastLED.show();
            RGB::cambiarColor(125, 90, 100);
            etapaActual++;
            previousMillis = tiempo;
          }
          break;
        case 5:
          if(tiempo >= previousMillis + 300){
            for(int i = 0; i < NUM_LEDS ;i++){
              leds[i] = CRGB(0, 0, 0);
            }
            FastLED.show();
            RGB::cambiarColor(0, 0, 0);
            previousMillis = tiempo;
            etapaActual++;
          }
          break;
        case 6:
          if(tiempo >= previousMillis + 100){
            for(int i=0; i<NUM_LEDS ;i++){
              if(i<100) leds[i] = CRGB(160, 160, 255);
              else leds[i] = CRGB(70,70,255);
            }
            FastLED.show();
            RGB::cambiarColor(125, 90, 100);
            previousMillis = tiempo;
            etapaActual++;
          }
          break;
        case 7:
          if(tiempo >= previousMillis + 300){
            for(int i=0; i<NUM_LEDS ;i++){
              leds[i] = CRGB(0, 0, 0);
            }
            FastLED.show();
            RGB::cambiarColor(0, 0, 0);
            previousMillis = tiempo;
            etapaActual++;
          }
          break;
        case 8:
          if(tiempo >= previousMillis + 200) set(1);//default
          break;
      }
    }

    static void cierre() {
      unsigned int tiempo = millis();

      if (previousMillis + (6500/255) <= tiempo){
        for (int veces=0;veces<random(0,15);veces++)
        {
          int pos = random16(NUM_LEDS);
          if(pos < 100) leds[pos] = CRGB(160, 160, 255);
          else leds[pos] = CRGB(70, 70, 255);
        }
        FastLED.show();
        previousMillis = tiempo;
        RGB::cambiarColor((RGB::r >= 255 ? 255 : RGB::r + 1), (RGB::g >= 180 ? 180 : RGB::g + 1), (RGB::b >= 200 ? 200 : RGB::b + 1));
      }

      if (n + 6500 <= tiempo) set(5);
    }

    static void perdiste() {
      unsigned int tiempo = millis();

      if (previousMillis + (4000/255) <= tiempo){
        for (int veces=0;veces<random(0,15);veces++)
        {
          int pos = random16(NUM_LEDS);
          leds[pos] = CRGB(255, 0, 0);
        }
        FastLED.show();
        previousMillis = tiempo;
      }

      if (n + RGB::r*(4000/255) <= tiempo) RGB::cambiarColor((255 <= RGB::r ? 255 : RGB::r + 1), 0, 0);;
      if (n + 4000 <= tiempo) set(7);
    }

    static void blanco(){
      for(int i = 0; i < NUM_LEDS;i++){
        if (i < 100) leds[i] = CRGB(160, 160, 255);
        else leds[i] = CRGB(70, 70, 255);
      }
      FastLED.show();
      RGB::cambiarColor(255, 180, 200);
      set(-1);
    }

    static void rojo(){
      for(int i = 0; i < NUM_LEDS;i++){
        leds[i] = CRGB(255, 0, 0);
      }
      FastLED.show();
      RGB::cambiarColor(255, 0, 0);
      set(-1);
    }


}; unsigned int Efectos::previousMillis = 0; int Efectos::efectoActual = -1; int Efectos::etapaActual = -1; unsigned int Efectos::n = 0;

bool aguaActiva = false;
unsigned int inicioAgua = 0;

void setAgua(){
  aguaActiva = true;
  inicioAgua = millis();
  digitalWrite(AGUA, HIGH);
  //Serial.println("agua set");
}

void agua(){
  if (aguaActiva && inicioAgua + 300 <= millis()) {
    digitalWrite(AGUA, LOW);
    aguaActiva = false;
    //Serial.println("off");
  }
}

void efecto(){
  switch (Efectos::efectoActual){
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
      Efectos::cierre();
      break;
    case 4:
      Efectos::encendidoGradual();
      break;
    case 5:
      Efectos::blanco();
      break;
    case 6:
      Efectos::perdiste();
      break;
    case 7:
      Efectos::rojo();
      break;
  }
}

void setup() {
  FastLED.addLeds<LED_TYPE,11,BRG>(leds, NUM_LEDS).setCorrection(TypicalLEDStrip);
  FastLED.addLeds<LED_TYPE, 9, COLOR_ORDER>(leds, NUM_LEDS).setCorrection( TypicalLEDStrip );  
  FastLED.addLeds<LED_TYPE, 10, COLOR_ORDER>(leds, NUM_LEDS).setCorrection( TypicalLEDStrip );

  FastLED.setBrightness(BRIGHTNESS);

  pinMode(RED, OUTPUT);
  pinMode(GREEN, OUTPUT);
  pinMode(BLUE, OUTPUT);
  pinMode(AGUA, OUTPUT);

  Efectos::set(0);

  Serial.begin(9600);
  /*while(true) {
    while (Serial.available() <= 0);
    int identificate = Serial.read();
    if (identificate == 5) Serial.print(8);
    else continue;
  }*/
  //setAgua();
}

void loop() {
  if (Serial.available() > 0) {
    int efecto = Serial.read();
    if(efecto != 67) Efectos::set(efecto);
    else if (efecto == 67) setAgua();
  }
  efecto();
  agua();
}
