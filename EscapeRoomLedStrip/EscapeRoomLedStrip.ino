// pines de cada color
const int redPin = 3;
const int greenPin = 5;
const int bluePin = 6;

// cantidad de juegos completados
//int juegosCompletados = 0;

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

    analogWrite(redPin, red);
    analogWrite(greenPin, green);
    analogWrite(bluePin, blue);

    Serial.begin(9600);
}

void loop(){
    // Test colores
    /*cambiarColor(255,0,0);
    delay(500);
    cambiarColor(255,255,0);
    delay(500);
    cambiarColor(0,255,0);
    delay(500);
    cambiarColor(0,255,255);
    delay(500);
    cambiarColor(0,0,255);
    delay(500);
    cambiarColor(255,0,255);
    delay(500);*/
  if (Serial.available() > 0) {
      String colores = Serial.readString();
      if (colores.length() == 1) {
          switch (colores[0]) {
              case '0':
                  rayo();
                  cambiarColor(red, green, blue);
                  break;
          }
      } else if (colores.length() >= 3) {
          cambiarColor(colores[0], colores[1], colores[2]);
      }
  }
}