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

def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]

ADDR = (SERVER,PORT)
#IP = socket.gethostbyname(socket.gethostname())
IP = get_ip_address()
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

# the size of message recived
HEADER = 1024


user.bind(("",int(PORT1)))
user_left.bind(("",int(PORT2)))
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
    thread = threading.Thread(target=commands, args=(handle,))
    thread.start()
    startThread()

def commands(username):
    handle = username

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
            message = ("4" + " " + handle).encode(FORMAT)
            user.send(message)
            msg = user.recv(HEADER).decode(FORMAT)
            if msg == "FAILURE":
                print("out : FAILURE")
            else:
                message = msg.split()
                if len(message) == 0:
                    print("out : No Followers yet")
                else:
                    table = [(IP,PORT2,PORT3)]
                    for i in message:
                            subMessage = i.split(',')
                            table.append((subMessage[0],subMessage[1],subMessage[2]))
                    while(True):
                        userInput = input("in : Enter your 140 char tweet to send : ")
                        if len(userInput) > 140:
                            print("tweet should not be more than 140 char")
                        else:
                            userInput = userInput.replace(" ", "_")
                            tweet(table,userInput)
                            break

        elif inputForOption == "0":
            message = (inputForOption).encode(FORMAT)
            user.send(message)
            msg = user.recv(HEADER).decode(FORMAT)
            print(msg)
            sys.exit()
        else:
            print("out : invalid input\n")

def recive(conn):
  msg = conn.recv(HEADER).decode(FORMAT)
  msg = msg.split()
  table = msg[0]
  tweet = msg[1]
  position = int(msg[2])
  table = table.split(";")
  table.pop()
  n = len(table)
  adress = table[(position+1) % n].split(",")  
  if position == 0:
    print("You reached the end, Enter comand number to proceed")
    return()
  else:
    user_right = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    user_right.bind(("",int(PORT3)))
    print("recived with order '" + str(position) + "' : " + tweet.replace("_"," ") +"\n Enter command number to proceed")
    user_right.connect((adress[0] , int(adress[1])))
    message = (msg[0]+" "+tweet+" "+" "+ str((position+1) % n))
    user_right.send(message.encode(FORMAT))
    user_right.close()
    return()

def startThread():
    user_left.listen()
    print("User is listening now ...")
    while True:
       conn, addr = user_left.accept()
       thread = threading.Thread(target=recive, args=(conn,))
       thread.start()

def tweet(table,tweet):
    user_right = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    print("1")
    user_right.bind(("",int(PORT3)))
    print(table)
    user_right.connect((table[1][0],int(table[1][1])))
    
    stringTable = ""
    for i in table:
        stringTable += i[0]+","+i[1]+","+i[2]+";"
    message = (stringTable+" "+tweet+" "+" "+"1")
    print("3")
    user_right.send(message.encode(FORMAT))
    user_right.close()
    print("4")


register(handle,IP,PORT1,PORT2,PORT3)
