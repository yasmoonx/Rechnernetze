import base64
import socket

username = base64.b64encode('rnetin'.encode('utf-8')).decode('utf-8')
password = base64.b64encode(
    'Ueben8fuer8RN'.encode('utf-8')).decode('utf-8')
mailserver = 'asmtp.htwg-konstanz.de'
port = 587

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((mailserver, port))


def main():
    nl = '\r\n'
    print('Enter data manually or press enter for default values')
    sender = input('Sender mail address:')
    if(sender == ''):
        sender = "scammer@scam.de"
        print('Default:'+sender)
    rcpt = input('Recipient mail address:')
    if(rcpt == ''):
        rcpt = 'yasmin.hoffmann@htwg-konstanz.de'
        print('Default:'+rcpt)
    subject = input('Email subject:')
    if(subject == ''):
        subject = 'irrelevant'
        print('Default:'+subject)
    content = input('Email content:')
    if(content == ''):
        content = 'This is a scam email from me muahaha'
        print('Default:'+content)

    checkCode('220')  # initial server request

    sock.send(('EHLO example.net'+nl).encode())
    checkCode('250')

    sock.send(('AUTH LOGIN'+nl).encode())
    checkCode('334')

    sock.send((username+nl).encode())
    checkCode('334')

    sock.send((password+nl).encode())
    checkCode('235')

    sock.send(('MAIL FROM: <'+sender+'>'+nl).encode())
    checkCode('250')

    sock.send(('RCPT TO: <'+rcpt+'>'+nl).encode())
    checkCode('250')

    sock.send(('DATA'+nl).encode())
    checkCode('354')

    msg = 'FROM:<' + sender + '>' + nl
    msg += 'TO:<' + rcpt + '>' + nl
    msg += 'Subject:' + subject + nl
    msg += nl
    msg += content + nl
    msg += '.' + nl

    sock.send(msg.encode())

    if checkCode('250'):
        print('Email was sent successfully')
    else: 
        print('Sorry, email was not sent.')

    sock.send(('QUIT'+nl).encode())
    checkCode('221')


def checkCode(code):
    ans = sock.recv(1024).decode()
    if(ans[:3] != code):
        print('Error! (no ' + code + ' answer)')
        print(ans)
        return 0
    else: 
        print(ans)
        return 1


if __name__ == "__main__":
    main()
