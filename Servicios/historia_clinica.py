import socket
import sys
import psycopg2

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the bus is listening
bus_address = ('localhost', 5000)
# print('Conectando a {} puerto {}'.format(*bus_address))
sock.connect(bus_address)

# Connect to the database
conn = psycopg2.connect(
    dbname="consultorio",
    user="carlos",
    password="213207091",
    host="localhost",
    port="6000"
)
cursor = conn.cursor()

try:
    # Send initial message to start the service
    message = b'00010sinithclin'
    # print('Enviando {!r}'.format(message))
    sock.sendall(message)
    sinit = 1

    while True:
        # Waiting for transaction
        # print(" [ Esperando transacción ... ]")
        amount_received = 0
        amount_expected = int(sock.recv(5))

        while amount_received < amount_expected:
            data = sock.recv(amount_expected - amount_received)
            amount_received += len(data)
        
        print("=" * 40)
        print("       SERVICIO HISTORIA CLÍNICA ")
        
        print(' \n Respuesta : [{!r}]'.format(data))

        if sinit == 1:
            sinit = 0
            print(" Mensaje (sinit answer): servicio OK")
        else:
            mensaje = data.decode()
            servicio = mensaje[:5]  # 'hclin'
            datos = mensaje[5:].split('|')

            # Filtrar los datos recibidos
            accion = datos[0]  # 'ver' o 'crear'

            if accion == 'ver':  # Acción de ver la historia clínica
                id_usuario_paciente = datos[1]  # id_usuario del paciente

                # Verificar si el paciente existe
                cursor.execute("SELECT id FROM paciente WHERE id_usuario = %s", (id_usuario_paciente,))
                paciente = cursor.fetchone()

                if paciente:  # Si el paciente existe
                    id_paciente = paciente[0]

                    # Extraer diagnósticos de la historia clínica del paciente
                    cursor.execute("""
                    SELECT diagnostico FROM historia_clinica WHERE id_paciente = %s
                    """, (id_paciente,))
                    diagnósticos = cursor.fetchall()

                    # Crear una lista de diagnósticos
                    diagnosticos_lista = [diagnostico[0] for diagnostico in diagnósticos]
                    diagnosticos_str = '/'.join(diagnosticos_lista)
                    
                    respuesta = b'hclinDiagnosticos|'
                    respuesta += diagnosticos_str.encode()
                    
                    numero = str(len(respuesta)).rjust(5, '0')
                    respuesta = numero.encode() + respuesta
                    
                    print('Enviando {!r}'.format(respuesta))
                    sock.sendall(respuesta)

                else:
                    # Si no se encuentra el paciente
                    respuesta = b'00024hclinUsuarioNoEncontrado'
                    sock.sendall(respuesta)

            elif accion == 'crear':  # Acción de crear una nueva historia clínica
                id_usuario_paciente = datos[1]  # id_usuario del paciente
                diagnostico = datos[2]
                tratamiento = datos[3]

                # Verificar si el paciente existe
                cursor.execute("SELECT id FROM paciente WHERE id_usuario = %s", (id_usuario_paciente,))
                paciente = cursor.fetchone()

                if paciente:  # Si el paciente existe
                    id_paciente = paciente[0]

                    # Insertar en la tabla historia_clinica
                    cursor.execute("""
                    INSERT INTO historia_clinica (id_paciente, diagnostico, tratamiento)
                    VALUES (%s, %s, %s)
                    """, (id_paciente, diagnostico, tratamiento))

                    conn.commit()

                    # Enviar respuesta de éxito
                    respuesta = b'00026hclinHistoriaClinicaCreada'
                    sock.sendall(respuesta)
                else:
                    # Si no se encuentra el paciente
                    respuesta = b'00024hclinUsuarioNoEncontrado'
                    sock.sendall(respuesta)
        
        print("=" * 40)

finally:
    print('Cerrando socket y conexión a la base de datos')
    sock.close()
    cursor.close()
    conn.close()
