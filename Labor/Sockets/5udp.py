import socket

server_ip = '141.37.168.26'
port_start = 1
port_end = 1
open_ports = []
error_msg_ports = []
no_msg_ports = []
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(1)

for port in range(port_start, port_end + 1):
    try:
        sock.sendto('I AM MESSAGE'.encode(), (server_ip, port))
        # Receive a response from the port
        data, addr = sock.recvfrom(1024)
        print('Antwort von Port {}: {}'.format(port, data))
        open_ports.append(port)
    except socket.error as e:
        if e.errno == 10054:
            error_msg_ports.append(port)
        else:
            no_msg_ports.append(port)
sock.close()

print(f'Offene Ports: {open_ports}\nPorts mit Error-Code 10054: {error_msg_ports}\nPorts ohne Antwort: {no_msg_ports}')

# Result:
# Antwort von Port 7: b'I AM MESSAGE'
# Antwort von Port 13: b'12:42:46 20.12.2022\n'
# Antwort von Port 17: b'"When a stupid man is doing something he is ashamed of, he always declares\r\n
#                        that it is his duty." George Bernard Shaw (1856-1950)\r\x00'
# Offene Ports: [7, 13, 17]
# Ports mit Error-Code 10054: []
# Ports ohne Antwort: [1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 12, 14, 15, 16, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29,
#                      30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50]
