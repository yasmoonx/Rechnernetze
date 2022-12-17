import socket
import time
import struct


My_IP = "127.0.0.1"
My_PORT_UDP = 51000             # 51000 UDP port
My_PORT_TCP = 50000             # 5000 TCP Port
server_activity_period = 30   # Zeit, wie lange der Server aktiv sein soll

def calculate(operation,numbers):
    result = 0
    if(operation =='Summe'):
        for n in numbers:
            result += n
    elif(operation=='Produkt'):
        result =1
        for n in numbers:
            result *= n
    elif(operation == 'Minimum'):
        min = float('inf')
        for n in numbers:
            if(n < min):
                min = n
        result = min
    elif(operation == 'Maximum'):
        max = 0
        for n in numbers:
            if(n > max):
                max = n    
        result= max
    return result

def getAnswer(data):
    copyData = data
    ID = struct.unpack('I',copyData[:4])[0]
    copyData = copyData[4:]             #slice off id
    op = copyData[:5].decode()
    if op!='Summe':   
                              #5 bytes for SUMME
        op = copyData[:7].decode() 
        print(op)              #7 bytes for PRODUKT, MAXIMUM, MINIMUM
        copyData= copyData[7:]          #slice off operation
    else:
        copyData = copyData[5:]         #slice off operation

    amount = struct.unpack('B',copyData[:1])[0]
    copyData = copyData[1:]             #slice off N
    numbers= []
    for i in range(amount):
        n = struct.unpack('i', copyData[:4])[0]
        numbers.append(n)
        copyData = copyData[4:]         #slice off number


        
    solution = calculate(op,numbers)
    answer = struct.pack('Ii', ID, solution)
    return answer


#echo_server:tcp

sock_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)            # (IPV4 adresse, )
sock_tcp.bind((My_IP, My_PORT_TCP))                                         # (Darf kontaktieren, schreibt darauf)
print('Listening on Port ',My_PORT_TCP, ' for incoming TCP connections')

t_end=time.time()+server_activity_period                            # Ende der Aktivitätsperiode

sock_tcp.listen(1)
print('Listening ...')

while time.time()<t_end:
    try:
        conn, addr = sock_tcp.accept()
        print('Incoming connection accepted: ', addr)
        break
    except socket.timeout:
        print('Socket timed out listening',time.asctime())

while time.time()<t_end:
    try:
        data = conn.recv(1024)
        if not data: # receiving empty messages means that the socket other side closed the socket
            print('Connection closed from other side')
            print('Closing ...')
            conn.close()
            break
        print('received message: ', data, 'from ', addr)

        #attention: unpack is a tuple(data,)
        

        conn.send(getAnswer(data))
        #conn.send(data[::-1])
        
    except socket.timeout:
        print('Socket timed out at',time.asctime())

sock_tcp.close()
if conn:
    conn.close()

#echo_server:udp
sock_udp = socket.socket(socket.AF_INET,
                     socket.SOCK_DGRAM)
sock_udp.bind((My_IP, My_PORT_UDP))

sock_udp.settimeout(10)
t_end = time.time()+server_activity_period  # Ende der Aktivitätsperiode

while time.time() < t_end:
    try:
        data, addr = sock_udp.recvfrom(1024)
        print('received message: ',data,' from ', addr)
        #sock_udp.sendto(data[::-1], addr)
        sock_udp.sendto(getAnswer(data),addr)
    except socket.timeout:
        print('Socket timed out at', time.asctime())

sock_udp.close()

