import socket
import time


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
        for n in numbers:
            result *= n
    elif(operation == 'Minimum'):
        min = float('inf')
        for n in numbers:
            if(n < min):
                min = n
        result = min
    elif(operation == 'Maxmimum'):
        max = 0
        for n in numbers:
            if(n > max):
                max = n    
        result= max
    return result
        


#echo_server:udp
sock_udp = socket.socket(socket.AF_INET,
                     socket.SOCK_DGRAM)
sock_udp.bind((My_IP, My_PORT_UDP))

sock_udp.settimeout(10)
t_end = time.time()+server_activity_period  # Ende der Aktivitätsperiode

while time.time() < t_end:
    try:
        data, addr = sock_udp.recvfrom(1024)
        print('received message: '+data.decode('utf-8')+' from ', addr)
        sock_udp.sendto(data[::-1], addr)
    except socket.timeout:
        print('Socket timed out at', time.asctime())

sock_udp.close()

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
        print('received message: ', data.decode('utf-8'), 'from ', addr)
        conn.send(data[::-1])
    except socket.timeout:
        print('Socket timed out at',time.asctime())

sock_tcp.close()
if conn:
    conn.close()