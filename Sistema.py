import sys
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import serial, threading, socket
from Sonido import Sonidos, detenerTodosLosSonidos, toggleSonido, closePygame, iniciarPygame
from Led import cambiarColor, efecto, EfectosLedsRGB, Colores, EfectosNeoPixel, EfectosGlobales, closeLED, conectarLEDS
from Codigos import Codigos
from Puertos import Puertos
from Niveles import Niveles, getNivel

sistema = None
root = None
arduino = None

class NivelTest:
    def __init__(self):
        pass

    def start(self):
        pass

    def stop(self):
        pass

    def restart(self):
        pass

    def close(self):
        pass

class NivelBoton:
    hilo = None
    terminar = None
    termino = None
    
    def __init__(self):
        self.terminar = threading.Event()
        self.termino = threading.Event()

    def start(self):
        arduino.write(Codigos.START_BOTON.value)
        self.terminar.clear()
        self.termino.clear()
        self.hilo = threading.Thread(target=self.hiloArduino)
        self.hilo.start()

    def cerrarHilo(self):
        arduino.write(Codigos.STOP.value)
        if self.hilo != None and self.hilo.is_alive():
            self.terminar.set()
            self.hilo.join()

    def stop(self):
        self.cerrarHilo()
    
    def close(self):
        self.cerrarHilo()

    def restart(self):
        arduino.write(Codigos.RESTART.value)
    
    def hiloArduino(self):
        while not self.terminar.is_set():
            if arduino.in_waiting > 0:
                try:
                    if not (int(arduino.readline()) == ord(Codigos.TERMINO.value)):
                        continue
                except Exception as e:
                    print(f"Error leyendo desde el puerto serial: {e}")
                if not self.terminar.is_set():
                    root.after(0, lambda: sistema.siguienteNivel())
                self.terminar.set()
                self.termino.set()

class JuegoIra:
    hilo = None
    terminar = None
    termino = None
    
    def __init__(self):
        self.terminar = threading.Event()
        self.termino = threading.Event()

    def start(self):
        arduino.write(Codigos.START.value)
        self.terminar.clear()
        self.termino.clear()
        self.hilo = threading.Thread(target=self.hiloArduino)
        self.hilo.start()

    def cerrarHilo(self):
        arduino.write(Codigos.STOP.value)
        if self.hilo != None and self.hilo.is_alive():
            self.terminar.set()
            self.hilo.join()

    def stop(self):
        self.cerrarHilo()
    
    def close(self):
        self.cerrarHilo()

    def restart(self):
        arduino.write(Codigos.RESTART.value)
    
    def hiloArduino(self):
        while not self.terminar.is_set():
            if arduino.in_waiting > 0:
                try:
                    if not (int(arduino.readline()) == ord(Codigos.TERMINO.value)):
                        continue
                except Exception as e:
                    print(f"Error leyendo desde el puerto serial: {e}")
                if not self.terminar.is_set():
                    root.after(0, lambda: sistema.siguienteNivel())
                self.terminar.set()
                self.termino.set()

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
        self.socket.setblocking(False)
    
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
            if datos == Codigos.TERMINO.value:
                if not self.terminar.is_set():
                    root.after(500, lambda: sistema.siguienteNivel())
                self.terminar.set()
                self.termino.set()



class Sistema:
    niveles = None
    nivelActual = 0

    def __init__(self):
        self.niveles = [NivelTest(), NivelTest(), NivelTest(), NivelTest(), JuegoTrivia(), NivelTest()]

    def start(self):
        self.niveles[self.nivelActual].start()

    def stop(self):
        self.niveles[self.nivelActual].stop()

    def restart(self):
        self.niveles[self.nivelActual].restart()

    def nivelAnterior(self):
        if self.nivelActual != 0:
            self.stop()
            self.nivelActual -= 1
            self.start()
        else:
            self.restart()
        root.actualizarNivel(self.nivelActual)

    def siguienteNivel(self):
        if self.nivelActual != len(self.niveles) - 1:
            self.stop()
            self.nivelActual += 1
            self.start()
        else:
            self.stop()
            self.nivelActual = 0
        root.actualizarNivel(self.nivelActual)
    
    def reiniciarJuego(self):
        self.stop()
        self.nivelActual = 0
        self.start()
    
    def terminarJuego(self):
        for nivel in self.niveles:
            nivel.close()
        #closeArduinoBotonIra()
        #closeLED()
        closePygame()
        closeTTK()
        sys.exit()

def iniciarSistema():
    global sistema
    sistema = Sistema()
    #conectarLEDS()
    #iniciarArduinoBotonIra()
    iniciarPygame()

def closeTTK():
    root.quit()
    root.destroy()

def closeArduinoBotonIra():
    arduino.close()

def iniciarArduinoBotonIra():
    global arduino
    arduino = serial.Serial(Puertos.BOTON_IRA.value, 9600, timeout=1)





