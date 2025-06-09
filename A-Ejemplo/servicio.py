

#------------------------------------------------------------
#Ejemplo de servicio SOA que procesa la transaccion recibida
#------------------------------------------------------------
import socket
import sys

# Create a TCP/IP socket
sock = socket.socket (socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the bus is listening
bus_address = ('localhost', 5000)
print ('connecting to {} port {}'.format (*bus_address))
sock.connect (bus_address)


try:
    # Send data
    message = b'00010sinitservi' # mensaje en bytes
    print ('sending {!r}'.format (message)) 
    sock.sendall (message)
    sinit = 1

    while True:
      # Look for the response
      print ("Waiting for transaction")
      amount_received = 0
      amount_expected = int(sock.recv (5)) 
      # recibe 5 primeros y vuelve numeros enteros
      

      while amount_received < amount_expected:
          data = sock.recv (amount_expected - amount_received)
          amount_received += len (data)
          
          
      print ("Procesing ...")
      print('received {!r}'.format(data))
      
      if (sinit == 1): # mensaje init iniciador
        sinit = 0
        print ('Received sinit answer')
      else:
        print ("Send answer") # mensajes clientes
        message = b'00013serviReceived'
        print ('sending {!r}'.format (message))
        sock.sendall (message)

finally:
    print ('closing socket')
    sock.close ()

