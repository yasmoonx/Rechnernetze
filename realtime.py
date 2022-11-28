import threading
import time
import logging
import random

format = "%(asctime)s: %(message)s"
logging.basicConfig(format=format, level=logging.INFO,
                    datefmt="%H:%M:%S")

TIMETRIMFACTOR = 0.01
STARTTIME = 0
CREATIONENDTIME = 1800 * TIMETRIMFACTOR
ENDTIME = 0
KILLSWITCH = 0

stationen_running = list()
""" We can check whether kunden_running is 0 along with creationendtime while yielding """
kunden_running = list()
kunden_running_lock = threading.Lock()

kunden_happy = list()
kunden_happy_lock = threading.Lock()

Stationen = [["Eingang", 0 * TIMETRIMFACTOR, 0],
             ["Wurst", 30 * TIMETRIMFACTOR, 0],
             ["Käse", 60 * TIMETRIMFACTOR, 0],
             ["Kasse", 5 * TIMETRIMFACTOR, 0],
             ["Bäcker", 10 * TIMETRIMFACTOR, 0],
             ["Ausgang", 0 * TIMETRIMFACTOR, 0]]

kundenAnzahl = 0


class realtime:
    def myThread():
        logging.info("start")

    def finalize(self):
        logging.info("Started at %d and ended at %d. Had %d Customers in total.",
                     STARTTIME, ENDTIME, kundenAnzahl)
        kunden_happy_lock.acquire()

        totallyHappyCount = 0
        fullBuyDuration = 0

        for k in kunden_happy:
            if k[3] == 0:
                totallyHappyCount += 1
                fullBuyDuration += (k[2] - k[1])/TIMETRIMFACTOR
        if totallyHappyCount != 0:
            logging.info("Glückliche Kundenanzahl: %d bei einer durchschnittlichen Einkaufszeit von %ds",
                         totallyHappyCount, fullBuyDuration/totallyHappyCount)
        else:
            logging.info("Alle unglücklich :(")

        for s in Stationen:
            logging.info("%s dropped %d percent", s[0], s[2].getDropRate())

    def generateCustomer(self):
        newK = KundIn(kundenAnzahl, random.choice([0, 1]), Stationen)
        runK = threading.Thread(target=newK.is_yielding)
        kunden_running.append(kundenAnzahl)
        """ kunden_running.append([newK, runK]) """
        kundenAnzahl += 1
        runK.start()
        time.sleep(random.randrange(
            1 * TIMETRIMFACTOR, 20 * TIMETRIMFACTOR, 1 * TIMETRIMFACTOR))
        if time.perf_counter <= CREATIONENDTIME:
            self.generateCustomer()

    def main():
        threads = list()
        for i in range(3):
            x = threading.Thread(target=realtime.myThread, args=(""))
            threads.append(x)
            x.start()

        for s in Stationen:
            """ logging.info(s) """
            s[2] = Station(s)
            """ 0 = name; 1 = waitTime; 2 = Klassenreferenz """

        k = KundIn(0, 0, Stationen)
        """ create Kunde with walklist 1 (Typ1) """

        for s in Stationen:
            t = threading.Thread(target=s[2].is_yielding())
            stationen_running.append(t)
            t.start()

        kT = threading.Thread(target=k.is_yielding(), args=(""))
        kT.start()

        STARTTIME = time.perf_counter()
        logging.info("Starttime: %d", STARTTIME)
        CREATIONENDTIME += STARTTIME
        creator = threading.Thread(target=realtime.generateCustomer, args=(""))
        creator.start()


class Thread:
    myVar = "text"

    def is_yielding(self): pass
    """ def wakeUp(self) = threading.Event():
        logging.info("DAMN BRO, I was sleeping!") """


warteListeLock = threading.Lock()


