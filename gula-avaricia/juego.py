from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QDialog,QGridLayout
from PyQt5.QtCore import Qt, QTimer, QSize
from PyQt5.QtGui import QPixmap, QPainter, QImage, QBrush
import sys
import random
import os
import time
import socket
import threading
from enum import Enum

STYLE = "style.css"
IPLOCAL= "192.168.1.10"

PUERTO= 8080

class Codigos(Enum):
    START   = b'\x00' # Inicia el juego
    RESTART = b'\x01' # Reinicia el juego
    STOP    = b'\x02' # Detiene el juego pero puede volver a iniciarse
    CLOSE   = b'\x03' # Detiene el juego y no puede volver a iniciarse
    TERMINO = b'\x04' # Indica que el juego terminó. Esto se mande desde el juego al sistema

def apagarPantalla():
    os.system('sudo vbetool dpms off')
    #os.system('echo "hola"')

def prenderPantalla():
    os.system('sudo vbetool dpms on')
    #os.system('echo "chau"')

apagarPantalla()

score = 0
easy_correct = 0    
current_question = None
termino = False

class Question:
    def __init__(self, text, options, correct_answer):
        self.text = text
        self.options = options
        self.correct_answer = correct_answer

easy_questions = [
    Question("¿Cuál es la capital de Francia?", ["a) París", "b) Madrid", "c) Roma", "d) Londres"], "a"),
    Question("¿Cuál es una comida tradicional argentina?", ["a) sushi", "b) pizza", "c) asado", "d) hamburguesa"], "c"),
    Question("¿Cuál es el capitán de la selección argentina?", ["a) Di Maria", "b) Messi", "c) Dibu", "d) Paredes"], "b"),
    Question("¿Cuáles son los colores del uniforme del\nInstituto Politécnico Modelo?", ["a) verde y blanco", "b) rojo y verde", "c) azul y gris", "d) naranja"], "c"),
    Question("¿Quién es el presidente de Argentina actualmente?", ["a) Rodriguez", "b) Perez", "c) Fiore", "d) Milei"], "d"),
    Question("¿Cuánto es 2 + 2?", ["a) 4", "b) 6", "c) 7", "d) 3"], "a"),
    Question("¿Cuál es la capital de Argentina?", ["a) Mendoza", "b) Santa Fe", "c) Buenos Aires", "d) Londres"], "c"),
    Question("¿Cuántos planetas hay en el sistema solar?", ["a) 1", "b) 3", "c) 8", "d) 20"], "c"),
    Question("¿Cuántos jugadores juegan en un equipo en un partido de fútbol profesional?", ["a) 4", "b) 11", "c) 27", "d) 2"], "b"),
    Question("¿Cuánto es 3 * 3?", ["a) 5", "b) 27", "c) 13", "d) 9"], "d"),
    Question("¿De dónde se hacen las\nhojas de papel?", ["a) del plástico", "b) del metal", "c) de los árboles", "d) del agua"], "c"),
    Question("¿En base a qué se alimentan \nlos vehículos nafteros?", ["a) electricidad", "b) viento", "c) nafta", "d) gas"], "c"),
    Question("¿Qué pesa más, \n1 kg de pluma o 1 kg de plomo?", ["a) pluma", "b) plomo", "c) pesan lo mismo", "d) no se puede medir"], "c"),
    Question("¿Qué animal no es un felino?", ["a) gato", "b) tigre", "c) perro", "d) león"], "c"),
    Question("¿Qué se lo conoce como 'bondi'\n en la jerga argentina?", ["a) auto", "b) colectivo", "c) tren", "d) bicicleta"], "b"),
    Question("¿Cuántos kilómetros\n hay en 1000 metros?", ["a) 1 km", "b) 0.2 km", "c) 20 km", "d) 100 km"], "a"),
    Question("¿Cuántos centímetros\n hay en un metro?", ["a) 30 cm", "b) 52 cm", "c) 100 cm", "d) 155 cm"], "c"),
    Question("¿Qué país habla portugués \ncomo lengua natal?", ["a) Argentina", "b) Brasil", "c) España", "d) Chile"], "b"),
    Question("¿Qué número de camiseta utiliza \nMessi en la selección argentina?", ["a) 1", "b) 10", "c) 23", "d) 4"], "b"),
    Question("¿Cuántos minutos\n hay en una hora?", ["a) 25 minutos", "b) 45 minutos", "c) 60 minutos", "d) 180 minutos"], "c"),
    Question("¿Cuántas horas\n hay en un día?", ["a) 5 horas", "b) 24 horas", "c) 13 horas", "d) 48 horas"], "b"),
    Question("¿Cuántos días tiene un año?", ["a) 365 días", "b) 120 días", "c) 31 días", "d) 666 días"], "a"),
    Question("¿Cada cuánto tiempo se realizan\n las elecciones en Argentina?", ["a) 1 años", "b) cada mes", "c) 4 años", "d) 30 años"], "c"),
    Question("¿Qué animal es conocido como el rey de la selva?", ["a) Elefante", "b) León", "c) Tigre", "d) Gorila"], "b"),
    Question("¿Qué planeta es conocido como \nel planeta rojo?", ["a) Marte", "b) Venus", "c) Júpiter", "d) Saturno"], "a"),
    Question("¿Cuál es el océano \nmás grande del mundo?", ["a) Atlántico", "b) Índico", "c) Pacífico", "d) Ártico"], "c"),
]

