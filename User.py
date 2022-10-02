import socket
import random
import sys

if len(sys.argv) != 3:
    print("The number of argument should be 2 'IP' and 'Port number'")
    exit()

#Defines the varaibles
SERVER = sys.argv[1]
PORT = int(sys.argv[2])
for line in sys.stdin:
    handle = line.rstrip()
    break

ADDR = (SERVER,PORT)
IP = socket.gethostbyname(socket.gethostname())
FORMAT = "utf-8"


#List of allowed port numbers
range1 = 36501
range2 = 37000
rangeDict = {}
while(range1 < range2):
    rangeDict[range1] = True
    range1 += 1
def randomPort():
    condition = True
    while condition:
        portRandom = random.randint(0, 499)
        port = list(rangeDict.keys())[portRandom]
        if rangeDict[port]:
            rangeDict[port] = False
            return str(port)


#Define distinct 3 ports number
PORT1 = randomPort()
PORT2 = randomPort()
PORT3 = randomPort()

#Define the sockets
user = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
user_left = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
user_right = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

user.bind((IP,int(PORT1)))
user_left.bind((IP,int(PORT2)))
user_right.bind((IP,int(PORT3)))
user.connect(ADDR)

#Ask the tracker to register
def register(handle,ip,port1,port2,port3):
    message = handle+":"+ip+":"+port1+":"+port2+":"+port3
    message = (message).encode(FORMAT)
    user.send(message)


register(handle,IP,PORT1,PORT2,PORT3)


