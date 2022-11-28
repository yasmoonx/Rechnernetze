import threading
import time
import logging
import random

format = "%(asctime)s: %(message)s"
logging.basicConfig(format=format, level=logging.INFO,
                    datefmt="%H:%M:%S")

TIMETRIMFACTOR = 0.01

stationen_running = list()  # unused
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


class realtime:
    kundenAnzahl = 0
    allDone = 0
    STARTTIME = 0
    CREATIONENDTIME = 1800 * TIMETRIMFACTOR
    ENDTIME = 0

    def finalize():
        logging.info("Started at %d and ended at %d. Had %d Customers in total.",
                     realtime.STARTTIME, realtime.ENDTIME, realtime.kundenAnzahl)

        kunden_happy_lock.acquire()

        totallyHappyCount = 0
        fullBuyDuration = 0

        """ logging.info("list of customer finalization:") """
        for k in kunden_happy:
            logging.info(k)
            if k[4] == 0:
                totallyHappyCount += 1
                fullBuyDuration += (float(k[2]) - float(k[1]))/TIMETRIMFACTOR
        if totallyHappyCount != 0:
            logging.info("Glückliche Kundenanzahl: %d bei einer durchschnittlichen Einkaufszeit von %ds",
                         totallyHappyCount, fullBuyDuration/totallyHappyCount)
        else:
            logging.info("Alle unglücklich :(")

        for s in Stationen:
            logging.info("%s dropped %d percent", s[0], s[2].getDropRate())

    def generateCustomer():
        wirdTyp = random.choice([1, 2])
        newK = KundIn(realtime.kundenAnzahl, wirdTyp, Stationen)
        runK = threading.Thread(target=newK.is_yielding)
        kunden_running.append(realtime.kundenAnzahl)
        """ kunden_running.append([newK, runK]) """
        realtime.kundenAnzahl += 1
        runK.start()
        if wirdTyp == 1:
            time.sleep(60*TIMETRIMFACTOR)
        else:
            time.sleep(200*TIMETRIMFACTOR)
        if float(time.perf_counter()) < realtime.CREATIONENDTIME:
            realtime.generateCustomer()
        else:
            logging.info("STOPPED GENERATING NEW CUSTOMERS AT %f",
                         time.perf_counter())

    def main():
        for s in Stationen:
            s[2] = Station(s)
            """ 0 = name; 1 = waitTime; 2 = Klassenreferenz """

        for s in Stationen:
            t = threading.Thread(target=s[2].is_yielding)
            stationen_running.append(t)
            t.start()

        """ create Kunde with walklist 1 (Typ1) """
        """ k = KundIn(0, 1, Stationen)
        kunden_running.append(0)

        kT = threading.Thread(target=k.is_yielding)
        kT.start() """

        realtime.STARTTIME = time.perf_counter()
        realtime.CREATIONENDTIME += realtime.STARTTIME
        creator = threading.Thread(target=realtime.generateCustomer)
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

    def getLen(self):  # noLock for this operation
        return len(self.warteListe)

    def activateStation(self):
        return self.myEvent

    def getDropRate(self):
        if (self.interested != 0):
            return self.dropped / self.interested
        else:
            return 0

    """ aufgehaltene Hand ist servEv """

    def subscribe(self, kd_id, items, aufgehalteneHand):
        logging.info("Kunde %d mit %d items stellt sich an bei %s",
                     kd_id, items, self.name)
        warteListeLock.acquire()
        self.warteListe.append({kd_id: [items, aufgehalteneHand]})
        self.interested += 1
        warteListeLock.release()
        return self.myEvent

    def unSubscribe(self, kd_id):
        logging.info("Kunde %d ist sauer und lässt %s aus",
                     kd_id, self.name)
        warteListeLock.acquire()
        self.dropped += 1
        self.warteListe.remove(kd_id)
        warteListeLock.release()

    """ Die Zeit für die Bedienung einer KundIn wird simuliert,
    in dem sich der Station-Thread für die Bediendauer schlafen legt. (done)
    Das wird über die sleep-Funktion aus dem Modul time realisiert.
    Danach wird die bediente KundIn aufgeweckt.
    Wenn keine weiteren KundInnen in der Warteschlange sind, wartet die Station auf die
    Ankunft des nächsten Kunden """

    def is_yielding(self):

        logging.info("'%s' is waiting for customers", self.name)
        """ self.myEvent.wait() """
        while not self.myEvent.is_set():
            if realtime.allDone == 1:
                logging.info("Station %s is shutting down.", self.name)
                return
        logging.info("received SET Event at %s", self.name)

        warteListeLock.acquire()
        currentKD = self.warteListe.pop(0)
        warteListeLock.release()
        kd_name = list(currentKD.keys())[0]
        currentKD = list(currentKD.values())[0]
        currentKDItems = currentKD[0]
        currentKDEvent = currentKD[1]
        logging.info("servingCustomer(at %s): '%d'",
                     self.name, kd_name)
        # TIMETRIM already in waitTime
        time.sleep(self.waitTime * currentKDItems)
        logging.info("servedCustomer(at %s): '%d'",
                     self.name, kd_name)

        currentKDEvent.set()

        if len(self.warteListe) != 0:
            self.is_yielding()
        else:
            self.myEvent.clear()
            """ logging.info("(just served) - %s will be waiting for customers",
                         self.name) """
            self.is_yielding()

    def __init__(self, name):
        logging.info("newStation: %s", name[0])
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
            self.Stationen.pop(4)

        """ ["Wurst", 30 * TIMETRIMFACTOR, 0],
             ["Käse", 60 * TIMETRIMFACTOR, 0],
             ["Kasse", 5 * TIMETRIMFACTOR, 0],
             ["Bäcker", 10 * TIMETRIMFACTOR, 0], """
        """ full """
        if typ == 1:
            baecker = self.Stationen.pop(3)
            baecker[1] = 10
            self.Stationen.insert(0, baecker)

            self.Stationen[1][1] = 5
            self.Stationen[2][1] = 3
            self.Stationen[3][1] = 30

            """ maximale WaitTime, Time to next Station """
            self.waitingTimes.append([10, 10])  # Bäcker
            self.waitingTimes.append([10, 30])  # Wurst
            self.waitingTimes.append([5, 45])  # Käse
            self.waitingTimes.append([20, 60])  # Kasse
        """ leberkäs """
        if typ == 2:
            self.Stationen.pop(1)  # remove Käse

            self.Stationen[0][1] = 2
            self.Stationen[1][1] = 3
            self.Stationen[2][1] = 3

            self.waitingTimes.append([5, 30])  # Wurst
            self.waitingTimes.append([20, 30])  # Kasse
            self.waitingTimes.append([20, 20])  # Bäcker

        self.myEvent = threading.Event()

        self.startedAt = time.perf_counter()

        logging.info(
            "Kunde %d betritt den Laden und läuft zu erster Station", kd_id)
        time.sleep(self.waitingTimes[0][0]*TIMETRIMFACTOR)

        self.Stationen[0][2].subscribe(
            kd_id, self.Stationen[0][1], self.myEvent).set()
        """ wartende Station wird aktiviert """

    def is_yielding(self):
        logging.info(
            "Kundenthread zu %d started and waits to receive package", self.kd_id)

        """ while not self.myEvent.is_set():
            notAwake = 1 """
        """ Better not Waiting but checking whether to leave the current location """

        self.myEvent.wait()

        """ logging.info("received SET Event at Kunde %s", self.kd_id) """

        logging.info("Consumer %s received the package", self.kd_id)
        self.Stationen.pop(0)

        if len(self.Stationen) == 0:
            """ FINISHED """
            logging.info(
                "KUNDE %d VON TYP %d IST FERTIG UND VERLÄSST DEN LADEN", self.kd_id, self.typ)
            kunden_running_lock.acquire()
            kunden_running.remove(self.kd_id)
            if len(kunden_running) == 0:
                realtime.allDone = 1
                realtime.ENDTIME = time.perf_counter()
            kunden_running_lock.release()
            kunden_happy_lock.acquire()
            kunden_happy.append(
                [self.kd_id, self.typ, self.startedAt, time.perf_counter(), self.skipped])
            kunden_happy_lock.release()
            if realtime.allDone == 1:
                realtime.finalize()
            """ END THREAD """
            return

        """ Subscribe to next after successful """
        nextStation = self.Stationen[0]
        wayToNextStation = self.waitingTimes.pop(0)[1]
        logging.info("Kunde %d geht %s lang zu nächster Station (just started)",
                     self.kd_id, wayToNextStation)
        time.sleep(wayToNextStation*TIMETRIMFACTOR)
        logging.info(
            "Consumer %s arrived to and waits at %s [LEN(WAITLIST) at arrival: %d]", self.kd_id, nextStation[0], nextStation[2].getLen())

        self.myEvent.clear()

        nextStation[2].subscribe(
            self.kd_id, nextStation[1], self.myEvent).set()

        if nextStation[2].getLen() > 7:
            self.Stationen[0][2].unSubscribe(self.kd_id)
            self.skipped += 1
            self.Stationen.pop(0)
            self.waitingTimes.pop(0)

        self.is_yielding()


realtime.main()