hard_questions = [
    Question("¿Cuál es la distancia desde \nBuenos Aires hasta Tokio?", ["a) 10 m .", "b) 90 cm.", "c) a la vuelta", "d) 10 cuadras"], "e"),
    Question("¿Cuál es el elemento más abundante\n en la corteza terrestre?", ["a) chocolate", "b) carne", "c) banana", "d) billetes"], "h"),
    Question("¿Cuál es la cantidad aproximada de galaxias\n en el universo observable?", ["a) muchas", "b) 1", "c) un par", "d) pocas"], "l"),
    Question("¿Cuál es el resultado de elevar e \n(la base de los logaritmos naturales) \na la potencia de pi (π)?", ["a) 1", "b) 2", "c) 3", "d) 4"], "f"),
    Question("¿Cuál es el valor aproximado de la constante\n de gravitación universal (G) \nen unidades SI?", ["a) un numero", "b) sustantivo", "c) adjetivo", "d) verbo"], "f"),
    Question("¿Cuál es la velocidad de un elefante en \ncaída libre?", ["a) 5 km/h", "b) un susurro", "c) a paso de tortuga", "d) 1km/h"], "f"),
    Question("¿Cuál es la temperatura de \nebullición del silencio?", ["a) 1000°C", "b) 478 °C", "c) -273.15°C", "d) depende del día"], "f"),
    Question("¿Cuántas patas tiene un leon?", ["a) 1", "b) 2", "c) ninguna", "d) 42"], "c"),
    Question("¿Cuál es la forma geométrica \nde un gato ?", ["a) cuadrado", "b) esférico", "c) triangular", "d) rectangular"], "f")
]

dichos = ["La avaricia rompe el saco", "Quien come para vivir, se alimenta;\nque vive para comer, revienta."]


empezar = threading.Event()

class Socket:
    servidor = None
    conexion = None
    
    hilo = None
    terminar = None #Le indica al hilo que tiene que terminar

    def __init__(self):
        self.terminar = threading.Event()
        
        servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        servidor.bind((IPLOCAL, PUERTO))
        
        servidor.listen(1)
        print("Esperando conexiones...")
        self.conexion, direccion = servidor.accept()
        print(f"Conectado a {direccion}")
        self.conexion.setblocking(False)#hace que el método recv no bloquee el hilo
        
        self.hilo = threading.Thread(target=self.hiloEscucha)
        self.hilo.start()
    
    def hiloEscucha(self):#Recomiendo usar eventos en los métodos start, stop y close porque el hilo se detiene para llamar a uno de estos métodos y no va a poder recibir nuevos mensaje hasta que termine la ejecución del método. Tampoco podría detenerse
        while not self.terminar.is_set():
            try:
                datos = self.conexion.recv(1024)
                print(datos)
            except BlockingIOError:
                continue
            if (datos == Codigos.START.value):
                self.start()
            elif (datos == Codigos.STOP.value):
                self.stop()
            elif (datos == Codigos.RESTART.value):
                self.stop()
                self.start()
            elif (datos == Codigos.CLOSE.value):
                self.close()#Tené en cuenta que el hilo no va a finalizar hasta que termine de ejecutarse esta función
                break
    
    def start(self):    
        empezar.set()
    
    def stop(self): #Arreglar esto
        global glitch_timer
        global app
        global seguir
        global ventanaPreguntas

        apagarPantalla()
        if glitch_timer is not None:
            glitch_timer.stop()
        if seguir is not None:
            seguir.close()  
        if ventanaPreguntas is not None:
            ventanaPreguntas.close()
        if app is not None:
            app.quit()
        


    def close(self):
        apagarPantalla()
        self.conexion.close()
        sys.exit()
        


        
     
    def notificarTermino(self):#Este método se encarga de notificar al sistema que el juego terminó
        self.conexion.sendall(Codigos.TERMINO.value)

    def comunicarScore(self,score):
        if score == 0:
            print("Score: 0")
            self.conexion.sendall(b'\xD0') 
        elif score == 1:
            print("Score: 1")
            self.conexion.sendall(b'\xD1')
        elif score == 2:
            print("Score: 2")
            self.conexion.sendall(b'\xD2')
        elif score == 4:
            print("Score: 4")
            self.conexion.sendall(b'\xD4') # GANO Y EL SIGUIENTE CODIGO SON LA CANTIDAD DE MONEDAS A ENTREGAR

