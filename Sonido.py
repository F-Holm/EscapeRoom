import pygame
from enum import Enum

class Sonido:
    def __init__(self, sonido, loop, canal):
        self.sonido = sonido
        self.loop = loop
        self.canal = canal

class Sonidos(Enum):
    RISA_DIABOLICA = Sonido("Sonidos/risaDiabolica.mp3", 0, 0)
    GRITO = Sonido("Sonidos/grito.mp3", 0, 1)
    DESPERTADOR = Sonido("Sonidos/homecoming.mp3", 1, 2)
    TRUENO = Sonido("Sonidos/trueno.mp3", 0, 3)
    MUSICA_FONDO = Sonido("Sonidos/musicaFondo.mp3", 1, 4)
    
    GANASTE = Sonido("Sonidos/ganaste.m4a", 0, 5)
    HORA = Sonido("Sonidos/hora.m4a", 0, 6)
    PERDISTE = Sonido("Sonidos/perdiste.m4a", 0, 7)
    RISA_MALA = Sonido("Sonidos/risa_mala.m4a", 0, 8)
    RISA_MALA_2 = Sonido("Sonidos/risa_mala_2.m4a", 0, 9)
    TEXTO_MAS_LENTO = Sonido("Sonidos/texto_mas_lento.m4a", 0, 10)

CANTIDAD_CANALES = 11

def iniciarPygame():
    pygame.mixer.init()
    pygame.mixer.set_num_channels(CANTIDAD_CANALES)

def reproducirSonido(sonido):
    if sonido.value.loop:
        pygame.mixer.Channel(sonido.value.canal).play(pygame.mixer.Sound(sonido.value.sonido), -1)
    else:
        pygame.mixer.Channel(sonido.value.canal).play(pygame.mixer.Sound(sonido.value.sonido))

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
