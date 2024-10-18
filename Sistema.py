import sys
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import serial, threading, socket
from Sonido import Sonidos, detenerTodosLosSonidos, toggleSonido, closePygame, iniciarPygame, reproduciendo, reproducirSonido, detenerSonido
from Led import efecto, Efectos, closeLED
from Codigos import Codigos
from Puertos import Puertos, IRA_ARDUINO, BOTON_RFID_ARDUINO, LEDS_ARDUINO
from Niveles import Niveles, getNivel

sistema = None
root = None

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

class Pre_Inicial:
    def __init__(self):
        pass

    def start(self):
        detenerTodosLosSonidos()

    def stop(self):
        pass

    def restart(self):
        pass

    def close(self):
        pass

class Inicio:
    reproduciendo = None
    hilo = None
    
    def __init__(self):
        self.reproduciendo = threading.Event()

    def start(self):
        sistema.niveles[len(sistema.niveles) - 1].gano = True
        self.hilo = threading.Thread(target=self.hiloSonido)
        self.reproduciendo.set()
        reproducirSonido(Sonidos.INTRODUCCION)
        self.hilo.start()
        efecto(Efectos.APAGADO)

    def cerrarHilo(self):
        if self.hilo != None and self.hilo.is_alive():
            self.reproduciendo.clear()
            self.hilo.join()
    
    def stop(self):
        self.cerrarHilo()
        detenerSonido(Sonidos.INTRODUCCION)
        reproducirSonido(Sonidos.MUSICA_FONDO)
        sistema.startTimers()

    def restart(self):
        self.cerrarHilo()
        detenerSonido(Sonidos.INTRODUCCION)
        reproducirSonido(Sonidos.INTRODUCCION)
        self.hilo = threading.Thread(target=self.hiloSonido)
        self.hilo.start()
    
    def hiloSonido(self):
        while self.reproduciendo.is_set():
            if not (reproduciendo(Sonidos.INTRODUCCION)):
                self.reproduciendo.clear()
                root.after(0, lambda: sistema.siguienteNivel())

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
        BOTON_RFID_ARDUINO.write(Codigos.BOTON_START.value)
        self.terminar.clear()
        self.termino.clear()
        self.hilo = threading.Thread(target=self.hiloArduino)
        self.hilo.start()
        reproducirSonido(Sonidos.DESPERTADOR)

    def cerrarHilo(self):
        BOTON_RFID_ARDUINO.write(Codigos.BOTON_STOP.value)
        if self.hilo != None and self.hilo.is_alive():
            self.terminar.set()
            self.hilo.join()

    def stop(self):
        self.cerrarHilo()
        detenerSonido(Sonidos.DESPERTADOR)
        efecto(Efectos.ENCENDIDO_GRADUAL)
    
    def close(self):
        self.cerrarHilo()

    def restart(self):
        BOTON_RFID_ARDUINO.write(Codigos.BOTON_RESTART.value)
        detenerSonido(Sonidos.DESPERTADOR)
        reproducirSonido(Sonidos.DESPERTADOR)
    
    def hiloArduino(self):
        while not self.terminar.is_set():
            if BOTON_RFID_ARDUINO.in_waiting > 0:
                try:
                    if not (int(BOTON_RFID_ARDUINO.readline()) == ord(Codigos.BOTON_TERMINO.value)):
                        continue
                except Exception as e:
                    print(f"Error leyendo desde el puerto serial: {e}")
                    continue
                if not self.terminar.is_set():
                    root.after(0, lambda: sistema.siguienteNivel())
                self.terminar.set()
                self.termino.set()

