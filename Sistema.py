import sys
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import serial, threading, socket, time
from Sonido import Sonidos, detenerTodosLosSonidos, toggleSonido, closePygame, iniciarPygame, reproduciendo, reproducirSonido, detenerSonido
from Led import efecto, Efectos, closeLED, conectarArduinoLeds
from Codigos import Codigos
from Puertos import Puertos
from Niveles import Niveles, getNivel, getNumOrden

#close -> significa que no se va a volver a abrir
#stop -> significa que se puede reanudar/reiniciar

#Instancia de la clase sistema
sistema = None

#Instancia de la clase App. Contiene todo lo relacionado a tkinter (Interfaz gráfica)
root = None

#Como hay 2 clases que comparten arduino, crea la variable de forma global
arduino_boton_rfid = None

#clase que no tiene funcionalidad que sirve para poder testear un juego sin tener que testear todo. Tiene comentarios sobre los método más repetidos
class NivelTest:
    def __init__(self):
        pass

    def start(self):
        pass

    #se llama cada vez que se pasa de nivel. Si querés que pase algo cuando termine el nivel, lo ponés en este método
    def stop(self):
        pass

    def restart(self):
        pass

    def close(self):
        pass

#Estado inicial -> Es el estado de cuando entrás al escape room y cuando salís.
class Pre_Inicial:
    def __init__(self):
        pass

    def start(self):
        detenerTodosLosSonidos()
        root.after(5000, lambda: efecto(Efectos.APAGADO))#después de 5 segundos de terminar el escape room se apagan las luces
        root.after(5000, lambda: detenerTodosLosSonidos())

    def stop(self):
        pass

    def restart(self):
        pass

    def close(self):
        pass

#La introducción y se inicia el sonido de fondo y el efecto default (confetti)
class Inicio:
    reproduciendo = None
    hilo = None
    
    def __init__(self):
        self.reproduciendo = threading.Event()

    def start(self):
        sistema.niveles[len(sistema.niveles) - 1].gano = True#esta variable determina si gaste o perdiste, se cambia a false automáticamente si se te acaba el tiempo y acá la volvés a setear en true
        self.hilo = threading.Thread(target=self.hiloSonido)#pasa al siguiente nivel cuando termine la introducción
        self.reproduciendo.set()
        reproducirSonido(Sonidos.INTRODUCCION)
        self.hilo.start()
        efecto(Efectos.APAGADO)
        root.actualizar_timer_label("10:00")

    def cerrarHilo(self):
        if self.hilo != None and self.hilo.is_alive():
            self.reproduciendo.clear()
            self.hilo.join()
    
    def stop(self):
        self.cerrarHilo()
        detenerSonido(Sonidos.INTRODUCCION)
        reproducirSonido(Sonidos.MUSICA_FONDO)
        sistema.hiloContador = threading.Thread(target=sistema.timer)
        sistema.startTimers()

    def restart(self):
        self.cerrarHilo()
        detenerSonido(Sonidos.INTRODUCCION)
        reproducirSonido(Sonidos.INTRODUCCION)
        self.hilo = threading.Thread(target=self.hiloSonido)
        self.hilo.start()
    
    def hiloSonido(self):#pasa al siguiente nivel cuando termine la introducción
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
        self.conectarArduino()
        self.terminar = threading.Event()
        self.termino = threading.Event()

    def start(self):
        arduino_boton_rfid.write(Codigos.BOTON_START.value)
        self.terminar.clear()
        self.termino.clear()
        self.hilo = threading.Thread(target=self.hiloArduino)
        self.hilo.start()
        reproducirSonido(Sonidos.DESPERTADOR)

    def cerrarHilo(self):
        arduino_boton_rfid.write(Codigos.BOTON_STOP.value)
        if self.hilo != None and self.hilo.is_alive():
            self.terminar.set()
            #self.hilo.join()

    def stop(self):
        self.cerrarHilo()
        detenerSonido(Sonidos.DESPERTADOR)
        efecto(Efectos.ENCENDIDO_GRADUAL)
    
    def close(self):
        self.cerrarHilo()

    def restart(self):
        arduino_boton_rfid.write(Codigos.BOTON_RESTART.value)
        detenerSonido(Sonidos.DESPERTADOR)
        reproducirSonido(Sonidos.DESPERTADOR)
    
    def conectarArduino(self):#Si falla la conexión se reemplaza el nivel por un test
        global arduino_boton_rfid
        try:
            arduino_boton_rfid = serial.Serial(Puertos.BOTON_RFID.value, 9600, timeout=1)
        except Exception as e:
                root.after(100, lambda: sistema.setNivelTest(getNumOrden(Niveles.JUEGO_BOTON)))

    def hiloArduino(self):#pasa al siguiente nivel cuando termine el nivel
        while not self.terminar.is_set():
            if arduino_boton_rfid.in_waiting > 0:
                try:
                    if not (int(arduino_boton_rfid.readline()) == ord(Codigos.BOTON_TERMINO.value)):
                        continue
                except Exception as e:
                    #print(f"Error leyendo desde el puerto serial: {e}")
                    continue
                if not self.terminar.is_set():
                    root.after(1, lambda: sistema.siguienteNivel())
                self.terminar.set()
                self.termino.set()

