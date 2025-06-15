import socket
import sys
import psycopg2
import json

# Crear un socket TCP/IP
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conectar al puerto 5000 donde está escuchando el servicio
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

try:
    # Enviar mensaje de inicio para iniciar el servicio de gestión de citas
    message = b'00010sinitgcitas'
    print('Enviando {!r}'.format(message))
    sock.sendall(message)
    
    sinit = 1

    while True:
        print(" [ Esperando transacción ... ]")
        amount_received = 0
        amount_expected = int(sock.recv(5))

        while amount_received < amount_expected:
            data = sock.recv(amount_expected - amount_received)
            amount_received += len(data)

        print(" [ Procesando ... ]")
        print(' -Mensaje recibido {!r}'.format(data))

        if sinit == 1:
            sinit = 0
            print(' -Recibido mensaje de inicio (sinit answer)')
        else:
            mensaje = data.decode()
            servicio = mensaje[:5]  # 'gcita'
            datos = mensaje[5:].split('|')

            # Extraer los datos
            id_cliente = datos[0]
            id_medico = datos[1]
            fecha = datos[2]
            hora = datos[3]

            print(f"Recibido - ID Cliente: {id_cliente}, ID Médico: {id_medico}, Fecha: {fecha}, Hora: {hora}")

            # Verificar si el médico existe
            cursor.execute("SELECT COUNT(*) FROM medico WHERE id_usuario = %s", (id_medico,))
            count = cursor.fetchone()[0]

            if count > 0:  # Si el médico existe, verificar horarios disponibles
                # Extraer el horario y verificar si ya está disponible
                # Separa la fecha y hora
                fecha_hora = {
                    'fecha': fecha,
                    'hora': hora
                }
                # Convertir la fecha y hora a formato JSON
                horario_json = json.dumps(fecha_hora)

                # Verificar si el horario ya existe en los horarios disponibles del médico
                cursor.execute("SELECT horarios_disponibles FROM medico WHERE id_usuario = %s", (id_medico,))
                result = cursor.fetchone()

                if result and result[0]:
                    

                else:
                    

            else:
                # Si el médico no existe, enviar respuesta de fallo
                print(" - El médico no existe.")
                respuesta = b'00018gcitasFallo'
                sock.sendall(respuesta)

finally:
    print('Cerrando socket y conexión a la base de datos')
    sock.close()
    cursor.close()
    conn.close()
