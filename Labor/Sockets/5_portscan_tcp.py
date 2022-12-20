import socket
import threading

server_ip = '141.37.168.26'
port_start = 1
port_end = 50
open_ports = []
closed_ports = []
continue_scan = True


def scan_port(port):
    global continue_scan

    # Open TCP connection
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    result = sock.connect_ex((server_ip, port))

    # If successfull add port to open port list and close connection
    if result == 0:
        open_ports.append(port)
    else:
        closed_ports.append(port)
    sock.close()

    # Wenn das Flag continue_scan False ist, beende den Thread
    if not continue_scan:
        return


# Start 1 thread per port and add to thread list
threads = []
for port in range(port_start, port_end + 1):
    t = threading.Thread(target=scan_port, args=(port,))
    threads.append(t)
    t.start()

# Wait on threads to have finished
for t in threads:
    t.join()

# Return list of open ports
print(f'Offene Ports: {open_ports}\nGeschlossene Ports: {closed_ports}')


# Result:
# Offene Ports: [7, 9, 17, 13, 19]
# Geschlossene Ports: [50, 39, 38, 27, 33, 43, 45, 40, 36, 35, 32, 31, 28, 48, 34, 16, 15, 12, 30, 4, 29, 3, 47, 1, 44,
#                      21, 22, 18, 10, 5, 49, 46, 42, 41, 24, 23, 8, 26, 25, 20, 14, 2, 6, 37, 11]
#
# Alle geben Error-Code 10035