#Cuando pasas al juego de los RFID se ejecuta el efecto del rayo. Esto y el estado pre-inicial son las únicas cosas no automatizadas
class Candado:
    def __init__(self):
        pass

    def start(self):
        pass

    def stop(self):
        efecto(Efectos.LIGHTNING)

    def restart(self):
        pass

    def close(self):
        pass

class JuegoRFID:
    hilo = None
    terminar = None
    termino = None
    
    def __init__(self):
        global arduino_boton_rfid
        if arduino_boton_rfid == None:#Si no es None se inicializó en la clase botón
            self.conectarArduino()
        self.terminar = threading.Event()
        self.termino = threading.Event()

    def start(self):
        arduino_boton_rfid.write(Codigos.START.value)
        self.terminar.clear()
        self.termino.clear()
        self.hilo = threading.Thread(target=self.hiloArduino)#pasa al siguiente nivel cuando termine el nivel
        self.hilo.start()
        self.parejas = ""
        root.actualizarEstado("0 parejas")

    def cerrarHilo(self):
        arduino_boton_rfid.write(Codigos.STOP.value)
        if self.hilo != None and self.hilo.is_alive():
            self.terminar.set()
            self.hilo.join()

    def stop(self):
        self.cerrarHilo()
    
    def close(self):
        self.cerrarHilo()
        arduino_boton_rfid.close()

    def restart(self):
        arduino_boton_rfid.write(Codigos.RESTART.value)
        
    def conectarArduino(self):#Si falla la conexión se reemplaza el nivel por un test
        global arduino_boton_rfid
        try:
            arduino_boton_rfid = serial.Serial(Puertos.BOTON_RFID.value, 9600, timeout=1)
        except Exception as e:
            root.after(100, lambda: sistema.setNivelTest(getNumOrden(Niveles.JUEGO_RFID)))
    
    def analizarCodigo(self, codigo):#si el mensaje recibido del arduino indica que terminó, setea los eventos para salir del hilo. Si el mensaje indica otra cosa, actualiza el estado actual (elemento de la interfaz).
        if codigo == ord(Codigos.RFID_0_PAREJAS.value):
            root.actualizarEstado("0 parejas")
            return False
        elif codigo == ord(Codigos.RFID_1_PAREJAS.value):
            root.actualizarEstado("1 parejas")
            return False
        elif codigo == ord(Codigos.RFID_2_PAREJAS.value):
            root.actualizarEstado("2 parejas")
            return False
        elif codigo == ord(Codigos.RFID_3_PAREJAS.value):
            root.actualizarEstado("3 parejas")
            return False
        elif codigo == ord(Codigos.RFID_4_PAREJAS.value):
            root.actualizarEstado("4 parejas")
            return False
        elif codigo == ord(Codigos.TERMINO.value):
            if not self.terminar.is_set():
                root.after(1, lambda: sistema.siguienteNivel())
            self.terminar.set()
            self.termino.set()
            return False
        return True

    def hiloArduino(self):#pasa al siguiente nivel cuando termine el nivel
        while not self.terminar.is_set():
            if arduino_boton_rfid.in_waiting > 0:
                dato = None
                try:
                    dato = int(arduino_boton_rfid.readline())
                    if not dato:
                        continue
                except Exception as e:
                    #print(f"Error leyendo desde el puerto serial: {e}")
                    continue
                self.analizarCodigo(dato)

