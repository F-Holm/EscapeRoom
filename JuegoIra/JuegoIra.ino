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


//variables
unsigned long int tiempo1;
unsigned long int tiempo2;
unsigned long int diferencia;

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
  TERMINO = 4
};

void setup()
{
  listoEmpezar = true;
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
  
  tiempo1 = 1;
  tiempo2 = 1000000;
  diferencia = 1000000;

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
  setLeds(255, 0, 0);
  perdio = true;
}

void ganarJ1(){
  tiempo1=millis();
  estadoJugador1 = true;
  setLed1(0, 255, 0);
}

void ganarJ2(){
  tiempo2=millis();
  estadoJugador2 = true;
  setLed2(0, 255, 0);
}

void calcularDiferencia(){
  diferencia=tiempo1-tiempo2;
  if(diferencia<0) diferencia=diferencia*-1;
}

void ganar(){
  setLeds(0, 255, 0);
  ledGanar = true;
  tiempoLedGanar = millis();
  perdio = false;

  terminarJuego();
  notificarTermino();
}

void perderXTiempo(){
  perder();
  tiempo1=10;
  tiempo2=100001;
  estadoJugador1 = false;
  estadoJugador2 = false;
}

void loop()
{
  //recibirInfo();
  
  if (ledGanar && tiempoLedGanar - millis() > 5000){
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

    if (botonPerderState1 || botonPerderState2){
      perder();
    }

    if (botonGanarState1 && !estadoJugador1 && !perdio){
      ganarJ1();
    }

    if (botonGanarState2 && !estadoJugador2  && !perdio){
      ganarJ2();
    }

    if (estadoJugador1 && estadoJugador2){
      calcularDiferencia();
      if(diferencia<=1000) ganar();
      else perderXTiempo();
    }
  }
}
