from email import message
from http import server
import socket
import random
import sys
import threading

if len(sys.argv) != 3:
    print("out : The number of argument should be 2 'IP' and 'Port number'")
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


user.bind(("",int(PORT1)))
user_left.bind(("",int(PORT2)))
user_right.bind(("",int(PORT3)))
user.connect(ADDR)
handle = ""
condition = True

#Ask the tracker to register
def register(handle,ip,port1,port2,port3):
    while condition:
        handle = input("in : Enter Handle name to register: \n")
        message = handle+":"+ip+":"+port1+":"+port2+":"+port3
        message = (message).encode(FORMAT)
        user.send(message)
        msg = user.recv(HEADER).decode(FORMAT)
        if msg == "out : SUCCESS":
            print(msg)
            break
        else:
            print(msg)
            handle = input("\nin : Enter Handle name to register: \n")

def commands():
    
    
    while(True):
        inputForOption = input(f"in : \nEnter 1 for query handles\nEnter 2 for follow\nEnter 3 for drop\nEnter 4 to tweet\nEnter 0 to exit\n")
        if inputForOption == "1":
            message = (inputForOption).encode(FORMAT)
            user.send(message)
            msg = user.recv(HEADER).decode(FORMAT)
            print(msg)

        
        elif inputForOption == "2":
            inputForFollow = input(f"in : Enter the name of who you want to follow:\n")
            message = ("2"+" "+inputForFollow).encode(FORMAT)
            user.send(message)
            msg = user.recv(HEADER).decode(FORMAT)
            print(msg)


        elif inputForOption == "3":
            inputForUnFollow = input(f"in : Enter the name of who you want to unfollow:\n")
            message = ("3"+" "+inputForUnFollow).encode(FORMAT)
            user.send(message)
            msg = user.recv(HEADER).decode(FORMAT)
            print(msg)

        elif inputForOption == "4": 
            message = ("4"+" "+handle).encode(FORMAT)
            user.send(message)
            msg = user.recv(HEADER).decode(FORMAT)
            if msg == "FAILURE":
                print("out : FAILURE")
            else:
                message = msg.split()
                table = [(IP,PORT2,PORT3)]
                if len(table) != 0:
                    for i in message:
                        subMessage = i.split(',')
                        table.append((subMessage[0],subMessage[1],subMessage[2]))
                response = setUp(table)
                if response == "SUCCESS":
                    print("out : SUCCESS,\n")
                    while(True):
                        userInput = input("in : Enter your 140 char tweet to send : ")
                        if len(userInput > 140):
                            print("tweet should not be more than 140 char")
                        else: 
                            break
                    tweet(userInput)

        elif inputForOption == "0":
            message = (inputForOption).encode(FORMAT)
            user.send(message)
            msg = user.recv(HEADER).decode(FORMAT)
            print(msg)
            sys.exit()
        else:
            print("out : invalid input\n")

def setUp(table):
    #Send for each follower ip left ip right port
    conn, addr = user_right.accept()
    thread = threading.Thread(target=sendLeftRight(table), args=(conn,addr))
    thread.daemon
    thread.start()
    user_left.listen()
    while True:
       conn, addr = user_left.accept()
       thread = threading.Thread(args=(conn,addr))
       msg = conn.recv(HEADER).decode(FORMAT)
       thread.daemon
       thread.start()
    return "SUCCESS"

def listeningThread():
    user_left.listen()
    while True:
       conn, addr = user_left.accept()
       thread = threading.Thread(args=(conn,addr))
       msg = conn.recv(HEADER).decode(FORMAT)
       thread.daemon
       thread.start()

def startThread():
    thread = threading.Thread(target=commands)
    thread.start()

def waitForUser():
    msg = conn.recv(HEADER).decode(FORMAT)
    return "T"
def sendLeftRight(table):
    for i in range(1,len(table)):
        user_right.connect((table[i][0],table[i][1]))
        message = table[i-1][0]+":"+table[i-1][1]+":"+table[i+1][0]+":"+table[i+1][1]
        message = message.encode(FORMAT)
        user_right.send(message)
        print("Send")

def tweet(message):
    return "T"

register(handle,IP,PORT1,PORT2,PORT3)
startThread()
listeningThread()