class JuegoRFID:
    hilo = None
    terminar = None
    termino = None
    
    def __init__(self):
        self.terminar = threading.Event()
        self.termino = threading.Event()

    def start(self):
        BOTON_RFID_ARDUINO.write(Codigos.START.value)
        self.terminar.clear()
        self.termino.clear()
        self.hilo = threading.Thread(target=self.hiloArduino)
        self.hilo.start()

    def cerrarHilo(self):
        BOTON_RFID_ARDUINO.write(Codigos.STOP.value)
        if self.hilo != None and self.hilo.is_alive():
            self.terminar.set()
            self.hilo.join()

    def stop(self):
        self.cerrarHilo()
    
    def close(self):
        self.cerrarHilo()
        BOTON_RFID_ARDUINO.close()

    def restart(self):
        BOTON_RFID_ARDUINO.write(Codigos.RESTART.value)
    
    def analizarCodigo(self, codigo):
        if codigo == ord(Codigos.RFID_0_PAREJAS.value):
            root.actualizarEstado("0 Parejas Correctas")
            return False
        elif codigo == ord(Codigos.RFID_1_PAREJAS.value):
            root.actualizarEstado("1 Parejas Correctas")
            return False
        elif codigo == ord(Codigos.RFID_2_PAREJAS.value):
            root.actualizarEstado("2 Parejas Correctas")
            return False
        elif codigo == ord(Codigos.RFID_3_PAREJAS.value):
            root.actualizarEstado("3 Parejas Correctas")
            return False
        elif codigo == ord(Codigos.RFID_4_PAREJAS.value):
            root.actualizarEstado("4 Parejas Correctas")
            return False
        elif codigo == ord(Codigos.TERMINO.value):
            if not self.terminar.is_set():
                root.after(0, lambda: sistema.siguienteNivel())
            self.terminar.set()
            self.termino.set()
            return False
        return True

    def hiloArduino(self):
        while not self.terminar.is_set():
            if BOTON_RFID_ARDUINO.in_waiting > 0:
                try:
                    if self.analizarCodigo(int(BOTON_RFID_ARDUINO.readline())):
                        continue
                except Exception as e:
                    print(f"Error leyendo desde el puerto serial: {e}")
                    continue

class JuegoIra:
    hilo = None
    terminar = None
    termino = None
    
    def __init__(self):
        self.terminar = threading.Event()
        self.termino = threading.Event()

    def start(self):
        IRA_ARDUINO.write(Codigos.START.value)
        self.terminar.clear()
        self.termino.clear()
        self.hilo = threading.Thread(target=self.hiloArduino)
        self.hilo.start()

    def cerrarHilo(self):
        IRA_ARDUINO.write(Codigos.STOP.value)
        if self.hilo != None and self.hilo.is_alive():
            self.terminar.set()
            self.hilo.join()

    def stop(self):
        self.cerrarHilo()
    
    def close(self):
        self.cerrarHilo()
        IRA_ARDUINO.close()

    def restart(self):
        IRA_ARDUINO.write(Codigos.RESTART.value)
    
    def analizarCodigo(self, codigo):
        if codigo == ord(Codigos.IRA_JUGANDO.value):
            root.actualizarEstado("Jugando")
            return False
        elif codigo == ord(Codigos.IRA_PERDIERON.value):
            root.actualizarEstado("Perdieron")
            return False
        elif codigo == ord(Codigos.IRA_TERMINO_JUGADOR_1.value):
            root.actualizarEstado("Terminó Jugador 1")
            return False
        elif codigo == ord(Codigos.IRA_TERMINO_JUGADOR_2.value):
            root.actualizarEstado("Terminó Jugador 2")
            return False
        elif codigo == ord(Codigos.TERMINO.value):
            if not self.terminar.is_set():
                root.after(0, lambda: sistema.siguienteNivel())
            self.terminar.set()
            self.termino.set()
            return False
        return True

    def hiloArduino(self):
        while not self.terminar.is_set():
            if IRA_ARDUINO.in_waiting > 0:
                try:
                    if self.analizarCodigo(int(IRA_ARDUINO.readline())):
                        continue
                except Exception as e:
                    print(f"Error leyendo desde el puerto serial: {e}")
                    continue

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
        self.socket.sendall(codigo)

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
    
    def _terminar(self):
        if not self.terminar.is_set():
            root.after(0, lambda: sistema.siguienteNivel())
        self.terminar.set()
        self.termino.set()
    
    def analizarCodigo(self, codigo):
        if codigo == (Codigos.TRIVIA_0_MONEDAS.value):
            root.mostrarMonedas("0")
            self._terminar()
            return False
        elif codigo == (Codigos.TRIVIA_1_MONEDAS.value):
            root.mostrarMonedas("1")
            self._terminar()
            return False
        elif codigo == (Codigos.TRIVIA_2_MONEDAS.value):
            root.mostrarMonedas("2")
            self._terminar()
            return False
        elif codigo == (Codigos.TRIVIA_3_MONEDAS.value):
            root.mostrarMonedas("3")
            self._terminar()
            return False
        elif codigo == (Codigos.TRIVIA_4_MONEDAS.value):
            root.mostrarMonedas("4")
            self._terminar()
            return False
        elif codigo == (Codigos.TRIVIA_PREGUNTA_1.value):
            root.actualizarEstado("Pregunta 1")
            return False
        elif codigo == (Codigos.TRIVIA_PREGUNTA_2.value):
            root.actualizarEstado("Pregunta 2")
            return False
        elif codigo == (Codigos.TRIVIA_PREGUNTA_3.value):
            root.actualizarEstado("Pregunta 3")
            return False
        elif codigo == (Codigos.TRIVIA_PREGUNTA_4.value):
            root.actualizarEstado("Pregunta 4")
            return False
        elif codigo == (Codigos.TRIVIA_PREGUNTA_5.value):
            root.actualizarEstado("Pregunta 5")
            return False
        elif codigo == ord(Codigos.TERMINO.value):
            self._terminar()
            return False
        return True

    def hiloSocket(self):
        while not self.terminar.is_set():
            datos = None
            try:
                datos = self.socket.recv(1024)
                self.analizarCodigo(datos)
            except BlockingIOError:
                continue

