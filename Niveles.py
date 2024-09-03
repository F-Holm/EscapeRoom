from enum import Enum

class Niveles(Enum):
    PRE_INICIAL = "Estado Pre-Inicial"
    INICIO = "Inicio"
    JUEGO_BOTON = "Juego Botón"
    JUEGO_IRA = "Juego Ira"
    JUEGO_RFID = "Juego RFID"
    JUEGO_TRIVIA = "Juego Trivia"
    FINAL = "Etapa Final"

def getNivel(numNivel):
    if numNivel == 0:
        return Niveles.PRE_INICIAL
    elif numNivel == 1:
        return Niveles.INICIO
    elif numNivel == 2:
        return Niveles.JUEGO_BOTON
    elif numNivel == 3:
        return Niveles.JUEGO_IRA
    elif numNivel == 4:
        return Niveles.JUEGO_RFID
    elif numNivel == 5:
        return Niveles.JUEGO_TRIVIA
    elif numNivel == 6:
        return Niveles.FINAL
    else:
        return None