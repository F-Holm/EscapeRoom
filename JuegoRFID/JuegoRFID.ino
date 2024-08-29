#include <SPI.h>
#include <MFRC522.h>
#include <Adafruit_NeoPixel.h>
#include <avr/power.h>

#define RST_PIN 9 // Configurable, see typical pin layout above
#define SS_1_PIN 10 // Configurable, take a unused pin, only HIGH/LOW required, must be different to SS 2
#define SS_2_PIN 8 // Configurable, take a unused pin, only HIGH/LOW required, must be different to SS 1

#define NR_OF_READERS 2

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

bool estadoParejas[5] = {false, false, false, false, false}; // Estado de cada pareja (si fue ingresada o no)
int contadorParejasCorrectas = 0; // Contador de parejas correctas

void cambiarColorUniforme(int r, int g, int b){
  for(int i = 0; i < 5; i++){ // apago todo los neopixel
    pixels.setPixelColor(i, r, g, b);
  }
  pixels.show();
}

// Función para parpadear los LEDs en rojo
void parpadear(int r, int g, int b) {
  cambiarColorUniforme(r, g, b);
  delay(400);
  cambiarColorUniforme(0, 0, 0);
  delay(400);
  cambiarColorUniforme(r, g, b);
  delay(400);
  cambiarColorUniforme(0, 0, 0);
  delay(400);

  for (int i= 0; i<contadorParejasCorrectas; i++){
    pixels.setPixelColor(i, pixels.Color(0, 255, 0)); // Enciende el LED correspondiente en verde
    pixels.show();
  }
}
 
void setup() {
  Serial.begin(9600); // Initialize serial communications with the PC
  while (!Serial); // Do nothing if no serial port is opened (added for Arduinos based on ATMEGA32U4)

  SPI.begin(); // Init SPI bus

  for (uint8_t reader = 0; reader < NR_OF_READERS; reader++) {
    mfrc522[reader].PCD_Init(ssPins[reader], RST_PIN); // Init each MFRC522 card
    mfrc522[reader].PCD_DumpVersionToSerial();
  }

  pixels.begin();
  //pruebaLEDs();
  cambiarColorUniforme(0,0,0);
  Serial.println("Aproxime las tarjetas RFID a los lectores...");
}
 
void verificarCombinacion() {
  for (int i = 0; i < 5; i++) {
  // Comprobar si los tags leídos corresponden a una pareja y si no han sido utilizados
    if ((tags[0] == parejas[i][0] && tags[1] == parejas[i][1]) || (tags[1] == parejas[i][1] && tags[0] == parejas[i][0])) {
      if (!estadoParejas[i]) { // Si la pareja no ha sido ingresada
        Serial.println("¡Combinación correcta!");
        estadoParejas[i] = true; // Marcamos la pareja como ingresada
        contadorParejasCorrectas++; // Aumentamos el contador

        // Encender el LED correspondiente
        for (int i=0; i < contadorParejasCorrectas; i++) {
          pixels.setPixelColor(i, pixels.Color(0, 255, 0)); // Enciende el LED correspondiente en verde
          pixels.show();
        }

        Serial.print("Contador de parejas correctas: ");
        Serial.println(contadorParejasCorrectas);

        // Reseteamos las variables después de una combinación correcta
        tags[0] = "";
        tags[1] = "";
        return; // Salimos de la función
      } else { // si la pareja ya se ingresó
        Serial.println("La pareja ya fue ingresada.");
        parpadear(255, 96, 0); // se supone que parpadea en NARANJA
      }
    }
  }
  
  // Si se leyeron ambos tags pero no corresponden a una pareja válida
  if (tags[0] != "" && tags[1] != "") {
    Serial.println("Combinación incorrecta.");
    parpadear(255, 0, 0); // Parpadear LEDs en rojo al fallar

    // probar si aca hace falta que vuelva a poner en verde o se ponen solos

    // Reseteamos las variables después de una combinación incorrecta
    tags[0] = "";
    tags[1] = "";
  }
}
 
void loop() {
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
  if (tags[0] != "") {
    Serial.print("Tag 1 leído: "); Serial.println(tags[0]);
    delay(1000); // Espera para evitar múltiples lecturas del mismo tag
  }
  
  if (tags[1] != "") {
    Serial.print("Tag 2 leído: "); Serial.println(tags[1]);
    delay(1000); // Espera para evitar múltiples lecturas del mismo tag
  }
  
  
  verificarCombinacion();
}