class Fin:
    reproduciendo = None
    hilo = None
    gano = True
    _e = None
    _s = None
    
    def __init__(self):
        self.reproduciendo = threading.Event()

    def start(self):
        sistema.stopTimers()
        if self.gano:
            self._s = Sonidos.GANASTE
            self._e = Efectos.CIERRE
        else:
            self._s = Sonidos.PERDISTE
            self._e = Efectos.PERDISTE
        detenerTodosLosSonidos()
        self.hilo = threading.Thread(target=self.hiloSonido)
        self.reproduciendo.set()
        reproducirSonido(self._s)
        self.hilo.start()
        efecto(self._e)

    def cerrarHilo(self):
        if self.hilo != None and self.hilo.is_alive():
            self.reproduciendo.clear()
            self.hilo.join()
    
    def stop(self):
        self.cerrarHilo()
        detenerSonido(self._s)

    def restart(self):
        self.cerrarHilo()
        detenerSonido(self._s)
        reproducirSonido(self._s)
        self.hilo = threading.Thread(target=self.hiloSonido)
        self.hilo.start()
    
    def hiloSonido(self):
        while self.reproduciendo.is_set():
            if not (reproduciendo(self._s)):
                self.reproduciendo.clear()
                root.after(0, lambda: sistema.siguienteNivel())

    def close(self):
        pass

class Sistema:
    niveles = None
    nivelActual = 0

    _333 = None
    _7 = None
    _10 = None
    _0 = None

    def __init__(self):#Pre_Inicial(), Inicio(), NivelBoton(), JuegoRFID(), JuegoIra(), JuegoTrivia(), Fin()
        self.niveles = [NivelTest(), NivelTest(), NivelTest(), NivelTest(), NivelTest(), NivelTest(), NivelTest()]
        iniciarPygame()#NivelTest

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
            self.start()
        root.actualizarNivel(self.nivelActual)
    
    def terminarJuego(self):
        for nivel in self.niveles:
            nivel.close()
        closeLED()
        closePygame()
        closeTTK()
        sys.exit()
    
    def reiniciarJuego(self):
        self.stop()
        self.nivelActual = 0
        self.start()
        root.actualizarNivel(self.nivelActual)
    
    def startTimers(self):
        self._333 = root.after((6*60 + 27) * 1000, lambda: reproducirSonido(Sonidos._333))
        self._7 = root.after((3*60) * 1000, lambda: reproducirSonido(Sonidos._7))
        self._10 = root.after((9*60 + 50) * 1000, lambda: reproducirSonido(Sonidos._10))
        self._0 = root.after(( 10*60 + 18 ) * 1000, lambda: self.perdio())
    
    def stopTimers(self):
        root.after_cancel(self._333)
        root.after_cancel(self._7)
        root.after_cancel(self._10)
        root.after_cancel(self._0)
    
    def perdio(self):
        self.stop()
        self.nivelActual = len(self.niveles) - 1
        self.niveles[self.nivelActual].gano = False
        self.start()

def iniciarSistema():
    global sistema
    sistema = Sistema()

