
class Sender:

    def keepSendingWindowFull():
        while len(sentPackageQueue) != 5:
            # Start one SenderGlobalThread + one Thread per each transfer?
            GoBackN.addPackageToQueue(allPackages[lastAckNum])
