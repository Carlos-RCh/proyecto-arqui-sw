import socket
import sys
import psycopg2
import smtplib
from email.mime.text import MIMEText

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

# Función para enviar correo
def send_email(to_email, subject, body):
    from_email = "prueba@consultorio.com"  # Reemplaza con tu correo
    password = "password"  # Reemplaza con tu contraseña

    # Aseguramos que el mensaje se codifique en UTF-8
    msg = MIMEText(body, 'plain', 'utf-8')
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    try:
        # Usamos Gmail como ejemplo
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email, password)
        server.sendmail(from_email, to_email, msg.as_string())
        server.quit()
        print("Correo enviado con éxito")
    except Exception as e:
        print(f"Ocurrió un error al enviar el correo: {e}")


try:
    # Enviar mensaje de inicio para iniciar el servicio de notificación
    message = b'00010sinitnotif'
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
            servicio = mensaje[:5]  # 'notif'
            datos = mensaje[5:].split('|')

            id_usuario = datos[0]  # ID del usuario
            id_cita = datos[1]  # ID de la cita

            print(f"Recibido - ID Usuario: {id_usuario}, ID Cita: {id_cita}")

            # Verificar si el usuario existe
            cursor.execute("SELECT correo FROM usuario WHERE id = %s", (id_usuario,))
            usuario = cursor.fetchone()

            # Verificar si la cita existe
            cursor.execute("SELECT id_horario FROM cita WHERE id = %s", (id_cita,))
            cita = cursor.fetchone()

            if usuario and cita:  # Si el usuario y la cita existen
                correo_usuario = usuario[0]

                # Obtener los detalles de la cita
                id_horario = cita[0]
                cursor.execute("SELECT fecha, horario FROM horario WHERE id = %s", (id_horario,))
                horario = cursor.fetchone()

                if horario:
                    fecha = horario[0]
                    hora = horario[1]

                    # Crear el mensaje para el correo
                    mensaje_cita = f"Hola {usuario[0]}, te recordamos del consultorio UDP que su cita es el {fecha} en el horario {hora}."

                    # Enviar el correo
                    send_email(correo_usuario, "Recordatorio de Cita", mensaje_cita)

                    # Respuesta de éxito
                    respuesta = b'00019notifCitaNotificada'
                    sock.sendall(respuesta)
                else:
                    # Si no existe el horario
                    respuesta = b'00024notifHorarioNoEncontrado'
                    sock.sendall(respuesta)
            else:
                # Si no existe el usuario o la cita
                respuesta = b'00030notifUsuarioOCitaNoEncontrados'
                sock.sendall(respuesta)

finally:
    print('Cerrando socket y conexión a la base de datos')
    sock.close()
    cursor.close()
    conn.close()
