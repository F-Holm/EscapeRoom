import pygame
from enum import Enum
from time import sleep

class Sonidos(Enum):
    HIMNO_URSS = "Sonidos/Himno nacional de la Unión de Repúblicas Socialistas Soviéticas.mp3"
    JIJIJIJA = "Sonidos/JIJIJIJA.mp3"

pygame.mixer.init()
pygame.mixer.set_num_channels(10)#Cambiar el numero una vez que sepamos cunatos canales vamos a necesitar

def reproducirSonido(sonido, loop, canal):#enum sonido, bool loop, int canal
    if loop:
        pygame.mixer.Channel(canal).play(pygame.mixer.Sound(sonido.value), -1)
    else:
        pygame.mixer.Channel().play(pygame.mixer.Sound(sonido.value), -1)

def detenerSonido(canal):
    pygame.mixer.Channel(canal).stop()

def delay(segundos):
    sleep(segundos)

def closePygame():
    pygame.quit()