def closeTTK():
    root.quit()
    root.destroy()

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
        self.efectos()
        self.pistas()
        self.sonidos1()
        self.sonidos2()
        
        #self.crearSwitch()
        self.separadorVertical()
        self.actualizarNivel(0)
    
    texto = ""

    def separadorVertical(self):
        separator = ttk.Separator(self, orient='vertical')
        separator.pack(side='left', fill='y')
    
    def configurarColumnaIzquierda(self):
        self.left_frame = tk.Frame(self, width=250, bg='lightgrey')
        self.left_frame.pack_propagate(False)  # Evita que el frame ajuste su tamaño automáticamente
        self.left_frame.pack(side='left', fill='y')
        
        self.left_label = tk.Label(self.left_frame, text="Texto en la columna izquierda", bg='lightgrey', anchor='center')
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
    
    def update_left_text(self, etapa):
        self.left_label.config(text=(self.texto + etapa))
    
    def escaperoom(self):
        row_frame = tk.Frame(self.main_frame)
        row_frame.pack(fill='x', expand=True)
        
        row_label = tk.Label(row_frame, text="Escape Room")
        row_label.pack(fill='x')

        #button_text = "Iniciar Escape Room"
        #button = tk.Button(row_frame, text=button_text, command=lambda: self.show_confirmation_dialog(0))
        #button.pack(side='left', fill='both', expand=True, padx=5, pady=5)

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

    def efectos(self):
        row_frame = tk.Frame(self.main_frame)
        row_frame.pack(fill='x', expand=True)
        
        row_label = tk.Label(row_frame, text="Efectos")
        row_label.pack(fill='x')
        
        button_text = "Apagado"
        button = tk.Button(row_frame, text=button_text, command=lambda: efecto(Efectos.APAGADO))
        button.pack(side='left', fill='both', expand=True, padx=5, pady=5)

        button_text = "Confetti"
        button = tk.Button(row_frame, text=button_text, command=lambda: efecto(Efectos.CONFETTI))
        button.pack(side='left', fill='both', expand=True, padx=5, pady=5)
        
        button_text = "Lightning"
        button = tk.Button(row_frame, text=button_text, command=lambda: efecto(Efectos.LIGHTNING))
        button.pack(side='left', fill='both', expand=True, padx=5, pady=5)

        button_text = "Cierre"
        button = tk.Button(row_frame, text=button_text, command=lambda: efecto(Efectos.CIERRE))
        button.pack(side='left', fill='both', expand=True, padx=5, pady=5)

        button_text = "Encendido Gradual"
        button = tk.Button(row_frame, text=button_text, command=lambda: efecto(Efectos.ENCENDIDO_GRADUAL))
        button.pack(side='left', fill='both', expand=True, padx=5, pady=5)

        button_text = "Blanco"
        button = tk.Button(row_frame, text=button_text, command=lambda: efecto(Efectos.BLANCO))
        button.pack(side='left', fill='both', expand=True, padx=5, pady=5)
        
        button_text = "Perdiste"
        button = tk.Button(row_frame, text=button_text, command=lambda: efecto(Efectos.PERDISTE))
        button.pack(side='left', fill='both', expand=True, padx=5, pady=5)

        button_text = "Rojo"
        button = tk.Button(row_frame, text=button_text, command=lambda: efecto(Efectos.ROJO))
        button.pack(side='left', fill='both', expand=True, padx=5, pady=5)

        button_text = "Agua"
        button = tk.Button(row_frame, text=button_text, command=lambda: efecto(Efectos.AGUA))
        button.pack(side='left', fill='both', expand=True, padx=5, pady=5)

        self.separadorHorizontal()

    def pistas(self):
        row_frame = tk.Frame(self.main_frame)
        row_frame.pack(fill='x', expand=True)
        
        row_label = tk.Label(row_frame, text="Pistas")
        row_label.pack(fill='x')
        
        button_text = "Armario"
        button = tk.Button(row_frame, text=button_text, command=lambda: toggleSonido(Sonidos.PISTA_ARMARIO))
        button.pack(side='left', fill='both', expand=True, padx=5, pady=5)
        
        button_text = "Gula"
        button = tk.Button(row_frame, text=button_text, command=lambda: toggleSonido(Sonidos.PISTA_GULA))
        button.pack(side='left', fill='both', expand=True, padx=5, pady=5)
        
        button_text = "Ira"
        button = tk.Button(row_frame, text=button_text, command=lambda: toggleSonido(Sonidos.PISTA_IRA))
        button.pack(side='left', fill='both', expand=True, padx=5, pady=5)
        
        button_text = "Lujuria"
        button = tk.Button(row_frame, text=button_text, command=lambda: toggleSonido(Sonidos.PISTA_LUJURIA))
        button.pack(side='left', fill='both', expand=True, padx=5, pady=5)
        
        button_text = "Código"
        button = tk.Button(row_frame, text=button_text, command=lambda: toggleSonido(Sonidos.PISTA_CODIGO))
        button.pack(side='left', fill='both', expand=True, padx=5, pady=5)
        
        self.separadorHorizontal()

    def sonidos1(self):
        row_frame = tk.Frame(self.main_frame)
        row_frame.pack(fill='x', expand=True)
        
        row_label = tk.Label(row_frame, text="Sonidos")
        row_label.pack(fill='x')

        button_text = "Detener todos los sonidos"
        button = tk.Button(row_frame, text=button_text, command=detenerTodosLosSonidos)
        button.pack(side='left', fill='both', expand=True, padx=5, pady=5)
        
        button_text = "Despertador"
        button = tk.Button(row_frame, text=button_text, command=lambda: toggleSonido(Sonidos.DESPERTADOR))
        button.pack(side='left', fill='both', expand=True, padx=5, pady=5)

        button_text = "Trueno"
        button = tk.Button(row_frame, text=button_text, command=lambda: toggleSonido(Sonidos.TRUENO))
        button.pack(side='left', fill='both', expand=True, padx=5, pady=5)

        button_text = "Musica Fondo"
        button = tk.Button(row_frame, text=button_text, command=lambda: toggleSonido(Sonidos.MUSICA_FONDO))
        button.pack(side='left', fill='both', expand=True, padx=5, pady=5)
        
        button_text = "Ganaste"
        button = tk.Button(row_frame, text=button_text, command=lambda: toggleSonido(Sonidos.GANASTE))
        button.pack(side='left', fill='both', expand=True, padx=5, pady=5)
        
        button_text = "Perdiste"
        button = tk.Button(row_frame, text=button_text, command=lambda: toggleSonido(Sonidos.PERDISTE))
        button.pack(side='left', fill='both', expand=True, padx=5, pady=5)

        button_text = "Introducción"
        button = tk.Button(row_frame, text=button_text, command=lambda: toggleSonido(Sonidos.INTRODUCCION))
        button.pack(side='left', fill='both', expand=True, padx=5, pady=5)

        #self.separadorHorizontal()
    
    def sonidos2(self):
        row_frame = tk.Frame(self.main_frame)
        row_frame.pack(fill='x', expand=True)
        
        #row_label = tk.Label(row_frame, text="Sonidos")
        #row_label.pack(fill='x')
        
        button_text = "Quedan 3:33 minutos"
        button = tk.Button(row_frame, text=button_text, command=lambda: toggleSonido(Sonidos._333))
        button.pack(side='left', fill='both', expand=True, padx=5, pady=5)
        
        button_text = "Quedan 7 minutos"
        button = tk.Button(row_frame, text=button_text, command=lambda: toggleSonido(Sonidos._7))
        button.pack(side='left', fill='both', expand=True, padx=5, pady=5)
        
        button_text = "Quedan 10 segundos"
        button = tk.Button(row_frame, text=button_text, command=lambda: toggleSonido(Sonidos._10))
        button.pack(side='left', fill='both', expand=True, padx=5, pady=5)
        
        
        #self.separadorHorizontal()

    def maxLargoNivel(self):
        max = 0
        for i in range(len(Niveles)):
            if len(getNivel(i).value) > max:
                max = len(getNivel(i).value)
        return max + 10 + len("Nivel Actual: ")#10 = 2*espacio = 2*5

    def actualizarNivel(self, nivel):
        self.texto = "Nivel Actual: " + getNivel(nivel).value + "\n\nNiveles:\n"
        for i in range(len(Niveles)):
            self.texto += getNivel(i).value
            if i != len(sistema.niveles) - 1:
                self.texto += "\n"
        self.update_left_text("")
    
    def actualizarEstado(self, estado):
        self.update_left_text("\n\nEstado: " + estado)

    def mostrarMonedas(self, monedas):
        messagebox.showinfo("Notificación", "Ganaron " + monedas + " monedas")

if __name__ == "__main__":
    iniciarSistema()
    root = App()
    root.mainloop()