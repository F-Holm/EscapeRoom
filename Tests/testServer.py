import socket
from enum import Enum

class Codigos(Enum):
    START = b'\x00'
    RESTART = b'\x01'
    STOP = b'\x02'
    CLOSE = b'\x03'
    TERMINO = b'\x04'

# Crear un socket TCP/IP
cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conectar al servidor
#ip_servidor = "192.168.1.10"
ip_servidor = input("Ingrese la ip del servidor: ")
cliente.connect((ip_servidor, 8080))

# Enviar datos
while True:
    num = int(input("Ingrese un mensaje: "))
    if (num == 1):
        cliente.sendall(Codigos.START.value)
    if (num == 2):
        cliente.sendall(Codigos.RESTART.value)
    if (num == 3):
        cliente.sendall(Codigos.STOP.value)
    if (num == 4):
        cliente.sendall(Codigos.CLOSE.value)
    if (num == 5):
        cliente.sendall(Codigos.TERMINO.value)
    if (num == 6):
        break

# Cerrar la conexión
cliente.close()