class Station(Thread):
    """ Die Station-Threads werden zu Beginn der
        Simulation gestartet und warten, bis Sie von einem KundIn-Thread aufgeweckt werden. """

    def activateStation(self):
        return self.myEvent

    def getDropRate(self):
        if (self.interested != 0):
            return self.dropped / self.interested
        else:
            return 0

    """ aufgehaltene Hand ist servEv """

    def subscribe(self, kd_id, aufgehalteneHand):
        warteListeLock.acquire()
        self.warteListe.append([kd_id, aufgehalteneHand])
        """ {kd_id: aufgehaltene Hand} for dict """
        self.interested += 1
        warteListeLock.release()
        return self.myEvent

    def unSubscribe(self, kd_id, kundenEvent):
        warteListeLock.acquire()
        self.dropped += 1
        self.warteListe.remove([kd_id, kundenEvent])
        warteListeLock.release()
    """ We could count in here the Skips to but would have to make sure unsubscribe is only called when too long waited """

    """ Die Zeit für die Bedienung einer KundIn wird simuliert,
    in dem sich der Station-Thread für die Bediendauer schlafen legt. (done)
    Das wird über die sleep-Funktion aus dem Modul time realisiert.
    Danach wird die bediente KundIn aufgeweckt. (WANN WURDE DIE ÜBERHAUPT EINGESCHLÄFERT?)
    Wenn keine weiteren KundInnen in der Warteschlange sind, wartet die Station auf die
    Ankunft des nächsten Kunden """

    def is_yielding(self):
        """ while not self.myEvent.is_set():
            notAwake = 1 """

        self.myEvent.wait()
        logging.info("received SET Event at %s", self.name)

        warteListeLock.acquire()
        currentKD = self.warteListe.pop(0)
        warteListeLock.release()
        logging.info("servingCustomer(at %s): '%d'",
                     self.name, currentKD[0])
        time.sleep(self.waitTime)
        logging.info("servedCustomer(at %s): '%d'",
                     self.name, currentKD[0])

        """ currentKD[1].set() """

        if len(self.warteListe) != 0:
            self.is_yielding()
        else:
            """ self.myEvent.isSet = False """
            self.myEvent.clear()
            logging.info("(w) - %s is waiting for customers",
                         self.name)
            self.is_yielding()

    def __init__(self, name):
        logging.info("newStation: '%s' is waiting for customers", name[0])
        self.name = name[0]
        self.waitTime = name[1]
        self.dropped = 0
        self.interested = 0
        self.myEvent = threading.Event()
        self.warteListe = list()


class KundIn(Thread):
    """ Die KundIn-Threads werden zum Beginn des Einkaufs gestartet. Das Einkaufen im Supermarkt zwischen
    den Stationen wird simuliert, in dem der Thread schlafen gelegt wird (time.sleep). Wenn eine KundIn
    an einer Station eintrifft, wird die KundIn in die Warteschlange eingereiht
    und der wartende Stations-Thread aktiviert """

    def __init__(self, kd_id, typ, Stationen):
        self.kd_id = kd_id
        self.typ = typ
        self.skipped = 0
        self.waitingTimes = list()

        self.Stationen = Stationen.copy()

        if typ != 0:
            self.Stationen.pop(0)
            self.Stationen.pop(5)

        """ full """
        if typ == 1:
            """ maximale WaitTime, Time to next Station """
            self.waitingTimes.append([10, 10])  # Bäcker
            self.waitingTimes.append([10, 30])  # Wurst
            self.waitingTimes.append([5, 45])  # Käse
            self.waitingTimes.append([20, 60])  # Kasse
        """ leberkäs """
        if typ == 2:
            self.Stationen.pop(1)
            self.waitingTimes.append([5, 30])  # Wurst
            self.waitingTimes.append([20, 30])  # Kasse
            self.waitingTimes.append([20, 20])  # Bäcker

        self.myEvent = threading.Event

        self.startedAt = time.perf_counter
        self.Stationen[0][2].subscribe(kd_id, self.myEvent).set()
        """ wartende Station wird aktiviert """

        """ self.myThread.start() """
        """ nn = self.Stationen[0][2].activateStation
        nn() """

    def is_yielding(self):
        logging.info("Kundenthread started")
        """ while not self.myEvent.is_set():
            notAwake = 1 """
        """ Better not Waiting but checking whether to leave the current location """
        """ if true:
            self.Stationen[0][2].unSubscribe(self.kd_id)
            self.skipped += 1
            self.Stationen.pop(0) """

        self.myEvent.wait()
        logging.info("received SET Event at %s", self.kd_id)

        logging.info("Consumer %s received the package", self.kd_id)
        self.Stationen.removeAt(0)

        if len(self.Stationen) == 0:
            """ FINISHED """
            kunden_running_lock.acquire()
            kunden_running.remove(self.kd_id)
            kunden_running_lock.release()
            kunden_happy_lock.acquire()
            kunden_happy.append(
                [self.kd_id, self.typ, self.startedAt, time.perf_counter, self.skipped])
            kunden_happy_lock.release()
            """ END THREAD """

        """ Subscribe to next after successful """
        nextStation = self.Stationen[0]
        wayToNextStation = 1
        time.sleep(wayToNextStation)
        logging.info(
            "Consumer %s arrived to and waits at %s [WAITLIST: %d]", self.kd_id, nextStation[0], 0)
        """ enter or return len """

        nextStation[2].subscribe(self.kd_id, self.myEvent).set()


realtime.main()