objeto = Socket()
objeto.daemon = True



def load_stylesheet():
    with open(STYLE, "r") as file:
        return file.read()

class CustomDialog(QDialog):
    def __init__(self, title, message, show_ok_button=True, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setStyleSheet(load_stylesheet())
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.showFullScreen()

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        
        self.message_label = QLabel(message)
        self.message_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.message_label)
        
        if show_ok_button:
            self.ok_button = QPushButton("OK")
            self.ok_button.clicked.connect(self.accept)
            layout.addWidget(self.ok_button)
            
        self.setLayout(layout)


def bienvenida():
    dialog = CustomDialog("¡Bienvenido a la trivia!", "¡Bienvenido a la trivia!\nResponde las siguientes preguntas y gana \nMUCHISIMAS\n monedas de chocolate")
    dialog.exec()

def glitch_effect(label, original_text):
    glitch_text = ''.join(random.choice(['@', '#', '%', '&', '*', original_text[i]]) for i in range(len(original_text)))
    label.setText(glitch_text)
    QTimer.singleShot(200, lambda: label.setText(original_text))



def verificarRta(answer, question_display, answer_buttons):
    global score
    global easy_correct
    global termino
    if answer == current_question.correct_answer:
        score += 1
        easy_correct += 1
        objeto.comunicarScore(score)
        msg_box = CustomDialog("Respuesta", "¡Correcto!")
        msg_box.exec()
    elif score > 0 :
        score = 0
        objeto.comunicarScore(score)
        msg_box = CustomDialog("Respuesta", "¡Incorrecto! \n " + random.choice(dichos))
        msg_box.exec() 

    else :
        score = 0
        objeto.comunicarScore(score)
        msg_box = CustomDialog("Respuesta", "¡Incorrecto!")
        msg_box.exec()

    score_msg = CustomDialog("Puntuación", f"Puntuación Total : \n {score} monedas de chocolate.")
    score_msg.exec()
    
    if score != 0 and termino != True:
        seguirJugando()

    if score == 0 and easy_correct >= 2:
        easy_correct = 0
    if termino == False:
        cargarPregunta(question_display, answer_buttons)
    elif termino:
        pass

def cargarPregunta(question_display, answer_buttons):
    global current_question
    global preguntasFacil
    global preguntasDificil

    if easy_correct < 2:
        current_question = random.choice(preguntasFacil)
        preguntasFacil.remove(current_question)
        question_display.setText(current_question.text)
    else:
        current_question = random.choice(preguntasDificil)
        preguntasDificil.remove(current_question)
        question_display.setText(current_question.text)

    for i in range(4):
        answer_buttons[i].setText(current_question.options[i])
        answer_buttons[i].disconnect()
        answer_buttons[i].clicked.connect(lambda _, ans=current_question.options[i][0]: verificarRta(ans, question_display, answer_buttons))

def seguirJugando():
    global seguir
    seguir = QDialog()
    seguir.setWindowTitle("Seguir Jugando")
    seguir.setStyleSheet(load_stylesheet())
    seguir.setWindowFlag(Qt.FramelessWindowHint)
    seguir.showFullScreen()

    layout = QVBoxLayout()
    layout.setAlignment(Qt.AlignCenter)
    
    seguir.label = QLabel("¡Respondiste muy bien!\n¿Quieres seguir jugando y ganar MÁS monedas de chocolate?")
    seguir.label.setAlignment(Qt.AlignCenter)
    layout.addWidget(seguir.label)
    
    aceptar = QPushButton('Sí')
    denegar = QPushButton('No')
    layout.addWidget(aceptar)
    layout.addWidget(denegar)
    
    seguir.setLayout(layout)
    aceptar.clicked.connect(seguir.close)
    denegar.clicked.connect(ganar)
    
    seguir.exec()

def ganar():
    global score
    global termino
    global glitch_timer
    global app
    global seguir
    global ventanaPreguntas

    termino=True
    objeto.comunicarScore(4)
    objeto.comunicarScore(score)
    objeto.notificarTermino()

    if glitch_timer is not None:
        glitch_timer.stop()

    mensaje = CustomDialog("¡GANASTE!", f"¡GANASTE!\nFelicidades, elegiste el camino correcto, \n no fuiste avaro, y la gula no te sobrepasó!  \n  Podés ir a buscar {score} monedas!!.")
    mensaje.exec()

    seguir.close()
    ventanaPreguntas.close()

    QTimer.singleShot(0, lambda: app.quit())
    apagarPantalla()


