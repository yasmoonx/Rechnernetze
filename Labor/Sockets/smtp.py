import base64
import socket

def main():
    nl = '\r\n'
    print('Enter data manually or press enter for default values')
    sender= input('Sender mail address:')
    if(sender == ''):
        sender= "scammer@scam.de"
        print('Default:'+sender)
    rcpt= input('Recipient mail address:')
    if(rcpt == ''):
        rcpt= 'yasmin.hoffmann@htwg-konstanz.de' 
        print('Default:'+rcpt)
    subject= input('Email subject:')
    if(subject == ''):
        subject= 'irrelevant'
        print('Default:'+subject)
    content= input('Email content:')
    if(content==''):
        content= 'This is a scam email from me muahaha' 
        print('Default:'+content)


    username = base64.b64encode('rnetin'.encode('utf-8')).decode('utf-8') 
    password = base64.b64encode('Ueben8fuer8RN'.encode('utf-8')).decode('utf-8') 
    mailserver = 'asmtp.htwg-konstanz.de'
    port= 587


    sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.connect((mailserver, port))
    ans = sock.recv(1024).decode()
    if(ans[:3]!= '220' ):
        print('Server not ready! (no 220 answer)')


    sock.send(('EHLO example.net'+nl).encode())
    ans = sock.recv(1024).decode()
    if(ans[:3]!= '250'):
        print('no 250 answer')


    sock.send(('AUTH LOGIN'+nl).encode())
    ans= sock.recv(1024).decode()
    if(ans[:3]!= '334'):
        print('no 334 answer')

    sock.send((username+nl).encode())
    ans= sock.recv(1024).decode()
    if(ans[:3]!= '334'):
        print('no 334 answer')

    sock.send((password+nl).encode())
    ans= sock.recv(1024).decode()
    if(ans[:3]!= '235'):
        print('no 235 answer')

    sock.send(('MAIL FROM: <'+sender+'>'+nl).encode())
    ans= sock.recv(1024).decode()
    if(ans[:3]!= '250'):
        print('no 250 answer')

    sock.send(('RCPT TO: <'+rcpt+'>'+nl).encode())
    ans= sock.recv(1024).decode()
    if(ans[:3]!= '250'):
        print('no 250 answer')

    sock.send(('DATA'+nl).encode())
    ans= sock.recv(1024).decode()
    if(ans[:3]!= '354'):
        print('no 354 answer')

    msg= 'FROM:<' + sender +'>'+ nl
    msg += 'TO:<' + rcpt +'>' + nl
    msg += 'Subject:' + subject + nl
    msg += nl
    msg += content + nl
    msg += '.' + nl

    sock.send(msg.encode())
    ans= sock.recv(1024).decode()
    if(ans[:3] != '250'):
        print('no 250 answer')
    else: 
        print('Email was sent successfully')

    sock.send(('QUIT'+nl).encode())
    ans= sock.recv(1024).decode()
    if(ans[:3] != '221'):
        print('no 221 answer')
    else:
        print(ans)

if __name__ == "__main__":
    main()


       

