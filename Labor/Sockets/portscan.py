import socket
from threading import Thread

Server_IP = '141.37.168.26'
open = []
closed=[]
threads=[]

socket.setdefaulttimeout(10)

def test_tcp(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('Connecting to TCP server with IP ', Server_IP, ' on Port ', port)
    try:
        sock.connect((Server_IP, port))
        open.append(port)
    except:
        closed.append(port)
    sock.close()
    return

for i in range(1,51):
    t=Thread(target=test_tcp,args=(i,))
    threads.append(t)
    
for t in threads:
    t.start()

for t in threads:
    t.join()
   
print('Open ports',sorted(open))
print('Closed ports',sorted(closed))