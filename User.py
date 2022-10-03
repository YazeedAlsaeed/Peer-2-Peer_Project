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

# the size of message recived
HEADER = 1024


user.bind((IP,int(PORT1)))
user_left.bind((IP,int(PORT2)))
user_right.bind((IP,int(PORT3)))
user.connect(ADDR)
conn, addr = user.accept()

#Ask the tracker to register
def register(ip,port1,port2,port3):
    while True:
        handle = input("Enter Handle name to register: ")
        message = handle+":"+ip+":"+port1+":"+port2+":"+port3
        message = (message).encode(FORMAT)
        user.send(message)
        msg = conn.recv(HEADER).decode(FORMAT)
        if msg == "SUCCESS":
            print(msg)
            break
        else:
            print(msg)
    

def commands():
    
    
    while(True):

        inputForOption = input(f"Enter 1 for query handles\nEnter 2 for follow\nEnter 3 for drop\nEnter -1 to exit")
        if inputForOption == "1":
            message = (inputForOption).encode(FORMAT)
            user.send(message)
            msg = conn.recv(HEADER).decode(FORMAT)
            print(msg)

        
        elif inputForOption == "2":
            inputForFollow = input(f"Enter the name of who you want to follow:")
            message = (inputForOption+" "+inputForFollow).encode(FORMAT)
            user.send(message)
            msg = conn.recv(HEADER).decode(FORMAT)
            print(msg)


        elif inputForOption == "3":
            inputForUnFollow = input(f"Enter the name of who you want to unfollow:")
            message = (inputForOption+" "+inputForUnFollow).encode(FORMAT)
            user.send(message)
            msg = conn.recv(HEADER).decode(FORMAT)
            print(msg)

        elif inputForOption == "-1":
            message = (inputForOption).encode(FORMAT)
            user.send(message)
            sys.exit()
        else:
            print("invalid input")



register(IP,PORT1,PORT2,PORT3)

commands()

msg = conn.recv(HEADER).decode(FORMAT)

