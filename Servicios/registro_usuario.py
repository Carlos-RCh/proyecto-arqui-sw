import socket
import sys
import psycopg2

# Crear un socket TCP/IP
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
bus_address = ('localhost', 5000)
print('Conectando a {} puerto {}'.format(*bus_address))
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
# LUEGO LO BORAMOS XD
try:
    # Enviar mensaje de inicio
    message = b'00010sinitruser'
    print('Enviando {!r}'.format(message))
    sock.sendall(message)
    
    sinit = 1

    while True:
        print("Esperando transacción")
        amount_expected = int(sock.recv(5))
        data = b""
        while len(data) < amount_expected:
            data += sock.recv(amount_expected - len(data))

        print("Procesando ...")
        print('Mensaje recibido {!r}'.format(data))

        if sinit == 1:
            sinit = 0
            print('Recibido mensaje de inicio (sinit answer)')
        else:
            mensaje = data.decode()
            servicio = mensaje[:5]
            datos = mensaje[5:].split('|')

            nombre = datos[0]
            correo = datos[1]
            contrasena = datos[2]
            tipo_usuario = datos[3]

            print(f"Servicio: {servicio}, Nombre: {nombre}, Correo: {correo}, Contraseña: {contrasena}, Tipo de Usuario: {tipo_usuario}")

            cursor.execute("""
            INSERT INTO usuario (nombre, correo, contrasena, rol)
            VALUES (%s, %s, %s, %s)
            """, (nombre, correo, contrasena, tipo_usuario))

            if tipo_usuario == "paciente":
                seguro = datos[4]
                cursor.execute("""
                INSERT INTO paciente (id_usuario, seguro_medico)
                VALUES ((SELECT id FROM usuario WHERE correo = %s), %s)
                """, (correo, seguro))
                conn.commit()
                print("Usuario paciente registrado correctamente.")

            elif tipo_usuario == "medico":
                especialidad = datos[4]
                cursor.execute("""
                INSERT INTO medico (id_usuario, especialidad)
                VALUES ((SELECT id FROM usuario WHERE correo = %s), %s)
                """, (correo, especialidad))
                conn.commit()
                print("Usuario médico registrado correctamente.")

            else:
                print("Tipo de usuario no válido")
                otro = b'00013ruserNovalido'
                sock.sendall()
                continue

            # Confirmación
            respuesta = b'00013ruserReceived'
            sock.sendall(respuesta)

finally:
    print('Cerrando socket y conexión a la base de datos')
    sock.close()
    cursor.close()
    conn.close()
