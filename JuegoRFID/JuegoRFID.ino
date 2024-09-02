#include <SPI.h>
#include <MFRC522.h>
#include <Adafruit_NeoPixel.h>
#include <avr/power.h>

#define RST_PIN 9 // Configurable, see typical pin layout above
#define SS_1_PIN 10 // Configurable, take a unused pin, only HIGH/LOW required, must be different to SS 2
#define SS_2_PIN 8 // Configurable, take a unused pin, only HIGH/LOW required, must be different to SS 1

#define NR_OF_READERS 2

#define boton 3
#define ledBoton 2

byte ssPins[] = {SS_1_PIN, SS_2_PIN};
 
MFRC522 mfrc522[NR_OF_READERS];
#define PIN 5
#define NUMPIXELS 5
String tags[]={"",""};
Adafruit_NeoPixel pixels = Adafruit_NeoPixel(NUMPIXELS, PIN, NEO_GRB + NEO_KHZ800); //nos permite controlar la tira con funciones de la libreria neopixel

// Define las parejas de tags aquí
const String parejas[5][2] = {
{"b3958b17", "a052f279"}, // Pareja 1
{"c32af216", "18b061c9"}, // Pareja 2
{"98765432", "fedcba98"}, // Pareja 3
{"87654321", "1234abcd"}, // Pareja 4
{"11223344", "55667788"} // Pareja 5
};

enum Codigos {
  START_RFID = 0,
  RESTART_RFID = 1,
  STOP_RFID = 2,
  CLOSE = 3,
  TERMINO_RFID = 4,
  START_BOTON = 5,
  RESTART_BOTON = 6,
  STOP_BOTON = 7,
  TERMINO_BOTON = 8
};

bool estadoParejas[NUMPIXELS] = {false, false, false, false, false}; // Estado de cada pareja (si fue ingresada o no)
int contadorParejasCorrectas = 0; // Contador de parejas correctas

bool juegoBotonIniciado = false;
bool juegoRFIDIniciado = false;

unsigned long int anterior = 0;
bool encendido = false;
int cantParpadeos = 0;
int r;
int g;
int b;

void setParpadear(int _cant, int _r, int _g, int _b){
  anterior = millis();
  cantParpadeos = _cant;
  r = _r;
  g = _g;
  b = _b;
}

void recibirDatos(){
  if (Serial.available() > 0){
    int info = Serial.read();
    switch (info){
      case Codigos::START_RFID://iniciar
        juegoRFIDIniciado = true;
        setVariables();
        break;
      case Codigos::RESTART_RFID://reiniciar
        setVariables();
        break;
      case Codigos::STOP_RFID://terminar
        juegoRFIDIniciado = false;
        break;
      case Codigos::START_BOTON://iniciar
        juegoBotonIniciado = true;
        break;
      case Codigos::RESTART_BOTON://reiniciar
        break;
      case Codigos::STOP_BOTON://detener
        juegoBotonIniciado = false;
        break;
    }
  }
}

void terminoBoton(){
  Serial.print(Codigos::TERMINO_BOTON);
  juegoBotonIniciado = false;
  digitalWrite(ledBoton, LOW);
}

void terminoRFID(){
  Serial.print(Codigos::TERMINO_RFID);
  juegoRFIDIniciado = false;
}

void setVariables(){
  for (int i = 0;i < NUMPIXELS;i++) estadoParejas[i] = false;
  contadorParejasCorrectas = 0;
  cantParpadeos = 0;
}

void cambiarColorUniforme(int _r, int _g, int _b){
  for(int i = 0; i < NUMPIXELS; i++){ // apago todo los neopixel
    pixels.setPixelColor(i, _r, _g, _b);
  }
  pixels.show();
}

void setRespuestasCorrectasNeopixel(){
  cantParpadeos = 0;
  for (int i = 0; i < NUMPIXELS; i++){
    if (i < contadorParejasCorrectas) pixels.setPixelColor(i, pixels.Color(0, 255, 0));
    else pixels.setPixelColor(i, pixels.Color(0, 0, 0));

  }
  pixels.show();
}