class JuegoIra:
    hilo = None
    terminar = None
    termino = None
    arduino = None
    
    def __init__(self):
        self.terminar = threading.Event()
        self.termino = threading.Event()
        self.conectarArduino()

    def start(self):
        self.arduino.write(Codigos.START.value)
        self.terminar.clear()
        self.termino.clear()
        self.hilo = threading.Thread(target=self.hiloArduino)#pasa al siguiente nivel cuando termine el nivel
        self.hilo.start()

    def cerrarHilo(self):
        self.arduino.write(Codigos.STOP.value)
        if self.hilo != None and self.hilo.is_alive():
            self.terminar.set()
            #self.hilo.join()

    def stop(self):
        self.cerrarHilo()
    
    def close(self):
        self.cerrarHilo()
        self.arduino.close()

    def restart(self):
        self.arduino.write(Codigos.RESTART.value)
    
    def conectarArduino(self):#Si falla la conexión se reemplaza el nivel por un test
        try:
            self.arduino = serial.Serial(Puertos.IRA.value, 9600, timeout=1)
        except Exception as e:
            root.after(100, lambda: sistema.setNivelTest(getNumOrden(Niveles.JUEGO_IRA)))
    
    def analizarCodigo(self, codigo):#si el mensaje recibido del arduino indica que terminó, setea los eventos para salir del hilo. Si el mensaje indica otra cosa, actualiza el estado actual (elemento de la interfaz).
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
                root.after(1, lambda: sistema.siguienteNivel())
            self.terminar.set()
            self.termino.set()
            return False
        return True

    def hiloArduino(self):#pasa al siguiente nivel cuando termine el nivel
        while not self.terminar.is_set():
            if self.arduino.in_waiting > 0:
                dato = 0
                try:
                    dato = int(self.arduino.readline())
                except Exception as e:
                    #print(f"Error leyendo desde el puerto serial: {e}")
                    continue
                self.analizarCodigo(dato)

class JuegoTrivia:
    socket = None
    hilo = None
    terminar = None
    termino = None
    
    def __init__(self):
        self.conectarSocket()
        self.terminar = threading.Event()
        self.termino = threading.Event()
    
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
            #self.hilo.join()

    def stop(self):
        self.cerrarHilo()
    
    def close(self):
        self.cerrarHilo()
        self.closeSocket()

    def restart(self):
        self.enviarMensaje(Codigos.RESTART.value)

    def closeSocket(self):
        self.socket.close()
    
    def _terminar(self):#Cierra el hilo y pasa al siguiente nivel
        if not self.terminar.is_set():
            root.after(1, lambda: sistema.siguienteNivel())
        self.terminar.set()
        self.termino.set()
    
    def conectarSocket(self):#Si falla la conexión se reemplaza el nivel por un test
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(1.0)
            self.socket.connect((Puertos.IP_TRIVIA.value, Puertos.PUERTO_TRIVIA.value))#pasa al siguiente nivel cuando termine el nivel
            self.socket.setblocking(False)
        except Exception as e:
            root.after(100, lambda: sistema.setNivelTest(getNumOrden(Niveles.JUEGO_TRIVIA)))
    
    def analizarCodigo(self, codigo):#si el mensaje recibido de la computadora indica que terminó, setea los eventos para salir del hilo. Si el mensaje indica otra cosa, actualiza el estado actual (elemento de la interfaz).
        if codigo == (Codigos.TRIVIA_0_MONEDAS.value):
            root.after(1, lambda: root.mostrarMonedas("0"))
            self._terminar()
            return False
        elif codigo == (Codigos.TRIVIA_1_MONEDAS.value):
            root.after(1, lambda: root.mostrarMonedas("1"))
            self._terminar()
            return False
        elif codigo == (Codigos.TRIVIA_2_MONEDAS.value):
            root.after(1, lambda: root.mostrarMonedas("2"))
            self._terminar()
            return False
        elif codigo == (Codigos.TRIVIA_3_MONEDAS.value):
            root.after(1, lambda: root.mostrarMonedas("3"))
            self._terminar()
            return False
        elif codigo == (Codigos.TRIVIA_4_MONEDAS.value):
            root.after(1, lambda: root.mostrarMonedas("4"))
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

    def hiloSocket(self):#pasa al siguiente nivel cuando termine el nivel
        while not self.terminar.is_set():
            datos = None
            try:
                datos = self.socket.recv(1024)
                self.analizarCodigo(datos)
            except BlockingIOError:
                continue

