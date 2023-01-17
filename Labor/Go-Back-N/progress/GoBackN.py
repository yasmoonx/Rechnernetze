import logging
import threading
import lossy_udp_socket
from PackageManager import PackageManager as pm
from Receiver import Receiver
""" from Sender import keepSendingWindowFull """


format = "%(asctime)s: %(message)s"
logging.basicConfig(format=format, level=logging.INFO,
                    datefmt="%H:%M:%S")


allPackages = list()
sentPackageQueue = []
lastAckNum = -1


class ConnHandler():
    def createConn():
        obj = "?"

    # t2: wird vom „lossy_udp_socket“ aufgerufen, um empfangene Pakete zu übergeben
    def receive(package):
        logging.info("got %s", package)
        content = pm.unpackData(package)[1]
        if content == b'ACK':
            GoBackN.registerAck(package)
        elif content == b'FIN':
            Receiver.printFull
        else:
            # RECEIVED PACKAGE SPLIT
            Receiver.recv(content)


class GoBackN:

    def registerAck(msg):
        expectedNum = pm.unpackData(sentPackageQueue[0])[0]
        packageNumReceived = pm.unpackData(msg)[0]
        if (expectedNum != packageNumReceived):
            # package was lost
            logging.info("Package " + expectedNum + " was lost." +
                         " Got " + packageNumReceived + " instead.")
            # timeout is another option to repeat send process (! parallel)
            GoBackN.resendQueue(expectedNum)
        else:
            sentPackageQueue.pop(0)
            GoBackN.addPackageToQueue(allPackages[expectedNum+5])

    def resendQueue(fromIndex):
        sentPackageQueue = list()
        for i in range(fromIndex, fromIndex + 5):
            GoBackN.addPackageToQueue(allPackages[i])

    def buildQueue():
        allPackages = pm.packData(
            headerNum=0, content=b'Dies ist ein ewig langer Text den man per UDP uebertragen muss aber sicherstellen soll, dass alles und alles in der richtigen Reihenfolge ankommt!')
        allPackages.append(pm.packData(len(allPackages)+1, b'FIN'))
        logging.info(pm.unpackData(allPackages[0]))
        # push for maximum window size
        for n in allPackages:
            GoBackN.addPackageToQueue(n)

    def addPackageToQueue(newPackage):
        if len(sentPackageQueue) < 6:
            sentPackageQueue.append(newPackage)
            # initiate send process
            """ sT = threading.Thread(target=Sender.keepSendingWindowFull, args="") """
            """ sT.start() """
            """ lossy_udp_socket(ConnHandler, 50000, 50001, 0) """

        else:
            logging.info("MaxWindowSize reached")


GoBackN.buildQueue()
