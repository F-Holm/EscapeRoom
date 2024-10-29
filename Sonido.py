import pygame, threading
from enum import Enum

class Sonido:
    def __init__(self, sonido, loop, canal, volumen):
        self.sonido = sonido
        self.loop = loop
        self.canal = canal
        self.volumen = volumen #de 0.0 a 1.0

class Sonidos(Enum):
    DESPERTADOR = Sonido("Sonidos/despertadorSamsung.mp3", 1, 1, 0.7)
    TRUENO = Sonido("Sonidos/trueno.mp3", 0, 2, 1.0)
    MUSICA_FONDO = Sonido("Sonidos/musicaFondo.mp3", 1, 3, 0.7)
    GANASTE = Sonido("Sonidos/ganaste.mp3", 0, 4, 0.7)
    PERDISTE = Sonido("Sonidos/perdiste.mp3", 0, 5, 0.7)
    INTRODUCCION = Sonido("Sonidos/Introducción.mp3", 0, 6, 0.7)
    #Timers
    _333 = Sonido("Sonidos/Timers/333.mp3", 0, 7, 0.7)
    _7 = Sonido("Sonidos/Timers/7Minutos.mp3", 0, 8, 0.7)
    _10 = Sonido("Sonidos/Timers/cuentaRegresiva.mp3", 0, 9, 0.7)
    #Pistas
    PISTA_ARMARIO = Sonido("Sonidos/Pistas/armarioPista.mp3", 0, 10, 0.5)
    PISTA_GULA = Sonido("Sonidos/Pistas/gulaPista.mp3", 0, 11, 0.7)
    PISTA_IRA = Sonido("Sonidos/Pistas/juegoIraPista.mp3", 0, 12, 0.7)
    PISTA_LUJURIA = Sonido("Sonidos/Pistas/lujuriaPista.mp3", 0, 13, 0.7)
    PISTA_CODIGO = Sonido("Sonidos/Pistas/pistaCodigo.mp3", 0, 14, 0.7)
    #
    HALLELUJAH = Sonido("Sonidos/hallelujah.mp3", 1, 15, 0.3)
    _ = Sonido("Sonidos/_.mp3", 1, 16, 1.0)
    NO_IRA = Sonido("Sonidos/NO_IRA.mp3", 0, 16, 0.7)

CANTIDAD_CANALES = len(Sonidos)

def iniciarPygame():
    pygame.mixer.init()
    pygame.mixer.set_num_channels(CANTIDAD_CANALES)

def reproducirSonido(sonido):
    canal = pygame.mixer.Channel(sonido.value.canal)
    canal.set_volume(sonido.value.volumen)
    if sonido.value.loop:
        canal.play(pygame.mixer.Sound(sonido.value.sonido), -1)
    else:
        canal.play(pygame.mixer.Sound(sonido.value.sonido))
    if (sonido != Sonidos.MUSICA_FONDO and reproduciendo(Sonidos.MUSICA_FONDO) and sonido != Sonidos.TRUENO):
        hilo = threading.Thread(target=lambda: reanudarIntro(sonido))
        hilo.start()
        detenerSonido(Sonidos.MUSICA_FONDO)

def reanudarIntro(sonido):
    while reproduciendo(sonido):
        pass
    reproducirSonido(Sonidos.MUSICA_FONDO)


def detenerSonido(sonido):
    canal = pygame.mixer.Channel(sonido.value.canal)
    if (canal.get_busy()):
        canal.stop()

def detenerTodosLosSonidos():
    for i in range(CANTIDAD_CANALES):
        canal = pygame.mixer.Channel(i)
        if (canal.get_busy()):
            canal.stop()

def reproduciendo(sonido):
    return pygame.mixer.Channel(sonido.value.canal).get_busy()

def toggleSonido(sonido):
    canal = pygame.mixer.Channel(sonido.value.canal)
    if canal.get_busy():
        canal.stop()
    else:
        reproducirSonido(sonido)

def closePygame():
    pygame.quit()
