""" from GoBackN import Sender.sentPackageQueue """
import logging
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

    def __init__(self) -> None:
        self.sock = lossy_udp_socket(
            ConnHandler, 50001, 50000, 0)
        Sender.buildQueue(self)

    def buildQueue(self):
        allPackages = pm.packData(
            headerNum=-1, content=b'Dies ist ein ewig langer Text den man per UDP uebertragen muss aber sicherstellen soll, dass alles und alles in der richtigen Reihenfolge ankommt!')
        allPackages.append(pm.packData(-1, b'FIN'))
        logging.info(allPackages)
        # push for maximum window size
        for n in allPackages:
            Sender.addPackageToQueue(self, n)

    def addPackageToQueue(self, newPackage):
        if len(Sender.sentPackageQueue) < 6:
            Sender.sentPackageQueue.append(newPackage)
            # initiate send process
            logging.info("Sending now: %s", newPackage)
            self.sock.send(newPackage)
        else:
            logging.info("MaxWindowSize reached")

    def resendQueue(fromIndex):
        Sender.sentPackageQueue = list()
        for i in range(fromIndex, fromIndex + 5):
            Sender.addPackageToQueue(Sender.allPackages[i])

    def registerAck(msg):
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
            nextPckNum = expectedNum+4
            if nextPckNum < len(Sender.allPackages):
                logging.info("ACK started send of %s",
                             Sender.allPackages[nextPckNum])
                Sender.addPackageToQueue(Sender.allPackages[nextPckNum])
