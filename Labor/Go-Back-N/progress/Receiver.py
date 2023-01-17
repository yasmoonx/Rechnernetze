import logging
import struct
from lossy_udp_socket import lossy_udp_socket
from PackageManager import PackageManager as pm


format = "%(asctime)s: %(message)s"
logging.basicConfig(format=format, level=logging.INFO,
                    datefmt="%H:%M:%S")


class ConnHandler():
    # t2: wird vom „lossy_udp_socket“ aufgerufen, um empfangene Pakete zu übergeben
    def receive(package):
        content = pm.unpackData(package)[1]
        headerNum = pm.unpackData(package)[0]
        logging.info("Receiver got %d with %s", headerNum, content)
        content = pm.unpackData(package)[1]
        if content == b'FIN':
            Receiver.printFull()
        else:
            # RECEIVED PACKAGE SPLIT
            Receiver.addSegment(package)


class Receiver():

    fullContent = ""
    lastPackageNumReceived = -1
    sock = 0

    def __init__(self) -> None:
        Receiver.sock = lossy_udp_socket(
            ConnHandler, 50000, 50001, 0.5)

    def printFull():
        print("Final Message Transfer: %s", Receiver.fullContent)

    def addSegment(package: bytes):
        content = pm.unpackData(package)[1]
        Receiver.lastPackageNumReceived = pm.unpackData(package)[0]
        Receiver.fullContent += content.decode("utf-8")
        AckPck = pm.packData(-1, b'ACK' +
                             Receiver.lastPackageNumReceived.to_bytes(1, 'big', signed=False))
        if len(AckPck) > 1:
            print("AHHHHHHHHHHHHHHHHHHHHHH!!!")
        Receiver.sock.send(
            AckPck[0]
        )