#Vas al cielo a menos que se acabe el tiempo
class Fin:
    reproduciendo = None
    hilo = None
    gano = True#determina si ganó o no. Vuelve a true en la clase inicio. 
    _e = None#efecto
    _s = None#sonido
    
    def __init__(self):
        self.reproduciendo = threading.Event()

    def start(self):
        detenerTodosLosSonidos()
        sistema.stopTimers()
        detenerTodosLosSonidos()
        if self.gano:
            self._s = Sonidos.GANASTE
            self._e = Efectos.CIERRE
            reproducirSonido(Sonidos.HALLELUJAH)
        else:
            self._s = Sonidos.PERDISTE
            self._e = Efectos.PERDISTE
        self.hilo = threading.Thread(target=self.hiloSonido)#pasa al siguiente nivel cuando termine el sonido
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
        detenerSonido(Sonidos.HALLELUJAH)

    def restart(self):
        self.cerrarHilo()
        detenerSonido(self._s)
        reproducirSonido(self._s)
        self.hilo = threading.Thread(target=self.hiloSonido)
        self.hilo.start()
    
    def hiloSonido(self):#pasa al siguiente nivel cuando termine el sonido
        while self.reproduciendo.is_set():
            if not (reproduciendo(self._s)):
                self.reproduciendo.clear()
                root.after(0, lambda: sistema.siguienteNivel())

    def close(self):
        pass

class Sistema:
    niveles = None#Arreglo de niveles. Se inicializa en el __init__()
    nivelActual = 0#Recorre el arreglo de niveles

    #timers
    _333 = None#timer de que quedan 3:33
    _7 = None#timer de que quedan 7:00
    _10 = None#timer de que quedan 0:10
    _0 = None#timer de que se acabó el tiempo. Llama a perdio()
    
    contadorActivo = None
    hiloContador = None
    
    def __init__(self):
        self.niveles = [Pre_Inicial(), Inicio(), NivelBoton(), Candado(), JuegoRFID(), JuegoTrivia(), JuegoIra(), Fin()]
        iniciarPygame()#librería que utilizo para los sonidos
        conectarArduinoLeds()#inicializa la variable para comunicarse con el arduino
        root.actualizarNivel(0)
        self.contadorActivo = threading.Event()

    #Inicia el nivel actual
    def start(self):
        self.niveles[self.nivelActual].start()

    #detiene el nivel actual
    def stop(self):
        self.niveles[self.nivelActual].stop()

    #reinicia el nivel actual
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
    
    #Se cierra el programa
    def terminarJuego(self):
        self.stopTimers()
        for nivel in self.niveles:
            nivel.close()
        efecto(Efectos.APAGADO)
        closeLED()
        closePygame()
        if(self.hiloContador != None and self.hiloContador.is_alive()):
            self.hiloContador.join()
        closeTTK()
        sys.exit()
    
    #Detiene el nivel actual y va al estado pre-inicial
    def reiniciarJuego(self):
        self.stop()
        self.nivelActual = 0
        self.start()
        root.actualizarNivel(self.nivelActual)
        self.stopTimers()
    
    def startTimers(self):
        #roor.after( milisegundos, función ) -> despuesa de x milisegundos ejecuta una función. Con lambda le podés pasar parámetros
        self._333 = root.after((6*60 + 27) * 1000, lambda: reproducirSonido(Sonidos._333))
        self._7 = root.after((3*60) * 1000, lambda: reproducirSonido(Sonidos._7))
        self._10 = root.after((10*60 - 23) * 1000, lambda: reproducirSonido(Sonidos._10))
        self._0 = root.after(( 10*60 ) * 1000, lambda: self.perdio())
        self.contadorActivo.set()
        self.hiloContador.start()
    
    def stopTimers(self):
        try:
            root.after_cancel(self._333)
            root.after_cancel(self._7)
            root.after_cancel(self._10)
            root.after_cancel(self._0)
            self.contadorActivo.clear()
        except Exception as e:
            return
    
    def timer(self):
        segundos = 10 * 60
        while self.contadorActivo.is_set() and segundos != -1:
            mins, secs = divmod(segundos, 60)
            timer = '{:02d}:{:02d}'.format(mins, secs)
            root.actualizar_timer_label(timer)
            time.sleep(1)
            segundos -= 1
    
    def setNivelTest(self, n):
        self.niveles[n] = NivelTest()
        print(f"Error conexión: {getNivel(n).value}")
    
    #Se llama cuando se te acaba el tiempo
    def perdio(self):
        self.stop()
        self.nivelActual = len(self.niveles) - 1#hace que el nivel actual sea el FIN
        self.niveles[self.nivelActual].gano = False#Esta variable determina si gana o pierde
        self.start()

