# message = b'00010sinitauten'
# message = b'00013autenReceived'

import socket
import sys
import psycopg2

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
bus_address = ('localhost', 5000)  # Dirección del bus SOA
sock.connect(bus_address)

# Conectar a la base de datos
conn = psycopg2.connect(
    dbname="consultorio",
    user="carlos",
    password="213207091",
    host="localhost",
    port="6000"
)
cursor = conn.cursor()


try:
    mensaje = b'00010sinitauten'
    #print('\n Enviando  : [{!r}]'.format(mensaje))
    sock.sendall(mensaje)
    sinit = 1

    while True:
        
        amount_received = 0                
        amount_expected = int(sock.recv(5))
        data = b""
        while len(data) < amount_expected:
            data += sock.recv(amount_expected - len(data))
        
        print("=" * 40)
        print("       SERVICIO AUTENTICACIÓN ")
        #print(' [Conectando a {} puerto {}]'.format(*bus_address))
        
        print(' \n Respuesta : [{!r}]'.format(data))

        if sinit == 1:            
            sinit = 0
            print(" Mensaje (sinit answer): servicio OK")
        else:
            
            mensaje = data.decode()
            servicio = mensaje[:5]
            datos = mensaje[5:].split('|')
            
            correo = datos[0]
            contrasena = datos[1]
            rol = datos[2]
            print(f" [ Servicio: {servicio}, Correo: {correo}, Contraseña: {contrasena} ]")

            # Verificar si el usuario existe
            cursor.execute("""
                SELECT * FROM usuario WHERE correo = %s AND contrasena = %s AND rol = %s
            """, (correo, contrasena, rol))

            # Si el correo y la contraseña coinciden, obtiene un registro
            usuario = cursor.fetchone()  
            
            # preparar respuesta    
            respuesta = b'auten'
            
            if usuario:
                respuesta += b'AccesoConcedido|'
                respuesta += b'true|'
                respuesta += str(usuario[0]).encode()    
                
            else:
                respuesta += b'AccesoDenegado|'
                respuesta += b'false|'
                respuesta += b'0'
            
            numero = str(len(respuesta)).rjust(5, '0')
            respuesta = numero.encode() + respuesta
            print(' Enviando  : [{!r}]'.format(respuesta))        
            sock.sendall(respuesta)  # Enviar la respuesta al cliente
        
        print("=" * 40)
finally:
    print(' Cerrando socket y conexión a la base de datos')
    sock.close()
    cursor.close()
    conn.close()
