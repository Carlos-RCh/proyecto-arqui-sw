import socket
import sys

# Crear un socket TCP/IP
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conectar al puerto 5000 donde está escuchando el servicio
bus_address = ('localhost', 5000)
print('Conectando a {} puerto {}'.format(*bus_address))
sock.connect(bus_address)

try:
    while True:
        
        opcion = input("Opción 1) Autenticación: ")    

        if opcion == "1":
            # Autenticación de Usuario
            servicio = b'auten'
            mensaje = servicio
            mensaje += input(" - Ingresa correo: ").encode() + b'|'
            mensaje += input(" - Ingresa contraseña: ").encode()

            # Enviar mensaje de autenticación
            numero = str(len(mensaje)).rjust(5, '0')
            mensaje = numero.encode() + mensaje
            print('Enviando {!r}'.format(mensaje))
            sock.sendall(mensaje)

            print(" [ Esperando transacción ... ]")
            amount_received = 0
            amount_expected = int(sock.recv(5))

            while amount_received < amount_expected:
                data = sock.recv(amount_expected - amount_received)
                amount_received += len(data)

            print(" [ Verificando respuesta del servicio ... ]")
            print(' Recibido {!r}'.format(data))
            
            mensaje = data.decode()
            datos = mensaje.split('|')

            confirmacion = datos[1]
            if confirmacion == 'true':
                print(" - Acceso exitoso.")
                acceso_permitido = True
            else:
                print(" - Acceso denegado.")
                acceso_permitido = False
            
            if acceso_permitido:
                while True:
                    opcion2 = input(" Opción 1) Agenda Medica, 2) Historia Clinica: ")
                    
                    if opcion2 == "1":
                       servicio = b'agmed'
                       mensaje = servicio
                       mensaje += input("Ingresa ID medico: ").encode() + b'|'  
                       mensaje += input(" - Ingresa año: ").encode() + b'/'  
                       mensaje += input(" - Ingresa mes: ").encode() + b'/' 
                       mensaje += input(" - Ingresa dia ").encode() + b'|' 
                       mensaje += input(" - Ingresa hora YY:ZZ: ").encode()  
                       
                    elif opcion2 == "2":
                        servicio = b'hclin'
                        mensaje = servicio
                        mensaje += input("Ingresa id paciente: ").encode()

                    else:
                        print(" Opción inválida !")
                        continue

                    # Enviar mensaje 
                    numero = str(len(mensaje)).rjust(5, '0')
                    mensaje = numero.encode() + mensaje
                    print('Enviando {!r}'.format(mensaje))
                    sock.sendall(mensaje)

                    print(" [ Esperando transacción ... ]")
                    amount_received = 0
                    amount_expected = int(sock.recv(5))

                    while amount_received < amount_expected:
                        data = sock.recv(amount_expected - amount_received)
                        amount_received += len(data)

                    print(" [ Verificando respuesta del servicio ... ]")
                    print('Recibido {!r}'.format(data))

                    # Salir del ciclo si el usuario decide no continuar
                    continuar = input("¿Deseas continuar con otra opción? (y/n): ")
                    if continuar.lower() != 'y':
                        break
            #Si no tienne aceso vuelve al menu principal
            else:
                print(" Acceso denegado.")
        
        else:
            print(" Opción inválida !")
            continue

finally:
    print('closing socket')
    sock.close()
