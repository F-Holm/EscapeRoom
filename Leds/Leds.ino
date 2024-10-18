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
      analogWrite(RED, _r); r = _r;
      analogWrite(GREEN, _g); g = _g;
      analogWrite(BLUE, _b); b = _b;
    }

    static void defaultColor(){
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
      if (e == 3 || e == 4) n = 0;
      efectoActual = e;
      etapaActual = 0;
      previousMillis = millis();
    }

    static void apagado() {
      for(int i = 0; i < NUM_LEDS;i++){
        leds[i] = CRGB(0, 0, 0);
      }
      FastLED.show();
      RGB::cambiarColor(0, 0, 0);
      n = 0;
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
      
      if (n == 255 && prendiendo) prendiendo = false;
      else if (n == 0 && !prendiendo) prendiendo = true;
      n = (prendiendo ? n + 1 : n - 1);
      RGB::cambiarColor(n, 0, 0);

      //if (previousMillis + 2000 <= millis()) set(3);
    }

    static void encendidoGradual() {
      unsigned int tiempo = millis();

      for (int veces=0;veces<random(0,15);veces++)
      {
        int pos = random16(NUM_LEDS);
        leds[pos] = CRGB( 255, random(0,60), 0);
      }
      FastLED.show();
      
      if (previousMillis + n*(5670/255) <= millis()){
        RGB::cambiarColor(n, 0, 0);
        n++;
      }
      if (previousMillis + 5670 <= millis()) {
        set(1);
        n = 0;
      }

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

      for (int veces=0;veces<random(0,15);veces++)
      {
        int pos = random16(NUM_LEDS);
        if(pos < 100) leds[pos] = CRGB(160, 160, 255);
        else leds[pos] = CRGB(70, 70, 255);
      }
      
      FastLED.show();

      if (previousMillis + n*(4000/255) <= millis()){
        RGB::cambiarColor((n > RGB::r ? n : RGB::r), (n > 180 ? 180 : n), (n > 200 ? 200 : n));
        n++;
      }
      if (previousMillis + 4000 <= millis()) {
        n = 0;
        set(5);
      }
    }

    static void perdiste() {
      unsigned int tiempo = millis();

      for (int veces=0;veces<random(0,15);veces++)
      {
        int pos = random16(NUM_LEDS);
        leds[pos] = CRGB(255, 0, 0);
      }
      
      FastLED.show();

      if (previousMillis + n*(4000/255) <= millis()){
        RGB::cambiarColor((n > RGB::r ? n : RGB::r), 0, 0);
        n++;
      }
      if (previousMillis + 4000 <= millis()) {
        n = 0;
        set(7);
      }
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
