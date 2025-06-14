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
    # Enviar mensaje de inicio
    message = b'00010sinitagmed'
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
            servicio = mensaje[:5]  # 'agmed'
            datos = mensaje[5:].split('|')
            
            # Extraer los datos
            id_medico = datos[0]
            fecha = datos[1]
            hora = datos[2]

            print(f" Recibido - ID Médico: {id_medico}, Fecha: {fecha}, Hora: {hora}")

            # Verificar si el médico existe
            cursor.execute("SELECT COUNT(*) FROM medico WHERE id_usuario = %s", (id_medico,))
            count = cursor.fetchone()[0]
            
            if count > 0:  # Si el médico existe, actualizamos los horarios disponibles
                
                horario = {
                    'fecha': fecha,
                    'hora': hora
                }
                # Convertir el horario a formato JSON
                horario_json = json.dumps(horario)

                # Obtener los horarios actuales (si existen)
                cursor.execute("SELECT horarios_disponibles FROM medico WHERE id_usuario = %s", (id_medico,))
                result = cursor.fetchone()

                if result and result[0]:
                    # Verificar si el dato es ya una lista o no
                    if isinstance(result[0], str):
                        # Si el valor es un string, convertimos a lista
                        horarios_existentes = json.loads(result[0])
                    elif isinstance(result[0], list):
                        # Si ya es una lista, usamos la lista directamente
                        horarios_existentes = result[0]
                    else:
                        # Si el valor no es ni un string ni lista, inicializamos una lista vacía
                        horarios_existentes = []
                else:
                    # Si no existen horarios, inicializamos una nueva lista
                    horarios_existentes = []

                # Agregar el nuevo horario a la lista de horarios existentes
                horarios_existentes.append(horario)

                # Actualizar la columna 'horarios_disponibles' con la lista completa de horarios
                cursor.execute("""
                    UPDATE medico
                    SET horarios_disponibles = %s
                    WHERE id_usuario = %s
                """, (json.dumps(horarios_existentes), id_medico))

                conn.commit()
                print(" - Registro de horarios médicos actualizado correctamente.")
                
                # Enviar respuesta de éxito
                respuesta = b'00020agmedRegistroExitoso'
                sock.sendall(respuesta)
            else:
                # Si el médico no existe, enviar mensaje de fallo
                print(" - El médico no existe.")
                respuesta = b'00018agmedRegistroFallo'
                sock.sendall(respuesta)

finally:
    print('Cerrando socket y conexión a la base de datos')
    sock.close()
    cursor.close()
    conn.close()
