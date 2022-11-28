import threading
import time
import logging

format = "%(asctime)s: %(message)s"
logging.basicConfig(format=format, level=logging.INFO,
                    datefmt="%H:%M:%S")


class realtime:
    def myThread():
        logging.info("start")

    def main():
        threads = list()
        for i in range(3*3):
            x = threading.Thread(target=realtime.myThread, args=(""))
            threads.append(x)
            x.start()

        Stationen = [["Eingang", 0, 0],
                     ["Wurst", 30, 0],
                     ["Käse", 60, 0],
                     ["Kasse", 5, 0],
                     ["Bäcker", 10, 0],
                     ["Ausgang", 0, 0]]

        for s in Stationen:
            """ logging.info(s) """
            s[2] = Station(s)

        k = KundIn(0, 0, Stationen)
        """ create Kunde with walklist 1 (Typ1) """

        stationen_running = list()
        for s in Stationen:
            t = threading.Thread(target=s[2].is_yielding())
            stationen_running.append(t)
            t.start()


class Thread:
    myVar = "text"

    """ def wakeUp(self) = threading.Event():
        logging.info("DAMN BRO, I was sleeping!") """


class Station(Thread):

    def newKunde(self, kd_id):
        self.warteListe.append(kd_id)
        return self.myEvent

    def is_yielding(self):
        while not self.myEvent.is_set():
            x = 0
        logging.info("received SET Event at %s", self.name)
        currentKD = self.warteListe.pop(0)
        logging.info("servingCustomer(at %s): '%d'",
                     self.name, currentKD)
        time.sleep(self.waitTime)
        logging.info("servedCustomer(at %s): '%d'",
                     self.name, currentKD)
        """ self.myEvent.isSet = 0 """
        """ self.is_yielding() """

    def __init__(self, name):
        logging.info("newStation: '%s' is waiting for customers", name[0])
        self.name = name[0]
        self.waitTime = name[1]
        self.myEvent = threading.Event()
        self.warteListe = list()


class KundIn(Thread):
    """ Die KundIn-Threads werden zum Beginn des Einkaufs gestartet. Das Einkaufen im Supermarkt zwischen
    den Stationen wird simuliert, in dem der Thread schlafen gelegt wird (time.sleep). Wenn eine KundIn
    an einer Station eintrifft, wird die KundIn in die Warteschlange eingereiht
    und der wartende Stations-Thread aktiviert """

    def __init__(self, kd_id, typ, Stationen):
        self.kd_id = 0
        self.myThread = threading.Thread(target=self)
        self.walkList = []

        if typ == 0:
            for s in Stationen:
                self.walkList.append(s[2].newKunde(kd_id))
        if typ == 1:
            self.walkList.append(s[0][2].newKunde(kd_id))
        logging.info(
            "Created Customer of Type %d with ID: %d determined to walk: %s", typ, kd_id, self.walkList)

        self.walkList.pop(0).set()

    def doSmth(self):
        logging.info("did something")


realtime.main()
