from collections import deque
import heapq

f = open("supermarkt.txt", "w")
fc = open("supermarkt_customer.txt", "w")
fs = open("supermarkt_station.txt", "w")



# print on console and into supermarket log
def my_print(msg):
    print(msg)
    f.write(msg + '\n')


# print on console and into customer log
# k: customer name
# s: station name
def my_print1(k, s, msg):
    t = EvQueue.time
    print(str(round(t, 4)) + ':' + k + ' ' + msg + ' at ' + s)
    fc.write(str(round(t, 4)) + ':' + k + ' ' + msg + ' at ' + s + '\n')


# print on console and into station log
# s: station name
# name: customer name
def my_print2(s, msg, name):
    t = EvQueue.time
    # print(str(round(t,4))+':'+s+' '+msg)
    fs.write(str(round(t, 4)) + ':' + s + ' ' + msg + ' ' + name + '\n')


# class consists of instance variables:
# t: time stamp
# work: job to be done
# args: list of arguments for job to be done
# prio: used to give leaving, being served, and arrival different priorities
class Ev:
    counter = 0

    def __init__(self, t, work, args=(), prio=255):
        self.t = t
        self.n = Ev.counter
        self.work = work
        self.args = args
        self.prio = prio
        Ev.counter += 1

    #fixes error: 'lesser than' not supported for Ev
    def __lt__(self, other):
        if(self.t==other.t):
            if(self.prio==other.prio):
                return self.n < other.n
            else:
                return self.prio > other.prio
        else:
            return self.t < other.t 



# class consists of
# q: event queue
# time: current time
# evCount: counter of all popped events
# methods push, pop, and start as described in the problem description

class EvQueue:
# please implement here

    time = 0
    evCount = 0

    def __init__(self) :
        self.q = []
    
    def pop(self):
        event = heapq.heappop(self.q)
        #update time
        EvQueue.time = event.t  
        #call ereignisfunktion with args
        event.work(event.args)
        return event
        
    def push(self,event):
        heapq.heappush(self.q,event)
        EvQueue.evCount+=1
    
    def start(self):
        #pop events till EvQueue is empty
        while len(self.q) > 0:
           self.pop()
            
            


# class consists of
# name: station name
# buffer: customer queue
# delay_per_item: service time
# CustomerWaiting, busy: possible states of this station
class Station():
    # please implement here
    def __init__(self,delay_per_item,name) :
        self.delay_per_item = delay_per_item
        self.name = name
        self.buffer = []
        self.busy = False

    def queue(self,customer):
        #customer stands in queue
        self.buffer.append(customer)

        if self.busy == False: #if station not busy
            self.busy = True
            T,station,N,W = customer.list[0]
            ev = Ev(EvQueue.time + (N*self.delay_per_item), work=self.done,args=customer,prio=2)
            evQ.push(ev)
            my_print2(self.name,'serves',customer.name)


    def done(self,customer):
        Customer.served[self.name]+=1 #customer was served at station
        #customer leaves station
        my_print1(customer.name,self.name,'leaves')
        self.busy= False
        ev = Ev(EvQueue.time, work=customer.leave_station,prio=2)
        evQ.push(ev)
        
             




# class consists of
# statistics variables
# and methods as described in the problem description
class Customer():
    served = dict()
    dropped = dict()
    complete = 0
    duration = 0
    duration_cond_complete = 0
    count = 0
# please implement here
    #list1 = shopping list, t = arrival time
    def __init__(self, list1,name,t) :
        self.list = list(list1)
        self.name = name
        self.t = t
        Customer.count += 1

    #begin shopping
    def run(self,args):
        if len(self.list)> 0:
            # T= Zeit bis naechste station,, N = anzahl einkaeufe, W = maximale warteschlange
            T,station,N,W = self.list[0]
            ev = Ev(self.t+T,work=self.arrive_station,prio=3)
            evQ.push(ev)
            my_print1(self.name,'Supermarkt','begins')

    #arrive at station
    def arrive_station(self,args):
        # T= Zeit bis naechste station,, N = anzahl einkaeufe, W = maximale warteschlange
        T,station,N,W = self.list[0]
        my_print1(self.name,station.name,'arrives')
        Customer.duration += station.delay_per_item * N
        #check for enough space in queue
        if len(station.buffer)+1 <= W:
            Customer.duration_cond_complete+= station.delay_per_item *N
            ev = Ev(EvQueue.time,work=station.queue, args=self,prio=1)
            evQ.push(ev)
        #not enough space in queue
        else:
            Customer.dropped[station.name]+= 1 #customer left station without buying stuff
            my_print1(self.name,station.name,'dropped')



    def leave_station(self,args):
        #delete entry in einkaufsliste
        self.list.pop(0)
        if len(self.list)>0: #keep shopping?
            # T= Zeit bis naechste station,, N = anzahl einkaeufe, W = maximale warteschlange
            T,station,N,W = self.list[0]
            #start event at next station
            ev = Ev(EvQueue.time+T,work=self.arrive_station,prio=3)
            evQ.push(ev)
        else:
            Customer.complete += 1
            my_print1(self.name,'Supermarkt','leaves')
        
        
        


        


#st = startTime, mT= maxTime, dT= time till new customer
def startCustomers(einkaufsliste, name, sT, dT, mT):
    i = 1
    t = sT
    while t < mT:
        kunde = Customer(list(einkaufsliste), name + str(i), t)
        ev = Ev(t, kunde.run, prio=1)
        evQ.push(ev)
        i += 1
        t += dT
    


evQ = EvQueue()
baecker = Station(10, 'Bäcker')
metzger = Station(30, 'Metzger')
kaese = Station(60, 'Käse')
kasse = Station(5, 'Kasse')
Customer.served['Bäcker'] = 0
Customer.served['Metzger'] = 0
Customer.served['Käse'] = 0
Customer.served['Kasse'] = 0
Customer.dropped['Bäcker'] = 0
Customer.dropped['Metzger'] = 0
Customer.dropped['Käse'] = 0
Customer.dropped['Kasse'] = 0
einkaufsliste1 = [(10, baecker, 10, 10), (30, metzger, 5, 10), (45, kaese, 3, 5), (60, kasse, 30, 20)]
einkaufsliste2 = [(30, metzger, 2, 5), (30, kasse, 3, 20), (20, baecker, 3, 20)]
startCustomers(einkaufsliste1, 'A', 0, 200, 30 * 60 + 1)
startCustomers(einkaufsliste2, 'B', 1, 60, 30 * 60 + 1)
evQ.start()
my_print('Simulationsende: %is' % EvQueue.time)
my_print('Anzahl Kunden: %i' % (Customer.count
                                ))
my_print('Anzahl vollständige Einkäufe %i' % Customer.complete)
x = Customer.duration / Customer.count
my_print(str('Mittlere Einkaufsdauer %.2fs' % x))
x = Customer.duration_cond_complete / Customer.complete
my_print('Mittlere Einkaufsdauer (vollständig): %.2fs' % x)
S = ('Bäcker', 'Metzger', 'Käse', 'Kasse')
for s in S:
    x = Customer.dropped[s] / (Customer.served[s] + Customer.dropped[s]) * 100
    my_print('Drop percentage at %s: %.2f' % (s, x))

f.close()
fc.close()
fs.close()