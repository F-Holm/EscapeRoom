// pines de cada color
const int redPin = 3;
const int greenPin = 5;
const int bluePin = 6;

// cantidad de juegos completados
int juegosCompletados = 0;

// valor de cada color
int red = 0;
int green = 0;
int blue = 0;

void cambiarColor(int r, int g, int b){
  analogWrite(redPin, r); red = r;
  analogWrite(greenPin, g); green = g;
  analogWrite(bluePin, b); blue = b;
}

void rayo(){
  cambiarColor(61, 126, 255);
  delay(400);
  cambiarColor(0, 0, 0);
  delay(200);
  cambiarColor(61, 126, 255);
  delay(400);
}

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

    if(Serial.avaliable() > 0){
      string colores = Serial.read();
      if (colores.size() == 1){
        switch (colores[0]){
          case 0:
            rayo();
            cambiarColor(red, green, blue);
            break;
        }
      }
      else cambiarColor(colores[0], colores[1], colores[2]);
    }
    /*
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
    */
}