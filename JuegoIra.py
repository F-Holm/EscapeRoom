from enum import Enum
import sys
import tkinter as tk
from tkinter import messagebox, ttk
from tkinter import *
from time import sleep
from Sonido import reproducirSonido, detenerSonido, delay, closePygame, Sonidos
import serial, time, threading
import socket
from Led import cambiarColor, efecto, Efectos, Colores, closeLED, EfectosNeoPixel
from Codigos import Codigos
from Puertos import Puertos
from variablesGlobales import sistema, root

class JuegoIra:
    arduino = None
    hilo = None
    terminar = None
    termino = None
    
    def __init__(self):
        self.arduino = serial.Serial(Puertos.IRA.value, 9600, timeout=1)
        self.terminar = threading.Event()
        self.termino = threading.Event()

    def start(self):
        self.arduino.write(Codigos.START.value)
        self.terminar.clear()
        self.termino.clear()
        self.hilo = threading.Thread(target=self.hiloArduino)
        self.hilo.start()

    def cerrarHilo(self):
        self.arduino.write(Codigos.STOP.value)
        if self.hilo != None and self.hilo.is_alive():
            self.terminar.set()
            self.hilo.join()

    def stop(self):
        self.cerrarHilo()
        sistema.siguienteNivel()
    
    def close(self):
        self.cerrarHilo()
        self.closeArduino()

    def restart(self):
        self.arduino.write(Codigos.RESTART.value)

    def closeArduino(self):
        self.arduino.close()
    
    def hiloArduino(self):
        while not self.terminar.is_set():
            if self.arduino.in_waiting > 0:
                try:
                    self.arduino.readline().decode('utf-8').strip()  # Decodificar y eliminar saltos de línea
                except Exception as e:
                    print(f"Error leyendo desde el puerto serial: {e}")
                if not self.terminar.is_set():
                    root.after(500, lambda: sistema.siguienteNivel())
                self.terminar.set()
                self.termino.set()