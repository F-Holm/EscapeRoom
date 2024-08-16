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
from Sistema import sistema, root

class JuegoTrivia:    
    socket = None
    hilo = None
    terminar = None
    termino = None
    
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((Puertos.IP_TRIVIA.value, Puertos.PUERTO_TRIVIA.value))
        self.terminar = threading.Event()
        self.termino = threading.Event()
    
    def enviarMensaje(self, codigo):
        self.socket.sendall(codigo.value.encode())

    def start(self):
        self.enviarMensaje(Codigos.START.value)
        self.terminar.clear()
        self.termino.clear()
        self.hilo = threading.Thread(target=self.hiloSocket)
        self.hilo.start()

    def cerrarHilo(self):
        self.enviarMensaje(Codigos.STOP.value)
        if self.hilo != None and self.hilo.is_alive():
            self.terminar.set()
            self.hilo.join()

    def stop(self):
        self.cerrarHilo()
        sistema.siguienteNivel()
    
    def close(self):
        self.cerrarHilo()
        self.closeSocket()

    def restart(self):
        self.enviarMensaje(Codigos.RESTART.value)

    def closeSocket(self):
        self.socket.close()
    
    def hiloSocket(self):
        while not self.terminar.is_set():
            datos = socket.recv(1024)
            if datos.decode() == Codigos.TERMINO.value:
                if not self.terminar.is_set():
                    root.after(500, lambda: sistema.siguienteNivel())
                self.terminar.set()
                self.termino.set()