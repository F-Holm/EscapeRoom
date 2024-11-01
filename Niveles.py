from enum import Enum

class Niveles(Enum):
    PRE_INICIAL = "Estado Pre-Inicial"
    INICIO = "Inicio"
    JUEGO_BOTON = "Juego Botón"
    CANDADO = "Candado"
    JUEGO_RFID = "Juego RFID"
    JUEGO_TRIVIA = "Juego Trivia"
    JUEGO_IRA = "Juego Ira"
    FINAL = "Etapa Final"

def getNivel(numNivel):
    return list(Niveles)[numNivel]

def getNumOrden(nivel):
    return list(Niveles).index(nivel)