from enum import Enum
from Codigos import Codigos
import serial

arduino0 = '/dev/ttyUSB0'
arduino1 = '/dev/ttyUSB1'
arduino2 = '/dev/ttyUSB2'

LEDS_ARDUINO = None
BOTON_RFID_ARDUINO = None
IRA_ARDUINO = None

#LEDS_ARDUINO = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
#BOTON_RFID_ARDUINO = serial.Serial('/dev/ttyUSB1', 9600, timeout=1)
#IRA_ARDUINO = serial.Serial('/dev/ttyUSB2', 9600, timeout=1)

leds = None
boton_rfid = None
ira = None

def identificar(arduino, puerto):
    global ira
    global boton_rfid
    global leds
    arduino.write(Codigos.IDENTIFICATE.value)
    respuesta = None
    while True:
    
        while arduino.in_waiting <= 0:
            continue
    
        respuesta = arduino.readline()
        if not respuesta:
            continue
        if (int(respuesta) == ord(Codigos.IRA_IDENTIFICACION.value)):
            ira = puerto
            IRA_ARDUINO = arduino
            break
        elif (int(respuesta) == ord(Codigos.BOTON_RFID_IDENTIFICACION.value)):
            boton_rfid = puerto
            BOTON_RFID_ARDUINO = arduino
            break
        elif (int(respuesta) == ord(Codigos.LEDS_IDENTIFICACION.value)):
            leds = puerto
            LEDS_ARDUINO = arduino
            break


#identificar(serial.Serial(arduino0, 9600, timeout=1), arduino0)
#identificar(serial.Serial(arduino1, 9600, timeout=1), arduino1)
#identificar(serial.Serial(arduino2, 9600, timeout=1), arduino2)

class Puertos(Enum):
    IP_TRIVIA = '192.168.1.10'
    PUERTO_TRIVIA = 8080
    LEDS = leds
    BOTON_RFID = boton_rfid
    IRA = ira