// Función para parpadear los LEDs en rojo
void parpadear() {
  if(cantParpadeos == 0) return;
  if(millis() - anterior < 400) return;
  anterior = millis();
  if (encendido)
  {
    encendido = false;
    cambiarColorUniforme(0, 0, 0);
    cantParpadeos--;
    if(cantParpadeos == 0){
      setRespuestasCorrectasNeopixel();
    }
  }
  else{
    encendido = true;
    cambiarColorUniforme(r, g, b);
  }
}

void setup() {
  setVariables();
  pinMode(boton, INPUT_PULLUP);//No se si es INPUT o INPUT_PULLUP
  pinMode(ledBoton, OUTPUT);
  
  Serial.begin(9600); // Initialize serial communications with the PC
  //while (!Serial); // Do nothing if no serial port is opened (added for Arduinos based on ATMEGA32U4)

  SPI.begin(); // Init SPI bus

  for (uint8_t reader = 0; reader < NR_OF_READERS; reader++) {
    mfrc522[reader].PCD_Init(ssPins[reader], RST_PIN); // Init each MFRC522 card
    mfrc522[reader].PCD_DumpVersionToSerial();
  }

  

  pixels.begin();
  //pruebaLEDs();
  cambiarColorUniforme(0, 0, 0);
}
 
void verificarCombinacion() {
  //Serial.println(tags[0] + "     " + tags[1]);
  for (int i = 0; i < NUMPIXELS; i++) {
  // Comprobar si los tags leídos corresponden a una pareja y si no han sido utilizados
    if ((tags[0] == parejas[i][0] && tags[1] == parejas[i][1]) || (tags[0] == parejas[i][1] && tags[1] == parejas[i][0])) {
      if (!estadoParejas[i]) { // Si la pareja no ha sido ingresada
        estadoParejas[i] = true; // Marcamos la pareja como ingresada
        contadorParejasCorrectas++; // Aumentamos el contador
        //Serial.println("true");
        // Encender el LED correspondiente
        
        setRespuestasCorrectasNeopixel();

        // Reseteamos las variables después de una combinación correcta
        tags[0] = "";
        tags[1] = "";
        return; // Salimos de la función
      } else { // si la pareja ya se ingresó
        setParpadear(2, 255, 96, 0);
      }
    }
  }
  // Si se leyeron ambos tags pero no corresponden a una pareja válida
  if (tags[0] != "" && tags[1] != "") {
    setParpadear(2, 255, 0, 0);
    // probar si aca hace falta que vuelva a poner en verde o se ponen solos
    // Reseteamos las variables después de una combinación incorrecta
    tags[0] = "";
    tags[1] = "";
  }
}

void loop() {
  parpadear();
  //recibirDatos();
  juegoRFIDIniciado = true;

  //if (tags[0] == "" && tags[1] == "") Serial.println(tags[0] + "\t" + tags[1]);
  if (juegoRFIDIniciado){
    for (uint8_t reader = 0; reader < NR_OF_READERS; reader++) {
      if (mfrc522[reader].PICC_IsNewCardPresent() && mfrc522[reader].PICC_ReadCardSerial()) {
        tags[reader]="";
        for (byte i = 0; i < mfrc522[reader].uid.size; i++) {
          tags[reader] += String(mfrc522[reader].uid.uidByte[i] < 0x10 ? "0" : "");
          tags[reader] += String(mfrc522[reader].uid.uidByte[i], HEX);
        }
        mfrc522[reader].PICC_HaltA();
        mfrc522[reader].PCD_StopCrypto1();
      }
    }
    verificarCombinacion();
    if (contadorParejasCorrectas == NUMPIXELS) terminoRFID();
  } else if (juegoBotonIniciado && digitalRead(boton)){
    terminoBoton();
  } else if (juegoBotonIniciado){
    digitalWrite(ledBoton, HIGH);
  }
}