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
ip_servidor = input("Ingrese la dirección IP del servidor: ")
cliente.connect((ip_servidor, 8080))

# Enviar datos
while True:
    mensaje = int(input("Ingrese un mensaje: "))
    if (mensaje == ""): continue
    cliente.sendall(Codigos.START.value)
    if mensaje == "0":
        break

# Cerrar la conexión
cliente.close()

