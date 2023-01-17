import logging
from math import ceil

""" import struct """

segmentSize = 20
format = "%(asctime)s: %(message)s"
logging.basicConfig(format=format, level=logging.INFO,
                    datefmt="%H:%M:%S")

newPackageCounter = -1


class PackageManager:

    def unpackData(package):
        headerNum = int.from_bytes(package[0:4], "big", signed=False)
        return [headerNum, package[4:]]

    def packData(headerNum: int, content: bytes):
        allPackages = list()

        """ struct.pack() """
        headerBytes = headerNum.to_bytes(2, "big", signed=False)
        headerSize = len(headerBytes)
        newEntry = 0
        if ((headerSize + len(content)) < segmentSize):
            newEntry = (headerBytes + content)
            allPackages.append(newEntry)
        else:
            limit = ceil((headerSize + len(content)) /
                         (segmentSize - headerSize))
            for i in range(headerNum, limit):
                currentHeader = i.to_bytes(2, "big", signed=False)

                # Header needs more Bytes?
                if headerSize != len(currentHeader):
                    headerSize = len(currentHeader)
                    newLimit = ceil(
                        (headerSize + len(content)) / segmentSize)
                    logging.info("limit adjusted - untested")

                maxContentSegSize = (segmentSize - headerSize)
                newEntry = currentHeader + \
                    content[maxContentSegSize *
                            (i-headerNum):maxContentSegSize*((i-headerNum)+1)]
                allPackages.append(newEntry)

        logging.info(allPackages)
        return allPackages

    def test():
        logging.info("FUCK YOU PUTIN")

    def createMessage():
        newPackageCounter = 0
        rt = PackageManager.packData(
            headerNum=newPackageCounter, content=b'Dies ist ein ewig langer Text den man per UDP uebertragen muss aber sicherstellen soll, dass alles und alles in der richtigen Reihenfolge ankommt!')
        """ GoBackNSocket.injectThisAbfuck(rt) """

    def main():
        logging.info("FUCK YOU PYTHON")


PackageManager.createMessage()
