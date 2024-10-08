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

unsigned int cantToques = 0;//cuantas veces tocó el alambre sin perder
const unsigned int cantVidas = 5;//Puede tocar n veces los alambres sin perder
const unsigned int msGodMode = 200;//Cuantos milisegundos tenés de inmunidad después de tocar un alambre
unsigned int ultToque = 0;

const unsigned int msDelayEntreNotificaciones = 1000;
unsigned int tiempoAnteriorNotificacion = millis();

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
  IDENTIFICATE = 5,
  ID = 6,
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

  /*while(true) {
    while (Serial.available() <= 0);
    int identificate = Serial.read();
    if (identificate == Codigos::IDENTIFICATE) { Serial.print(Codigos::ID); break; }
    else continue;
  }*/
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
}

void perder(){
  if (millis() - ultToque > msGodMode) {
    if (cantToques == cantVidas) {
      perdio = true;
      estadoJugador1 = false;
      estadoJugador2 = false;
      cantToques = 0;
    } else {
      cantToques++;
      ultToque = millis();
    }
  }
}

void ganarJ1(){
  estadoJugador1 = true;
  setLed1(0, 255, 0);
}

void ganarJ2(){
  estadoJugador2 = true;
  setLed2(0, 255, 0);
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
    else if (millis() - msDelayEntreNotificaciones >= tiempoAnteriorNotificacion){
      tiempoAnteriorNotificacion = millis();
      if (perdio) Serial.write(Codigos::PERDIERON);
      else if (estadoJugador1) Serial.write(Codigos::TERMINO_J1);
      else if (estadoJugador2) Serial.write(Codigos::TERMINO_J2);
      else Serial.write(Codigos::JUGANDO);
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
  }

  // Tests //
  /*
  if (!digitalRead(BOTON_EMPEZAR_1)) Serial.println("Empezó 1");
  if (!digitalRead(BOTON_PERDER_1)) Serial.println("Perdió 1");
  if (!digitalRead(BOTON_PERDER_2)) Serial.println("Perdió 2");
  if (!digitalRead(BOTON_GANAR_1)) Serial.println("Ganó 1");
  if (!digitalRead(BOTON_EMPEZAR_2)) Serial.println("Empezó 2");
  if (!digitalRead(BOTON_GANAR_2)) Serial.println("Ganó 2");
  */
}
