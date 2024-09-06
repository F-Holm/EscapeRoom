#include <SPI.h>
#include <MFRC522.h>
#include <Adafruit_NeoPixel.h>
#include <avr/power.h>

#define RST_PIN 9 // Configurable, see typical pin layout above
#define SS_1_PIN 10 // Configurable, take a unused pin, only HIGH/LOW required, must be different to SS 2
#define SS_2_PIN 8 // Configurable, take a unused pin, only HIGH/LOW required, must be different to SS 1

#define NR_OF_READERS 2

#define BOTON 3
#define LED_BOTON 2

byte ssPins[] = {SS_1_PIN, SS_2_PIN};
 
MFRC522 mfrc522[NR_OF_READERS];
#define PIN 5
#define NUMPIXELS 5
String tags[]={"",""};
Adafruit_NeoPixel pixels = Adafruit_NeoPixel(NUMPIXELS, PIN, NEO_GRB + NEO_KHZ800); //nos permite controlar la tira con funciones de la libreria neopixel

enum Codigos {
  RFID_START = 0,
  RFID_RESTART = 1,
  RFID_STOP = 2,
  CLOSE = 3,
  RFID_TERMINO = 4,

  BOTON_START = 160,
  BOTON_RESTART = 161,
  BOTON_STOP = 162,
  BOTON_TERMINO = 163,

  PAREJAS_BASE = 192//192 + cantParejasCorrectas = código
};

struct Boton{
  int anterior;
  bool encendido;
  int intervalo = 400;
  bool iniciado;

  void setParpadear(){
    anterior = millis();
    encendido = true;
    digitalWrite(LED_BOTON, HIGH);
  }

  bool debeParpadear(){
    return (millis() - anterior > intervalo && iniciado);
  }

  void parpadear(){
    if (!debeParpadear()) return;
    anterior = millis();
    if (encendido)
    {
      encendido = false;
      digitalWrite(LED_BOTON, LOW);
    }
    else{
      encendido = true;
      digitalWrite(LED_BOTON, HIGH);
    }
  }

  void termino(){
    Serial.print(Codigos::BOTON_TERMINO);
    iniciado = false;
    digitalWrite(LED_BOTON, LOW);
  }

} boton;

struct RFID{
  int anterior;
  bool encendido;
  int cantParpadeos;
  int r;
  int g;
  int b;
  int intervalo = 400;
  bool iniciado;

  bool estadoParejas[NUMPIXELS] = {false, false, false, false, false}; // Estado de cada pareja (si fue ingresada o no)
  int contadorParejasCorrectas = 0; // Contador de parejas correctas

  // Define las parejas de tags aquí
  const String parejas[5][2] = {
  {"b3958b17", "a052f279"}, // Pareja 1
  {"c32af216", "18b061c9"}, // Pareja 2
  {"98765432", "fedcba98"}, // Pareja 3
  {"87654321", "1234abcd"}, // Pareja 4
  {"11223344", "55667788"} // Pareja 5
  };

  void setVariables(){
    for (int i = 0;i < NUMPIXELS;i++) estadoParejas[i] = false;
    contadorParejasCorrectas = 0;
    terminarParpadeo();
  }

  void setParpadear(int _cant, int _r, int _g, int _b){
    anterior = millis();
    cantParpadeos = _cant;
    r = _r;
    g = _g;
    b = _b;
    encendido = true;
    cambiarColorUniforme(r, g, b);
  }

  bool debeParpadear(){
    return (millis() - anterior > intervalo || cantParpadeos > 0) && iniciado;
  }

  void parpadear(){
    if (!debeParpadear()) return;
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

  terminarParpadeo(){
    cantParpadeos = 0;
    encendido = false;
    cambiarColorUniforme(0, 0, 0);
  }

  void termino(){
    Serial.print(Codigos::RFID_TERMINO);
    iniciado = false;
  }

  void cambiarColorUniforme(int _r, int _g, int _b){
    for(int i = 0; i < NUMPIXELS; i++){ // apago todo los neopixel
      pixels.setPixelColor(i, _r, _g, _b);
    }
    pixels.show();
  }

  void setRespuestasCorrectasNeopixel(){
    rfid.cantParpadeos = 0;
    for (int i = 0; i < NUMPIXELS; i++){
      if (i < contadorParejasCorrectas) pixels.setPixelColor(i, pixels.Color(0, 255, 0));
      else pixels.setPixelColor(i, pixels.Color(0, 0, 0));

    }
    pixels.show();
  }

  void verificarCombinacion() {
    for (int i = 0; i < NUMPIXELS; i++) {
    // Comprobar si los tags leídos corresponden a una pareja y si no han sido utilizados
      if ((tags[0] == parejas[i][0] && tags[1] == parejas[i][1]) || (tags[0] == parejas[i][1] && tags[1] == parejas[i][0])) {
        if (!estadoParejas[i]) { // Si la pareja no ha sido ingresada
          estadoParejas[i] = true; // Marcamos la pareja como ingresada
          contadorParejasCorrectas++; // Aumentamos el contador
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

} rfid;

void recibirDatos(){
  if (Serial.available() > 0){
    int info = Serial.read();
    switch (info){
      case Codigos::RFID_START://iniciar
        rfid.iniciado = true;
        setVariables();
        break;
      case Codigos::RFID_RESTART://reiniciar
        setVariables();
        break;
      case Codigos::RFID_STOP://terminar
        rfid.iniciado = false;
        break;
      case Codigos::BOTON_START://iniciar
        boton.iniciado = true;
        break;
      case Codigos::BOTON_RESTART://reiniciar
        break;
      case Codigos::BOTON_STOP://detener
        boton.iniciado = false;
        break;
    }
  }
}

void setup() {
  pinMode(BOTON, INPUT_PULLUP);//No se si es INPUT o INPUT_PULLUP
  pinMode(LED_BOTON, OUTPUT);
  
  Serial.begin(9600); // Initialize serial communications with the PC
  //while (!Serial); // Do nothing if no serial port is opened (added for Arduinos based on ATMEGA32U4)

  SPI.begin(); // Init SPI bus

  for (uint8_t reader = 0; reader < NR_OF_READERS; reader++) {
    mfrc522[reader].PCD_Init(ssPins[reader], RST_PIN); // Init each MFRC522 card
    mfrc522[reader].PCD_DumpVersionToSerial();
  }

  pixels.begin();

  rfid.cambiarColorUniforme(0, 0, 0);
}


void loop() {
  recibirDatos();
  //rfid.iniciado = true;

  if (rfid.iniciado){
    rfid.parpadear();
    Serial.print(rfid.contadorParejasCorrectas + Codigos::PAREJAS_BASE);

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
    if (rfid.contadorParejasCorrectas == NUMPIXELS) rfid.termino();
  } else if (boton.iniciado && digitalRead(BOTON)){
    boton.termino();
  } else if (boton.iniciado){
    boton.parpadear();
  }
}