fullContent = ""


class Receiver:

    def printFull():
        print("Final Message Transfer: %s", fullContent)

    def recv(msg: bytes):
        fullContent += msg
