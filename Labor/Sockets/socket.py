import base64
import socket

nl = '/r/n'.encode('utf-8')


def main():
    username = base64.b64encode('rnetin'.encode('utf-8')).decode('utf-8')
    password = base64.b64encode(
        'Ueben8fuer8RN'.encode('utf-8')).decode('utf-8')
    mailserver = 'smtp.'
    clientSocket = socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.connect((mailserver, 587))

    """ print(base64.b64decode('Base64-String').decode('utf-8')) """


main()
