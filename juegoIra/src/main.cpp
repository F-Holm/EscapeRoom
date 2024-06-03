#include <Arduino.h>

//puertos esp
#define botonEmpezar1 25
#define botonGanar1 27
#define botonEmpezar2 14
#define botonGanar2 12

#define botonPerder 26

#define REDled1 23
#define YELLOWled1 22
#define GREENled 21
#define REDled2 19
#define YELLOWled2 18

//variables
unsigned long int tiempo1;
unsigned long int tiempo2;
unsigned long int diferencia;

int estadoJugador1 = 0;
int estadoJugador2 = 0;



void setup()
{
  Serial.begin(9600);
  pinMode(botonEmpezar1, INPUT_PULLUP);
  pinMode(botonGanar1, INPUT_PULLUP);
  pinMode(botonEmpezar2, INPUT_PULLUP);
  pinMode(botonGanar2, INPUT_PULLUP);
  pinMode(botonPerder, INPUT_PULLUP);
  pinMode(REDled1, OUTPUT);
  pinMode(YELLOWled1, OUTPUT);
  pinMode(GREENled, OUTPUT);
  pinMode(REDled2, OUTPUT);
  pinMode(YELLOWled2, OUTPUT);
}


void empezar(){
  ledStateRed = 1;
  digitalWrite(REDled1, ledStateRed);
  digitalWrite(REDled2, ledStateRed);
  ledStateYellow = 0;
  digitalWrite(YELLOWled1, ledStateYellow);
  digitalWrite(YELLOWled2, ledStateYellow);
}

void perder(){
  ledStateYellow = 1;
  digitalWrite(YELLOWled1, ledStateYellow);
  digitalWrite(YELLOWled2, ledStateYellow);
  ledStateRed = 0;
  digitalWrite(REDled1, ledStateRed);
  digitalWrite(REDled2, ledStateRed);
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
  digitalWrite(REDled1, ledStateRed);
  digitalWrite(REDled2, ledStateRed);
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
  
  delay(100);  
}