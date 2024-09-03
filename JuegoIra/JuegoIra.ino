#include <Adafruit_NeoPixel.h>

//puertos arduino
#define BOTON_EMPEZAR_1 7
#define BOTON_EMPEZAR_2 4

#define BOTON_GANAR_1 5
#define BOTON_GANAR_2 6

#define BOTON_PERDER_1 8
#define BOTON_PERDER_2 9

#define PIN_NEOPIXEL 10
#define CANT_PIXELES 2

bool estadoJugador1 = false;
bool estadoJugador2 = false;

Adafruit_NeoPixel pixel = Adafruit_NeoPixel(CANT_PIXELES, PIN_NEOPIXEL, NEO_GRB + NEO_KHZ800);

bool listoEmpezar = false;

bool ledGanar = false;
unsigned int tiempoLedGanar = 0;

bool perdio = false;

enum Codigos {
  START = 0,
  RESTART = 1,
  STOP = 2,
  CLOSE = 3,
  TERMINO = 4,
  JUGANDO = 176,
  PERDIERON = 177,
  TERMINO_J1 = 178,
  TERMINO_J2 = 179
};

void setup()
{
  Serial.begin(9600);

  pinMode(BOTON_EMPEZAR_1, INPUT_PULLUP);
  pinMode(BOTON_EMPEZAR_2, INPUT_PULLUP);
  pinMode(BOTON_GANAR_1, INPUT_PULLUP);
  pinMode(BOTON_GANAR_2, INPUT_PULLUP);
  pinMode(BOTON_PERDER_1, INPUT_PULLUP);
  pinMode(BOTON_PERDER_2, INPUT_PULLUP);

  pixel.begin(); 
  pixel.show();
}

void setLed1(int r, int g, int b){
  pixel.setPixelColor(0, pixel.Color(r, g, b));
  pixel.show();
}

void setLed2(int r, int g, int b){
  pixel.setPixelColor(1, pixel.Color(r, g, b));
  pixel.show();
}

void setLeds(int r, int g, int b){
  pixel.setPixelColor(0, pixel.Color(r, g, b));
  pixel.setPixelColor(1, pixel.Color(r, g, b));
  pixel.show();
}

void terminarJuego(){
  listoEmpezar = false;
  perdio = true;

  int estadoJugador1 = false;
  int estadoJugador2 = false;

  setLeds(0, 0, 0);
}

void notificarTermino(){
  listoEmpezar = false;
  Serial.print(Codigos::TERMINO);
}

void recibirInfo(){
  if (Serial.available() > 0){
    int info = Serial.read();
    switch (info){
      case Codigos::START://iniciar
        listoEmpezar = true;
        perdio = true;
        break;
      case Codigos::RESTART://reiniciar
        terminarJuego();
        listoEmpezar = true;
        break;
      case Codigos::STOP://terminar
        terminarJuego();
        break;
    }
  }
}

void empezar(){
  ledGanar = false;
  setLeds(0, 0, 255);
  perdio = false;
  Serial.print(Codigos::PERDIERON)
}

void perder(){
  setLeds(255, 0, 0);
  perdio = true;
  Serial.print(Codigos::PERDIERON);
}

void ganarJ1(){
  estadoJugador1 = true;
  setLed1(0, 255, 0);
  Serial.print(Codigos::TERMINO_J1);
}

void ganarJ2(){
  estadoJugador2 = true;
  setLed2(0, 255, 0);
  Serial.print(Codigos::TERMINO_J2)
}

void ganar(){
  setLeds(0, 255, 0);
  ledGanar = true;
  tiempoLedGanar = millis();
  perdio = false;

  terminarJuego();
  notificarTermino();
}

void loop()
{
  recibirInfo();
  
  if (ledGanar && millis() - tiempoLedGanar > 5000){
    setLeds(0, 0, 0);
    ledGanar = false;
  }

  if (listoEmpezar){
    bool botonEmpezarState1 = !digitalRead(BOTON_EMPEZAR_1);
    bool botonPerderState1 = !digitalRead(BOTON_PERDER_1);
    bool botonPerderState2 = !digitalRead(BOTON_PERDER_2);
    bool botonGanarState1 = !digitalRead(BOTON_GANAR_1);
    bool botonEmpezarState2 = !digitalRead(BOTON_EMPEZAR_2);
    bool botonGanarState2 = !digitalRead(BOTON_GANAR_2);


    if (botonEmpezarState1 && botonEmpezarState2){
      empezar();
    }

    if (botonPerderState1 || botonPerderState2 || perdio){
      perder();
    }

    if (botonGanarState1 && !estadoJugador1 && !perdio){
      ganarJ1();
    }

    if (botonGanarState2 && !estadoJugador2  && !perdio){
      ganarJ2();
    }

    if (estadoJugador1 && estadoJugador2){
      ganar();
    }
  }
}
