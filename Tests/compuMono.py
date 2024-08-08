import socket

# Crear un socket TCP/IP
servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Obtener la IP privada de la computadora
hostname = socket.gethostname()
ip_privada = socket.gethostbyname(hostname)

# Enlazar el socket a la dirección y puerto
servidor.bind((ip_privada, 8080))

# Mostrar la IP privada y el puerto
print(f"Servidor iniciado en IP: {ip_privada}, Puerto: 8080")

# Escuchar conexiones entrantes
servidor.listen(1)
print("Esperando conexiones...")

# Aceptar una conexión
conexion, direccion = servidor.accept()
print(f"Conectado a {direccion}")

# Recibir datos
while True:
    datos = conexion.recv(1024)
    if not datos or datos.decode() == chr(0):
        break
    print(f"Recibido: {ord(datos.decode())}")

# Cerrar la conexión
conexion.close()

