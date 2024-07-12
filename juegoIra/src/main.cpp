#include <Arduino.h>

//puertos esp
#define botonEmpezar1 25
#define botonGanar1 27
#define botonEmpezar2 14
#define botonGanar2 12

#define botonPerder 26

#define REDled 23
#define YELLOWled 22
#define GREENled 21

//variables
unsigned long int tiempo1;
unsigned long int tiempo2;
unsigned long int diferencia;

int estadoJugador1 = 0;
int estadoJugador2 = 0;

int ledStateRed = 0;
int ledStateYellow = 0;
int ledStateGreen = 0;



void setup()
{
  Serial.begin(9600);
  pinMode(botonEmpezar1, INPUT_PULLUP);
  pinMode(botonGanar1, INPUT_PULLUP);
  pinMode(botonEmpezar2, INPUT_PULLUP);
  pinMode(botonGanar2, INPUT_PULLUP);
  pinMode(botonPerder, INPUT_PULLUP);
  pinMode(REDled, OUTPUT);
  pinMode(YELLOWled, OUTPUT);
  pinMode(GREENled, OUTPUT);
}

bool listoEmpezar = false;

void terminarJuego(){
  listoEmpezar = false;
  

  tiempo1 = 1;
  tiempo2 = 1000000;
  diferencia = 1000000;

  int estadoJugador1 = 0;
  int estadoJugador2 = 0;

  int ledStateRed = 0;
  int ledStateYellow = 0;
  int ledStateGreen = 0;

  digitalWrite(REDled, LOW);
  digitalWrite(YELLOWled, LOW);
  digitalWrite(GREENled, LOW);
}

void notificarTermino(){
  Serial.print('0');
}

void recibirInfo(){
  if (Serial.available() > 0){
    char info = Serial.read();
    switch (info){
      case '0'://iniciar
        listoEmpezar = true;
        break;
      case '1'://terminar
        terminarJuego();
        break;
      case '2'://reiniciar
        terminarJuego();
        listoEmpezar = true;
      default:
        break;
    }
  }
}

void empezar(){
  ledStateRed = 1;
  digitalWrite(REDled, ledStateRed);
  ledStateYellow = 0;
  digitalWrite(YELLOWled, ledStateYellow);
}

void perder(){
  ledStateYellow = 1;
  digitalWrite(YELLOWled, ledStateYellow);
  ledStateRed = 0;
  digitalWrite(REDled, ledStateRed);
}

void ganarJ1(){
  tiempo1=millis();
  estadoJugador1 = 1;
}

void ganarJ2(){
  tiempo2=millis();
  estadoJugador2 = 1;
}

void calcularDiferencia(){
  diferencia=tiempo1-tiempo2;
  if(diferencia<0){
    diferencia=diferencia*-1;
  }
}

void ganar(){
  ledStateGreen = 1;
  digitalWrite(GREENled, ledStateGreen);
  ledStateRed = 0;
  digitalWrite(REDled, ledStateRed);
  
  delay(3000);

  terminarJuego();
  notificarTermino();
}

void perderXTiempo(){
  perder();
  tiempo1=10;
  tiempo2=100001;
  estadoJugador1=0;
  estadoJugador2=0;
}

void loop()
{
  recibirInfo();

  if (listoEmpezar){
    int botonEmpezarState1 = !digitalRead(botonEmpezar1);
    int botonPerderState = !digitalRead(botonPerder);
    int botonGanarState1 = !digitalRead(botonGanar1);
    int botonEmpezarState2 = !digitalRead(botonEmpezar2);
    int botonGanarState2 = !digitalRead(botonGanar2);


    if (botonEmpezarState1 == HIGH && botonEmpezarState2 == HIGH){
      empezar();
    }

    if (botonPerderState == HIGH){
      perder();
    }

    if ((botonGanarState1 == HIGH) && (ledStateYellow == LOW) && (estadoJugador1 == LOW)){
      ganarJ1();
    }

    if ((botonGanarState2 == HIGH) && (ledStateYellow == LOW) && (estadoJugador2 == LOW)){
      ganarJ2();
    }

    if (estadoJugador1==HIGH && estadoJugador2==HIGH){
      calcularDiferencia();
      if(diferencia<=1000){
        ganar();
      } else {
        perderXTiempo();
      }
    }
  }

  delay(100); 
}