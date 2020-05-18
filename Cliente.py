import socket
import sys

# VER CURSO SECCION 7 ENTRADAS Y SALIDAS DE DATOS > 'SCRIPTS'


CABECERA = 64
PORT = 5050
FORMATO = 'utf-8'
MENSAJE_DESCONECTADO = "!DESCONECTANDO"
SERVER = "192.168.56.1" #ubicacion del servidor
ADDR = (SERVER, PORT)
cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect(ADDR) #Aca nos conectamos con el servidor

def send(msje):
    mensaje = msje.encode(FORMATO)
    mensaje_longitud = len(mensaje)
    send_lenght = str(mensaje_longitud).encode(FORMATO)
    send_lenght += b' ' * (CABECERA - len(send_lenght))
    cliente.send(send_lenght)
    cliente.send(mensaje)
    print(cliente.recv(2048).decode(FORMATO))


send(sys.argv[1])
send(MENSAJE_DESCONECTADO)