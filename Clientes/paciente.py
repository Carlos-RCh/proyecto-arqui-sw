import socket
import sys

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
bus_address = ('localhost', 5000)
print('Conectando a {} puerto {}'.format(*bus_address))
sock.connect(bus_address)

try:
    while True:

        opcion = input(" Opción 1) Registrar Usuario , 2) Autenticación , 3) Agendar Cita, 4) Notificar Cita : ")
        print(" Ingrese:")
        
        if opcion == "1":
            servicio = b'ruser'
            mensaje = servicio
            mensaje += input(" - Nombre: ").encode() + b'|'
            mensaje += input(" - Correo: ").encode() + b'|'
            mensaje += input(" - Contraseña: ").encode() + b'|'
            mensaje += b'paciente|'
    
            # Validar que se ingrese solo una de las opciones válidas: 'Fonasa', 'Isapre', 'Privado'
            while True:
                seguro_salud = input(" - Seguro de Salud (Fonasa/Isapre/Privado/Ninguno): ").strip()
                if seguro_salud in ['Fonasa', 'Isapre', 'Privado','Ninguno']:
                    mensaje += seguro_salud.encode()
                    break
                else:
                    print(" Opción inválida !")
    
        elif opcion == "2":
            servicio = b'auten'
            mensaje = servicio
            mensaje += input(" - Ingresa correo: ").encode() + b'|'
            mensaje += input(" - Ingresa contraseña: ").encode()


        elif opcion == "3":
            servicio = b'gcita'
            mensaje = servicio
            mensaje += input(" - Ingresa id paciente: ").encode() + b'|'
            mensaje += input(" - Ingresa id medico: ").encode() + b'|'
            mensaje += input(" - Ingresa fecha xx/xx/xx: ").encode() + b'|'
            mensaje += input(" - Ingresa hora YY:ZZ: ").encode()

        elif opcion == "4":
            servicio = b'notif'
            mensaje = servicio
            mensaje += input(" - Ingresa ID de cita: ").encode() + b'|'
            mensaje += input(" - Ingresa correo del paciente: ").encode()
            
        else:
            print(" Opción inválida !")
            continue


        numero = str(len(mensaje)).rjust(5, '0')
        mensaje = numero.encode() + mensaje

        print(' Enviando {!r}'.format(mensaje))
        sock.sendall(mensaje)

        print(" [ Esperando transacción ... ]")
        amount_received = 0
        amount_expected = int(sock.recv(5))

        while amount_received < amount_expected:
            data = sock.recv(amount_expected - amount_received)
            amount_received += len(data)

        print(" [ Verificando respuesta del servicio ... ]")
        print(' Recibido {!r}'.format(data))


finally:
    print('closing socket')
    sock.close()
