import logging
import lossy_udp_socket
import PackageManager as pm


format = "%(asctime)s: %(message)s"
logging.basicConfig(format=format, level=logging.INFO,
                    datefmt="%H:%M:%S")


allPackages = list()
sentPackageQueue = []
lastAckNum = -1


""" def __init__(self,conn,loc_port,rem_addr,PLR):
    self.none = 0; """


class GoBackN:

    def createConn():
        obj = "?"

    # t2: wird vom „lossy_udp_socket“ aufgerufen, um empfangene Pakete zu übergeben
    def receive(package):
        dropRate = 0

    def registerAck(msg):
        expectedNum = pm.unpackData(sentPackageQueue[0])[0]
        packageNumReceived = pm.unpackData(msg)[0]
        if (expectedNum != packageNumReceived):
            # package was lost
            logging.info("Package " + expectedNum + " was lost." +
                         " Got " + packageNumReceived + " instead.")
            # timeout is another option to repeat send process
        else:
            sentPackageQueue.pop(0)

    def buildQueue():
        allPackages = pm.packData(
            headerNum=0, content=b'Dies ist ein ewig langer Text den man per UDP uebertragen muss aber sicherstellen soll, dass alles und alles in der richtigen Reihenfolge ankommt!')
        # push for maximum window size
        for n in allPackages:
            GoBackN.addPackageToQueue(n)

    def addPackageToQueue(newPackage):
        if len(sentPackageQueue < 5):
            sentPackageQueue.append(newPackage)
            # initiate send process

        else:
            logging.info("MaxWindowSize reached")


GoBackN.buildQueue()
