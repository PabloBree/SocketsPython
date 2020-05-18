import socket
import threading
from io import open

# VER CURSO SECCION 14 MANEJO DE FICHEROS > 'Ficheros de texto'

USUARIO = 'Pablo'
PSW = 'Bressi'

CABECERA = 64 #esta variable lo que indica es que el primer mensaje que tiene que recibir el server es de 64 bytes e indica el tamano del mensaje que va a recibir el server posteriormente
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname()) #esta funcion permite automaticamente obtener la IPV4 Address para no tener que hardcodear y tener que estar cambiandola manualmente.
ADDR = (SERVER, PORT)
FORMATO = 'utf-8'
MENSAJE_DESCONECTADO = "!DESCONECTANDO"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #con esto creamos el espacio de conexion
server.bind(ADDR)

def revisarPermiso(msg):
    espacio = msg.find(' ')
    usuario = msg[0:espacio]
    contra = msg[espacio+1:]



    fichero = open('Autentificación.txt','r')
    texto = fichero.read()
    fichero.close()

    registro1 = texto.find(' ')
    usuarioCorrecto = texto[0:registro1]
    contraCorrecta = texto[registro1+1:]

    print("Tamano total del archivo {}".format(len(texto)))
    print("Espacio posicion: {} \n".format(registro1))
    print("Usuario: {}  tamano {} \n".format(usuario, len(usuarioCorrecto)))
    print("Contrasena: {}  tamano {} \n".format(contra, len(contraCorrecta)))

    if usuario == usuarioCorrecto and contra == contraCorrecta:
        return True
    else:
        return False

def manejar_cliente(conn, addr): #esta funcion maneja cada conexion de manera individual
    print("[NUEVA CONEXION] {} conectado".format(addr))
    conectado = True

    usuario = False
    contra = False

    while conectado:
        mensaje_longitud = conn.recv(CABECERA).decode(FORMATO)

        if mensaje_longitud:
            mensaje_longitud = int(mensaje_longitud)
            mensaje = conn.recv(mensaje_longitud).decode(FORMATO)

            if mensaje == MENSAJE_DESCONECTADO:
                conectado = False

            print("[IP|PUERTO>{}] Dice; {}".format(addr,mensaje))
            conn.send("Mensaje recibido {}".format(mensaje).encode(FORMATO))

            if mensaje != MENSAJE_DESCONECTADO:
                if revisarPermiso(mensaje):
                    conn.send("Autorizado".encode(FORMATO))
                else:
                    conn.send("Rechazado... Desconectandolo".encode(FORMATO))
                    conectado = False





    conn.close()

def start(): #Esta funcion maneja conexiones nuevas
    server.listen() #empieza a escuchar para posibles conexiones
    print("[ESCUCHANDO] El server esta escuchando en {}".format(SERVER))
    while True:
        conn, addr = server.accept() #en la variable conn se guarda la informacion del cliente para poder enviarle despues informacion.
        thread = threading.Thread(target=manejar_cliente, args=(conn, addr))  #cuando una conexion nueva aparece, generamos un thread nuevo enviandoselo a la funcion manejar_cliente con sus respectivos argumentos
        thread.start()
        print("[CLIENTES CONECTADOS] {} ".format(threading.active_count()-1))

print("[EMPEZANDO] El server esta comenzando...")
start()