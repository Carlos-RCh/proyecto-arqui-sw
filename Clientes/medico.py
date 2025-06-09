import socket
import sys

# Crear un socket TCP/IP
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conectar al puerto 5000 donde está escuchando el servicio
bus_address = ('localhost', 5000)
print('Conectando a {} puerto {}'.format(*bus_address))
sock.connect(bus_address)
# mensaje = b'hclin'

try:
    while True:
        if input('¿Deseas enviar una transacción? (y/n): ') != 'y':
            break

        opcion = input("Opción 1) Autenticación, 2) Registra Usuario, 3) Agenda Medica, 4) Historia Clinica: ")

        if opcion == "1":
            servicio = b'auten'
            mensaje = servicio
            mensaje += input("Ingresa correo: ").encode() + b' '
            mensaje += input("Ingresa contraseña: ").encode()

        elif opcion == "2":
            servicio = b'ruser'
            mensaje = servicio
            mensaje += input("Ingresa nombre: ").encode() + b' '
            mensaje += input("Ingresa correo: ").encode() + b' '
            mensaje += input("Ingresa contraseña: ").encode() + b' '
            mensaje += b'medico'

        elif opcion == "3":
            servicio = b'agmed'
            mensaje = servicio
            mensaje += input("Ingresa ID medico: ").encode()

        elif opcion == "4":
            servicio = b'hclin'
            mensaje = servicio
            mensaje += input("Ingresa id paciente: ").encode()

        else:
            print("Opción inválida.")
            continue

        numero = str(len(mensaje)).rjust(5, '0')
        mensaje = numero.encode() + mensaje

        print('mensaje en bytes')
        print('sending {!r}'.format(mensaje))
        sock.sendall(mensaje)

        print("Waiting for transaction")
        amount_received = 0
        amount_expected = int(sock.recv(5))

        while amount_received < amount_expected:
            data = sock.recv(amount_expected - amount_received)
            amount_received += len(data)

        print("Checking servi answer ...")
        print('received {!r}'.format(data))

finally:
    print('closing socket')
    sock.close()
