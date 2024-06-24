from enum import Enum
import sys
import pygame
from time import sleep
import tkinter as tk
from tkinter import messagebox, ttk
from tkinter import *
import serial, time, threading

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

class juegoIra:
    arduino = serial.Serial('/dev/ttyUSB0', 9600)
    hilo = None
    eventoFin = threading.Event()

    def start(self):
        self.arduino.write(b'0')
        self.hilo = threading.Thread(target=self.hiloArduino)
        self.hilo.start()

    def stop(self):
        self.arduino.write(b'1')
        self.eventoFin.set()

    def restart(self):
        self.arduino.write(b'2')

    def closeArduino(self):
        self.arduino.close()
    
    def hiloArduino(self):
        while self.eventoFin.is_set() == False:
            try:
                if self.arduino.in_waiting > 0:
                    data = self.arduino.readline()
                    if data == b'0':
                        self.stop()
            except:
                pass
        self.eventoFin.clear()

class Sistema:
    niveles = [juegoIra()]#Agregá niveles utilizando las clases correspondientes -> [Nivle1(), Nivle2(), Nivel3("qwerty"), ...]
    nivelActual = 0

    def start(self):
        self.niveles[self.nivelActual].start()

    def stop(self):
        self.niveles[self.nivelActual].stop()

    def restart(self):
        self.niveles[self.nivelActual].restart()

    def nivelAnterior(self):
        if self.nivelActual != 0:
            self.nivelActual -= 1
        else:
            self.restart()

    def siguienteNivel(self):
        if self.nivelActual != len(self.niveles) - 1:
            self.nivelActual += 1
        else:
            self.terminarJuego()
    
    def terminarJuego(self):
        self.stop()
        self.niveles[0].closeArduino()
        pygame.quit()
        root.quit()
        root.destroy()
        sys.exit()

sistema = Sistema()
    
root = tk.Tk()
root.title("Escape room")

juegoAnterior = ttk.Button(root, text="Nivel anterior", command=sistema.nivelAnterior)
juegoAnterior.grid(row=0, column=0, padx=10, pady=10)
root.bind("<KeyPress-Left>", lambda e: sistema.nivelAnterior())

juegoSiguiente = ttk.Button(root, text="Siguiente nivel", command=sistema.siguienteNivel)
juegoSiguiente.grid(row=0, column=2, padx=10, pady=10)
root.bind("<KeyPress-Right>", lambda e: sistema.siguienteNivel())

juegoSiguiente = ttk.Button(root, text="Iniciar nivel", command=sistema.start)
juegoSiguiente.grid(row=1, column=0, padx=10, pady=10)
root.bind("<KeyPress-Up>", lambda e: sistema.start())

juegoSiguiente = ttk.Button(root, text="Detener nivel", command=sistema.stop)
juegoSiguiente.grid(row=1, column=2, padx=10, pady=10)
root.bind("<KeyPress-Down>", lambda e: sistema.stop())

juegoSiguiente = ttk.Button(root, text="Reiniciar nivel", command=sistema.restart)
juegoSiguiente.grid(row=1, column=1, padx=10, pady=10)
root.bind("<Return>", lambda e: sistema.restart())

juegoSiguiente = ttk.Button(root, text="Terminar juego", command=sistema.terminarJuego)
juegoSiguiente.grid(row=2, column=1, padx=10, pady=10)
root.bind("<Escape>", lambda e: sistema.terminarJuego())