class PasswordDialog(QDialog):
    def __init__(self, correct_password, parent=None):
        super().__init__(parent)
        self.correct_password = correct_password
        self.entered_password = ""
        
        self.setWindowTitle("Ingresar Contraseña")
        self.setStyleSheet(load_stylesheet())
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.showFullScreen()

        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignCenter)
        self.setLayout(self.layout)

        self.display = QHBoxLayout()
        self.layout.addLayout(self.display)

        self.password_labels = []
        for _ in range(4):  # Assuming password length is 4
            label = QLabel("_")
            label.setAlignment(Qt.AlignCenter)
            label.setStyleSheet("font-size: 36px; color: lime; border: 2px solid lime; padding: 10px;")
            self.display.addWidget(label)
            self.password_labels.append(label)

        self.button_grid = QGridLayout()
        self.layout.addLayout(self.button_grid)

        buttons = [
            ('1', 0, 0), ('2', 0, 1), ('3', 0, 2),
            ('4', 1, 0), ('5', 1, 1), ('6', 1, 2),
            ('7', 2, 0), ('8', 2, 1), ('9', 2, 2),
            ('0', 3, 1)
        ]

        for text, row, col in buttons:
            button = QPushButton(text)
            button.clicked.connect(self.button_clicked)
            self.button_grid.addWidget(button, row, col)

    def button_clicked(self):
        sender = self.sender().text()
        if len(self.entered_password) < 4:
            self.entered_password += sender
            self.update_display()

        if len(self.entered_password) == 4:
            QTimer.singleShot(500, self.check_password)

    def update_display(self):
        for i, label in enumerate(self.password_labels):
            label.setText(self.entered_password[i] if i < len(self.entered_password) else "_")

    def check_password(self):
        if self.entered_password == self.correct_password:
            self.accept()  # Password correct, close dialog
        else:
            self.wrong_password()

    def wrong_password(self):
        self.entered_password = ""
        self.update_display()
        self.flash_red()

    def flash_red(self):
        original_style = self.styleSheet()

        def set_red():
            self.setStyleSheet("QLabel {color: red; border: 2px solid red;} QPushButton {background-color: red; color: black;}")
        
        def set_original():
            self.setStyleSheet(original_style)
        
        def flash():
            set_red()
            QTimer.singleShot(250, set_original)
            QTimer.singleShot(500, set_red)
            QTimer.singleShot(750, set_original)

        flash()





def main():
    global current_question
    global termino
    global seguir
    global ventanaPreguntas
    global glitch_timer
    global app
    global score
    global preguntasFacil
    global preguntasDificil
    global easy_correct
    apagarPantalla()
    empezar.wait()
    empezar.clear()

    preguntasFacil = easy_questions
    preguntasDificil = hard_questions

    easy_correct = 0     
    score = 0 
    app = None
    seguir = None
    ventanaPreguntas = None
    current_question = None


    prenderPantalla()

    
    app = QApplication(sys.argv)
    app.setOverrideCursor(Qt.BlankCursor)

    stylesheet = load_stylesheet()
    app.setStyleSheet(stylesheet)

    #correct_password = "1234"
    #dialog = PasswordDialog(correct_password)
    #if dialog.exec() == QDialog.Accepted:
    #    print("Contraseña correcta, iniciando el juego...")

    bienvenida()

    ventanaPreguntas = QWidget()
    ventanaPreguntas.setWindowTitle("Trivia")
    ventanaPreguntas.setStyleSheet(stylesheet)
    ventanaPreguntas.setWindowFlag(Qt.FramelessWindowHint)
    ventanaPreguntas.showFullScreen()

    layout = QVBoxLayout()
    layout.setAlignment(Qt.AlignCenter)
    ventanaPreguntas.setLayout(layout)

    question_display = QLabel()
    question_display.setAlignment(Qt.AlignCenter)
    layout.addWidget(question_display)

    buttons_layout = QGridLayout()
    layout.addLayout(buttons_layout)

    answer_buttons = [QPushButton() for _ in range(4)]
    for i, button in enumerate(answer_buttons):
        buttons_layout.addWidget(button, i // 2, i % 2)

    cargarPregunta(question_display, answer_buttons)

    glitch_timer = QTimer()
    glitch_timer.timeout.connect(lambda: glitch_effect(question_display, current_question.text))
    glitch_timer.start(3000)  # Cada 3 segundos se ejecuta el efecto de glitch
    
    ventanaPreguntas.show()
    if termino == False:
        app.exec()
    if termino == True:
        print("Termino el Juego")
        termino = False

while True:
    main() 
    print("Reiniciando el juego...")
