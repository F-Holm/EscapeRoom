from enum import Enum
import pygame
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

def detenerSonidos():
    pygame.mixer.music.stop()

def delay(segundos):
    sleep(segundos)

class Sistema:
    niveles = []#Agregá niveles utilizando las clases hijas -> [Nivle1(), Nivle2(), Nivel3("qwerty"), ...]
    nivelActual = 0

    def start():
        pass

    def stop():
        detenerSonidos()

    def restart():
        pass

    def nivelAnterior(self):
        if self.nivelActual != 0:
            nivelActual -= 1

    def siguienteNivel(self):
        if self.nivelActual != len(self.niveles) - 1:
            self.nivelActual += 1