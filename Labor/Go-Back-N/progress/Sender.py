""" from GoBackN import Sender.sentPackageQueue """
import logging
from threading import Lock
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
        if content[0:3] == b'ACK':
            AckNum = int.from_bytes(
                content[3:], "big", signed=False)
            logging.info("Sender got %d with ACK%d", headerNum, AckNum)
            Sender.registerAck(AckNum)


class Sender():
    sentPackageQueue = list()
    allPackages = list()
    sock = 0
    mutexList = Lock()

    def __init__(self) -> None:
        Sender.sock = lossy_udp_socket(
            ConnHandler, 50001, 50000, 0)
        Sender.buildQueue()

    def buildQueue():
        Sender.allPackages = pm.packData(
            headerNum=-1, content=b'Dies ist ein ewig langer Text den man per UDP uebertragen muss aber sicherstellen soll, dass alles und alles in der richtigen Reihenfolge ankommt!')
        # Warum auch immer springt dieser Aufruf zwischen den oberen und erfordert manuelle PackageNummer
        Sender.allPackages.append(pm.packData(25, b'FIN')[0])
        logging.info(Sender.allPackages)
        # push for maximum window size
        for n in Sender.allPackages:
            Sender.addPackageToQueue(n, True)

    def addPackageToQueue(newPackage, supressWarning):
        if len(Sender.sentPackageQueue) < 6:
            Sender.sentPackageQueue.append(newPackage)
            # initiate send process

            Sender.sock.send(newPackage)
        elif (supressWarning == False):
            logging.info("MaxWindowSize reached")

    def resendQueue(fromIndex):
        Sender.sentPackageQueue = list()
        for i in range(fromIndex, fromIndex + 5):
            Sender.addPackageToQueue(Sender.allPackages[i], False)

    def registerAck(msg):
        Sender.mutexList.acquire()
        expectedNum = pm.unpackData(Sender.sentPackageQueue[0])[0]
        packageNumReceived = msg
        if (expectedNum != packageNumReceived):
            # package was lost
            logging.info("Package %d was lost. Got %d instead.",
                         expectedNum, packageNumReceived)
            # timeout is another option to repeat send process (! parallel)
            Sender.resendQueue(expectedNum)
        else:
            Sender.sentPackageQueue.pop(0)
            Sender.mutexList.release()
            nextPckNum = expectedNum+4
            if nextPckNum < len(Sender.allPackages):
                print("ACK started send of ",
                      Sender.allPackages[nextPckNum])
                Sender.addPackageToQueue(
                    newPackage=Sender.allPackages[nextPckNum], supressWarning=False)
            else:
                Sender.sock.stop()
