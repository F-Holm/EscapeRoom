// pines de cada color
const int redPin = 3;
const int greenPin = 5;
const int bluePin = 6;

// cantidad de juegos completados
int juegosCompletados = 0;

// valor de cada color
int r = 255;
int g = 0;
int b = 0;


void setup() {
    pinMode(redPin, OUTPUT);
    pinMode(greenPin, OUTPUT);
    pinMode(bluePin, OUTPUT);

    analogWrite(redPin, r);
    analogWrite(greenPin, g);
    analogWrite(bluePin, b);

    Serial.begin(9600);
}

void loop(){
    // FALTA RECIBIR EL INT DE HOLM

    // 5 presets, 1 por cada etapa. Desde rojo hasta blanco
    switch(juegosCompletados) {
      case 1:
        g=63; b=63;
        analogWrite(greenPin, g);
        analogWrite(bluePin, b);
        break:
      case 2:
        g=127; b=127;
        analogWrite(greenPin, g);
        analogWrite(bluePin, b);
        break:
      case 3:
        g=189; b=189;
        analogWrite(greenPin, g);
        analogWrite(bluePin, b);
        break;
      case 4:
        g=255; b=255;
        analogWrite(greenPin, g);
        analogWrite(bluePin, b);
        break:
      default:
        g=0; b=0;
        analogWrite(greenPin, g);
        analogWrite(bluePin, b);
        break:
    }
}