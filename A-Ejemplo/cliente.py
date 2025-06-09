#------------------------------------------------------------
#Ejemplo de cliente SOA que envia un "Hola Mundo" al servidor
#------------------------------------------------------------

import socket # conexiones de red (un socket TCP/IP).
import sys

# Create a TCP/IP socket
sock = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
# -protocolo de direcciones IPv4 y socket stream


# Connect the socket to the port where the bus is listening
bus_address = ('localhost', 5000)
print ('connecting to {} port {}'.format (*bus_address))
sock.connect (bus_address)



try:
    while True:
      # Send Hello world to servi
      if (input ('Send Hello world to servi ? y/n: ') != 'y'):
        break
      
      
      message = b'00016serviHello world' # convierte mensaje en bytes
      print ('sending {!r}'.format (message))
      sock.sendall (message)


      # Look for the response
      print ("Waiting for transaction")
      amount_received = 0
      amount_expected = int(sock.recv (5)) 
      # lee primeros 5 bytes y vuelve numeros enteros

      # recibe todos los bytes separados 
      while amount_received < amount_expected:
          data = sock.recv (amount_expected - amount_received)
          amount_received += len (data)
      
                
      print ("Checking servi answer ...")
      print('received {!r}'.format(data))

finally:
    print ('closing socket')
    sock.close ()