def iniciarSistema():
    global sistema
    sistema = Sistema()

#cierro TTK -> tkinter -> librería que utilizo para la interfaz gráfica.
def closeTTK():
    root.quit()
    root.destroy()

#Interfaz gráfica
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
        
        #Elementos de la derecha. Cada método es una fila
        self.escaperoom()
        self.nivelActual()
        self.efectos()
        self.pistas()
        self.sonidos1()
        self.sonidos2()
        
        self.separadorVertical()
    
    texto = ""

    def separadorVertical(self):
        separator = ttk.Separator(self, orient='vertical')
        separator.pack(side='left', fill='y')
    
    def configurarColumnaIzquierda(self):
        self.left_frame = tk.Frame(self, width=250, bg='lightgrey')
        self.left_frame.pack_propagate(False)
        self.left_frame.pack(side='left', fill='y')

        # Parte superior de la columna izquierda
        self.timer_label = tk.Label(self.left_frame, text="10:00", bg='lightgrey', font=('Helvetica', 48), anchor='center')
        self.timer_label.pack(side='top', fill='x', pady=(50, 0))  # Agrega un margen de 10 píxeles en la parte superior

        # Parte inferior de la columna izquierda
        self.lower_frame = tk.Frame(self.left_frame, bg='lightgrey')
        self.lower_frame.pack(side='bottom', fill='both', expand=True)

        self.left_label = tk.Label(self.lower_frame, text="Texto en la columna inferior", bg='lightgrey', anchor='center')
        self.left_label.pack(fill='both', expand=True)

    
    def toggle_fullscreen(self, event=None):
        self.fullscreen = not self.fullscreen
        self.attributes("-fullscreen", self.fullscreen)
        return "break"
    
    def show_confirmation_dialog(self, accion):#se llama cada vez que apretás un botón que requiera confirmación
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
        elif accion == 5:
            text = "detener los timers"
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
            elif accion == 5:
                sistema.stopTimers()
    
    def separadorHorizontal(self):#Separa cada una de las filas de la derecha
        separator = ttk.Separator(self.main_frame, orient='horizontal')
        separator.pack(fill='x', pady=5)
    
    def update_left_text(self, etapa):
        self.left_label.config(text=(self.texto + etapa))
    
    def actualizar_timer_label(self, nuevo_texto):
        self.timer_label.config(text=nuevo_texto)
    
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

        button_text = "Detener timer"
        button = tk.Button(row_frame, text=button_text, command=lambda: self.show_confirmation_dialog(5))
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

        button_text = "No Ira"
        button = tk.Button(row_frame, text=button_text, command=lambda: toggleSonido(Sonidos.NO_IRA))
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

        button_text = "Hallelujah"
        button = tk.Button(row_frame, text=button_text, command=lambda: toggleSonido(Sonidos.HALLELUJAH))
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
        
        button_text = "-"
        button = tk.Button(row_frame, text=button_text, command=lambda: toggleSonido(Sonidos._))
        button.pack(side='left', fill='both', expand=True, padx=5, pady=5)
        
        #self.separadorHorizontal()

    def actualizarNivel(self, nivel):#muestra todos los niveles a la izquierda e indica el nivel actual. También elimina el estado del nivel anterior
        self.texto = "Nivel Actual: " + getNivel(nivel).value + "\n\nNiveles:\n"
        for i in range(len(Niveles)):
            self.texto += getNivel(i).value
            if i != len(Niveles) - 1:
                self.texto += "\n"
        self.update_left_text("")
    
    def actualizarEstado(self, estado):#Estado es la información del nivel actual (cuantas parejas ingresó, en que pregunta está, si está jugando o perdió)
        self.update_left_text("\n\nEstado: " + estado)

    def mostrarMonedas(self, monedas):#Esto se llama cuando se termina la trivia
        messagebox.showinfo("Notificación", "Ganaron " + monedas + " monedas")

if __name__ == "__main__":
    root = App()
    iniciarSistema()#Inicializo la variable sistema
    root.mainloop()#Inicia la interfaz gráfica