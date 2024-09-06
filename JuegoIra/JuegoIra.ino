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
  //listoEmpezar = true; perdio = true;//Para tests
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
  Serial.print(Codigos::JUGANDO);
}

void perder(){
  perdio = true;
  estadoJugador1 = false;
  estadoJugador2 = false;
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
  Serial.print(Codigos::TERMINO_J2);
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
    perdio = true;
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

    if (perdio && botonEmpezarState1 && !botonEmpezarState2){
      setLed1(0, 0, 255);
      setLed2(255, 0, 0);
    } else if (perdio && !botonEmpezarState1 && botonEmpezarState2){
      setLed2(0, 0, 255);
      setLed1(255, 0, 0);
    } else if (perdio && !botonEmpezarState1 && !botonEmpezarState2) {
      setLeds(255, 0, 0);
    }

    if (botonPerderState1 && !estadoJugador1 || botonPerderState2 && !estadoJugador2){
      perder();
    }

    if (botonGanarState1 && !estadoJugador1 && !perdio){
      ganarJ1();
    }

    if (botonGanarState2 && !estadoJugador2 && !perdio){
      ganarJ2();
    }

    if (estadoJugador1 && estadoJugador2){
      ganar();
    }
  }

  //Tests
  /*if (!digitalRead(BOTON_EMPEZAR_1)) Serial.println("Empezó 1");
  if (!digitalRead(BOTON_PERDER_1)) Serial.println("Perdió 1");
  if (!digitalRead(BOTON_PERDER_2)) Serial.println("Perdió 2");
  if (!digitalRead(BOTON_GANAR_1)) Serial.println("Ganó 1");
  if (!digitalRead(BOTON_EMPEZAR_2)) Serial.println("Empezó 2");
  if (!digitalRead(BOTON_GANAR_2)) Serial.println("Ganó 2");*/
}