class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Escape Room")
        self.fullscreen = False
        self.geometry("1200x600")
        
        self.bind("<F11>", self.toggle_fullscreen)
        
        self.configurarColumnaIzquierda()

        self.main_frame = tk.Frame(self)
        self.main_frame.pack(side='left', fill='both', expand=True)
        
        self.escaperoom()
        self.nivelActual()
        self.efectosGlobales()
        self.efectosNeoPixel()
        self.efectosLedsRGB()
        self.coloresLedsRGB()
        self.sonidos()
        
        #self.crearSwitch()
        self.separadorVertical()
        self.actualizarNivel(0)
    
    def separadorVertical(self):
        separator = ttk.Separator(self, orient='vertical')
        separator.pack(side='left', fill='y')
    
    def configurarColumnaIzquierda(self):
        self.left_frame = tk.Frame(self, width=100, bg='lightgrey')
        self.left_frame.pack(side='left', fill='y')
        
        self.left_label = tk.Label(self.left_frame, text="Texto en la columna izquierda", bg='lightgrey')
        self.left_label.pack(fill='both', expand=True)
    
    def toggle_fullscreen(self, event=None):
        self.fullscreen = not self.fullscreen
        self.attributes("-fullscreen", self.fullscreen)
        return "break"
    
    def show_confirmation_dialog(self, accion):
        text = ""
        if accion == 0:
            text = "iniciar el juego"
        elif accion == 1:
            text = "volver al nivel anterior"
        elif accion == 2:
            text = "ir al siguiente nivel"
        elif accion == 3:
            text = "reiniciar el juego"
        elif accion == 4:
            text = "terminar el juego"
        else:
            return
        
        response = messagebox.askquestion("Confirmación", f"¿Seguro que quieres {text}?")
        if response == 'yes':
            if accion == 0:
                iniciarSistema()
            elif accion == 1:
                sistema.nivelAnterior()
            elif accion == 2:
                sistema.siguienteNivel()
            elif accion == 3:
                sistema.reiniciarJuego()
            elif accion == 4:
                sistema.terminarJuego()

    def crearSwitch(self):
        switch_frame = tk.Frame(self.main_frame)
        switch_frame.pack(fill='x')
        switch = tk.Checkbutton(switch_frame, text="Switch")
        switch.pack(side='right')
    
    def separadorHorizontal(self):
        separator = ttk.Separator(self.main_frame, orient='horizontal')
        separator.pack(fill='x', pady=5)
    
    def update_left_text(self, texto):
        self.left_label.config(text=texto)
    
    def escaperoom(self):
        row_frame = tk.Frame(self.main_frame)
        row_frame.pack(fill='x', expand=True)
        
        row_label = tk.Label(row_frame, text="Escape Room")
        row_label.pack(fill='x')

        button_text = "Iniciar Escape Room"
        button = tk.Button(row_frame, text=button_text, command=lambda: self.show_confirmation_dialog(0))
        button.pack(side='left', fill='both', expand=True, padx=5, pady=5)

        button_text = "Nivel Anterior"
        button = tk.Button(row_frame, text=button_text, command=lambda: self.show_confirmation_dialog(1))
        button.pack(side='left', fill='both', expand=True, padx=5, pady=5)

        button_text = "Siguiente Nivel"
        button = tk.Button(row_frame, text=button_text, command=lambda: self.show_confirmation_dialog(2))
        button.pack(side='left', fill='both', expand=True, padx=5, pady=5)

        button_text = "Reiniciar Escape Room"
        button = tk.Button(row_frame, text=button_text, command=lambda: self.show_confirmation_dialog(3))
        button.pack(side='left', fill='both', expand=True, padx=5, pady=5)

        button_text = "Terminar Escape Room"
        button = tk.Button(row_frame, text=button_text, command=lambda: self.show_confirmation_dialog(4))
        button.pack(side='left', fill='both', expand=True, padx=5, pady=5)
        
        self.separadorHorizontal()

    def nivelActual(self):
        row_frame = tk.Frame(self.main_frame)
        row_frame.pack(fill='x', expand=True)
        
        row_label = tk.Label(row_frame, text="Nivel Actual")
        row_label.pack(fill='x')
        
        button_text = "Iniciar Nivel"
        button = tk.Button(row_frame, text=button_text, command=lambda :sistema.start)
        button.pack(side='left', fill='both', expand=True, padx=5, pady=5)

        button_text = "Reiniciar Nivel"
        button = tk.Button(row_frame, text=button_text, command=lambda :sistema.restart)
        button.pack(side='left', fill='both', expand=True, padx=5, pady=5)

        button_text = "Detener Nivel"
        button = tk.Button(row_frame, text=button_text, command=lambda :sistema.stop)
        button.pack(side='left', fill='both', expand=True, padx=5, pady=5)
        
        self.separadorHorizontal()

    def efectosGlobales(self):
        row_frame = tk.Frame(self.main_frame)
        row_frame.pack(fill='x', expand=True)
        
        row_label = tk.Label(row_frame, text="Efectos Globales")
        row_label.pack(fill='x')
        
        button_text = "Rayo"
        button = tk.Button(row_frame, text=button_text, command=lambda: efecto(EfectosGlobales.RAYO))
        button.pack(side='left', fill='both', expand=True, padx=5, pady=5)
        
        self.separadorHorizontal()

    def efectosNeoPixel(self):
        row_frame = tk.Frame(self.main_frame)
        row_frame.pack(fill='x', expand=True)
        
        row_label = tk.Label(row_frame, text="Efectos Neo Pixel")
        row_label.pack(fill='x')
        
        button_text = "Cielo Infierno"
        button = tk.Button(row_frame, text=button_text, command=lambda: efecto(EfectosNeoPixel.CIELO_INFIERNO))
        button.pack(side='left', fill='both', expand=True, padx=5, pady=5)

        button_text = "Cielo"
        button = tk.Button(row_frame, text=button_text, command=lambda: efecto(EfectosNeoPixel.CIELO))
        button.pack(side='left', fill='both', expand=True, padx=5, pady=5)
        
        self.separadorHorizontal()

    def efectosLedsRGB(self):
        row_frame = tk.Frame(self.main_frame)
        row_frame.pack(fill='x', expand=True)
        
        row_label = tk.Label(row_frame, text="Efectos LEDs RGB")
        row_label.pack(fill='x')
        
        button_text = "Rayo"
        button = tk.Button(row_frame, text=button_text, command=lambda: efecto(EfectosLedsRGB.RAYO))
        button.pack(side='left', fill='both', expand=True, padx=5, pady=5)
        
        self.separadorHorizontal()

    def coloresLedsRGB(self):
        row_frame = tk.Frame(self.main_frame)
        row_frame.pack(fill='x', expand=True)
        
        row_label = tk.Label(row_frame, text="Colores LEDs")
        row_label.pack(fill='x')
        
        button_text = "Negro"
        button = tk.Button(row_frame, text=button_text, command=lambda: cambiarColor(Colores.NEGRO))
        button.pack(side='left', fill='both', expand=True, padx=5, pady=5)

        button_text = "Blanco"
        button = tk.Button(row_frame, text=button_text, command=lambda: cambiarColor(Colores.BLANCO))
        button.pack(side='left', fill='both', expand=True, padx=5, pady=5)

        button_text = "Rojo"
        button = tk.Button(row_frame, text=button_text, command=lambda: cambiarColor(Colores.ROJO))
        button.pack(side='left', fill='both', expand=True, padx=5, pady=5)

        button_text = "Verde"
        button = tk.Button(row_frame, text=button_text, command=lambda: cambiarColor(Colores.VERDE))
        button.pack(side='left', fill='both', expand=True, padx=5, pady=5)

        button_text = "Azul"
        button = tk.Button(row_frame, text=button_text, command=lambda: cambiarColor(Colores.AZUL))
        button.pack(side='left', fill='both', expand=True, padx=5, pady=5)
        
        self.separadorHorizontal()

    def sonidos(self):
        row_frame = tk.Frame(self.main_frame)
        row_frame.pack(fill='x', expand=True)
        
        row_label = tk.Label(row_frame, text="Sonidos")
        row_label.pack(fill='x')

        button_text = "Detener todos los sonidos"
        button = tk.Button(row_frame, text=button_text, command=detenerTodosLosSonidos)
        button.pack(side='left', fill='both', expand=True, padx=5, pady=5)
        
        button_text = "Himno de la URSS"
        button = tk.Button(row_frame, text=button_text, command=lambda: toggleSonido(Sonidos.HIMNO_URSS))
        button.pack(side='left', fill='both', expand=True, padx=5, pady=5)

        button_text = "JIJIJIJA"
        button = tk.Button(row_frame, text=button_text, command=lambda: toggleSonido(Sonidos.JIJIJIJA))
        button.pack(side='left', fill='both', expand=True, padx=5, pady=5)
        
        #self.separadorHorizontal()

    def maxLargoNivel(self):
        max = 0
        for i in range(len(Niveles)):
            if len(getNivel(i).value) > max:
                max = len(getNivel(i).value)
        return max + 10 + len("Nivel Actual: ")#10 = 2*espacio = 2*5

    def rellenar(self, texto):
        maxLargo = self.maxLargoNivel()
        while len(texto) < maxLargo:
            if maxLargo - len(texto) % 2 == 0:
                texto = " " + texto + " "
            else:
                texto = " " + texto
        return texto

    def actualizarNivel(self, nivel):
        espacio = "     "
        texto = espacio + "Nivel Actual: " + getNivel(nivel).value + espacio
        texto = self.rellenar(texto) + "\n\n Niveles: \n"
        for i in range(len(Niveles)):
            texto += getNivel(i).value
            if i != 5:
                texto += "\n"
        self.update_left_text(texto)


if __name__ == "__main__":
    iniciarSistema()
    root = App()
    root.mainloop()