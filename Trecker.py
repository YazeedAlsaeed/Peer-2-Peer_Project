import socket
import random
import sys
import pickle

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

def commands():
    
    inputCorE = input("For command press C or E to exit\n")
    while(inputCorE.upper() != "E"):
        if(inputCorE.upper() == "C"):
            inputForOption = input(f"Enter 1 for query handles\nEnter 2 for follow\nEnter 3 for drop\n")
            if inputForOption == "1":
                message = (inputForOption).encode(FORMAT)
                user.send(message)
                print(message)
                
                pickle.loads(message)
            elif inputForOption == "2":
                inputForFollow = input(f"Enter the name of who you want to follow:")
                message = (inputForOption+" "+inputForFollow).encode(FORMAT)
                user.send(message)
            elif inputForOption == "3":
                inputForUnFollow = input(f"Enter the name of who you want to unfollow:")
                message = (inputForOption+" "+inputForUnFollow).encode(FORMAT)
                user.send(message)
            else:
                print("invalid input")
        else:
            print("Invalid input please choose C or E")
        inputCorE = input("For command press C or E to exit\n")


register(handle,IP,PORT1,PORT2,PORT3)
commands()
