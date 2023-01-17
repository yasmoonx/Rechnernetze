import logging
from threading import Lock
from math import ceil

segmentSize = 20
format = "%(asctime)s: %(message)s"
logging.basicConfig(format=format, level=logging.INFO,
                    datefmt="%H:%M:%S")


class PackageManager:
    newPackageCounter: int = 0
    mutexPC = Lock()

    def unpackData(package):
        headerNum = int.from_bytes(package[0:2], "big", signed=False)
        return [headerNum, package[2:]]

    def packData(headerNum: int, content: bytes):
        allPackages = list()
        if headerNum == -1:
            PackageManager.mutexPC.acquire()
            headerNum = PackageManager.newPackageCounter
            PackageManager.newPackageCounter += 1
            PackageManager.mutexPC.release()

        headerBytes = headerNum.to_bytes(2, "big", signed=False)
        headerSize = len(headerBytes)
        newEntry = 0
        if ((headerSize + len(content)) < segmentSize):
            newEntry = (headerBytes + content)
            allPackages.append(newEntry)
        else:
            limit = ceil((headerSize + len(content)) /
                         (segmentSize - headerSize))
            """ for i in range(headerNum, limit): """
            i = headerNum
            while i < limit:
                currentHeader = i.to_bytes(2, "big", signed=False)

                # Header needs more Bytes?
                if headerSize != len(currentHeader):
                    headerSize = len(currentHeader)
                    limit = ceil(
                        (headerSize + len(content)) / segmentSize)
                    logging.info("limit adjusted - untested")

                maxContentSegSize = (segmentSize - headerSize)
                newEntry = currentHeader + \
                    content[maxContentSegSize *
                            (i-headerNum):maxContentSegSize*((i-headerNum)+1)]
                allPackages.append(newEntry)
                i = i+1

        """ logging.info("PM created until %d", PackageManager.newPackageCounter) """
        return allPackages

    """ def createMessage():
        PackageManager.packData(
            headerNum=PackageManager.newPackageCounter, content=b'Dies ist ein ewig langer Text den man per UDP uebertragen muss aber sicherstellen soll, dass alles und alles in der richtigen Reihenfolge ankommt!')
 """


""" 
PackageManager.createMessage() """
