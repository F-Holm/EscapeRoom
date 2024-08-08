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
    // FALTA RECIBIR EL INT DE HOLM
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
    String colores = Serial.readString(); // Cambiar a readString
    if (colores.length() == 1) { // Usar length() para verificar el tamaño
        switch (colores[0]) {
            case '0': // Comparar como carácter
                rayo();
                cambiarColor(red, green, blue); // Asegúrate de que estas variables estén definidas
                break;
            // Puedes añadir más casos aquí si es necesario
        }
    } else if (colores.length() >= 3) { // Asegúrate de que hay al menos 3 caracteres para RGB
        int r = colores[0];
        int g = colores[1];
        int b = colores[2];
        cambiarColor(r, g, b);
    }
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