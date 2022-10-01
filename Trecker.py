import random
import socket
import threading

HEADER = 1024
SERVER = socket.gethostbyname(socket.gethostname())
PORT = 36500
ADDR = (SERVER,PORT)
FORMAT = "utf-8"

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind(ADDR)


def handle_client(conn,addr):
    connected = True

    while connected:
        msg = conn.recv(HEADER).decode(FORMAT)
        if msg:
            obj = handle(msg,"192,192,192,192","1","2","3")
            message = register(obj)
            print(f"{addr} , {msg}")
            print(message)
        if msg == "!":
            connected = False
    print("Closed")
    conn.close()


def start():
    count = 1
    server.listen()
    print("server is listening")
    while True:
       conn, addr = server.accept()
       thread = threading.Thread(target=handle_client, args=(conn,addr))
       thread.start()
       print(f"ACTIVE CONNECTION {count}")
       count += 1 
       

#TODO Check Again!
range1 = 36501
range2 = 37000
rangeDict = {}

while(range1 < range2):
    rangeDict[range1] = True
    range1 += 1

class handle():
    def __init__(self,handleName,ipv4,port1,port2,port3):

        self.handleName = handleName
        self.ipv4 = ipv4
        self.port1 = port1
        self.port2 = port2
        self.port3 = port3
        self.followers = []
    
#Form the handles list
handles = []

#register the handle if unique
def register(object):
    for i in handles:
        if object.handleName == i.handleName:
            return "FAILURE"
    handles.append(object)
    handles.sort()
    return "SUCCESS"
            
#Return the number of handles with its content
def query_handles():
    listOfHandlesNames = [i.handleName for i in handles]
    return(len(handles),listOfHandlesNames)

#The ability for handle A to follow handle B
def follow(handleA,handleB):
    indexOfHandleB = find(handleB)
    handles[indexOfHandleB].followers.append(handleA)
    handles[indexOfHandleB].followers.sort()

#The ability for handle A to unfollow handle B
def drop(handleA,handleB): 
    indexOfHandleB = find(handleB)
    handles[indexOfHandleB].followers.remove(handleA)
    handles[indexOfHandleB].followers.sort()

#Function to find the index of handle in the list    
def find(handleName):
    count=0
    for i in handles:
        if handleName == i.handleName:
            return count
        count = count+1
    return -1

#Choose from allowed port number randomly.
def randomPort():

    condition = True
    while condition:
        portRandom = random.randint(0, 499)
        port = list(rangeDict.keys())[portRandom]
        if rangeDict[port]:
            condition = False
            return port


start()
