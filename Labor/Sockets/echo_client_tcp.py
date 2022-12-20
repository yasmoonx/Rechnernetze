import socket
import struct
import time

Server_IP = '127.0.0.1'
Server_PORT = 50000
counter = 0


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.settimeout(10)
print('Connecting to TCP server with IP ', Server_IP, ' on Port ', Server_PORT)
sock.connect((Server_IP, Server_PORT))


def buildmsg():
    global counter
    numbers = []
    op = input('Rechenoperation:')
    amount = int(input('Anzahl Zahlen:'))

    for i in range(amount):
        n = int(input('Zahl'+str(i+1)+": "))
        numbers.append(n)

    # ID: unsigned Int I,Operation: utf8 kodiert, N unsignged char B,z als signed Integer i
    byte_stream = struct.pack('I', counter)
    byte_stream += op.encode()
    byte_stream += struct.pack('B', amount)
    for num in numbers:
        byte_stream += struct.pack('i', num)

    print('Sending Message:', counter, op, amount, str(numbers))
    print(byte_stream)
    counter += 1

    return byte_stream


sock.send(buildmsg())
# buildmsg()

try:
    data = sock.recv(1024)
    print('Message received: ', data)
    ID = struct.unpack('I', data[:4])[0]
    RESULT = struct.unpack('i', data[4:])[0]
    print('ID=', ID, '\nResult=', RESULT)
except socket.timeout:
    print('Socket timed out at', time.asctime())
sock.close()
