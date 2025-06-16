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
        # Preguntar si desea salir o autenticarse
        opcion = input("Opción 0) Salir 1) Autenticación: ")

        if opcion == "0":
            print("Saliendo del cliente...")
            break  

        elif opcion == "1":
            # Opción de autenticación
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
            print('Recibido {!r}'.format(data))
            
            mensaje = data.decode()
            datos = mensaje.split('|')

            confirmacion = datos[1]
            if confirmacion == 'true':
                print(" - Acceso exitoso.")
                acceso_permitido = True
            else:
                print(" - Acceso denegado.")
                acceso_permitido = False

            # Si el acceso es exitoso, permite continuar con las opciones de reporte
            if acceso_permitido:
                while True:
                    # Opción de reporte
                    print(" --------------------------------------")
                    opcion2 = input("1) Reporte de Medicos: ")

                    if opcion2 == "1":
                        servicio = b'repor'
                        mensaje = servicio
                        mensaje += b'ver|'
                        while True:
                                filtro = input(" - Especialidad (Pediatria, Cardiologia, General, Dermatologa) o Todos: ").strip()
                                if filtro in ['Pediatria', 'Cardiologia', 'General', 'Dermatologa', 'Todos']:
                                    mensaje += filtro.encode()
                                    break
                                else:
                                    print(" Opción inválida !")

                    else:
                        print(" Opción inválida.")
                        continue

                    # Enviar mensaje de reporte
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
            else:
                print("Acceso denegado.")

        else:
            print("Opción inválida. Elige 0 para salir o 1 para autenticarse.")
            continue

finally:
    print('Cerrando socket')
    sock.close()
