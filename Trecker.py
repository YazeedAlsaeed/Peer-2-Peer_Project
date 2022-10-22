import socket
import threading

#Defines the varaibles
HEADER = 1024
PORT = 36500
ADDR = ("",PORT)
FORMAT = "utf-8"
cond = False

#Define the socket
server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind(ADDR)

#Recieve the message from user and response
def handle_client(conn,addr):
    connected = True
    cond = True
    obj = handle('1','2','3','4','5')

    while connected:
        msg = conn.recv(HEADER).decode(FORMAT)
        
        #To register new
        if not msg[0].isdigit() and cond:
            msgList = msg.split(":")
            obj = handle(msgList[0],msgList[1],msgList[2],msgList[3],msgList[4])
            message = register(obj)
            conn.send(message.encode(FORMAT))
            cond = False
        
        #To query handles
        elif msg[0] == "1":
            message = query_handles()
            conn.send(message.encode(FORMAT))

        #To follow other handles    
        elif msg[0] == "2":
            message = msg.split()
            if len(message) != 2:
                conn.send("out : Error".encode(FORMAT))
            else:
                handlesOfFollowing = find(message[1])
                if(not handlesOfFollowing):
                    conn.send(("out : Error: The user can not be found").encode(FORMAT))
                else:
                    follow(obj,handlesOfFollowing)
                    conn.send(("out : Followed Succecfully").encode(FORMAT)) 
        
        #To drop other handles    
        elif msg[0] == "3":
            message = msg.split()
            if len(message) != 2:
                conn.send("out : Error".encode(FORMAT))
            else:
                handlesOfDropped = find(message[1])
                if(not handlesOfDropped):
                    conn.send(("out : Error: The user can not be found").encode(FORMAT))
                else:
                    try:
                        drop(obj,handlesOfDropped)
                        conn.send(("out : Dropped Succecfully").encode(FORMAT))
                    except:
                        conn.send(("Error has occured").encode(FORMAT))
        #To tweet 
        elif msg[0] == "4":
            message = msg.split()
            if len(message) != 2:
                conn.send("out : Error 'Takes one argument only'".encode(FORMAT))
            else:
                conn.send(tweet(message[1]).encode(FORMAT))

         #To exit   
        elif msg[0] == "0":
            connected = False
            message = exit(obj)
            conn.send(message.encode(FORMAT))
    print("\nCONNECTION WITH " + obj.ipv4 + ":" + obj.port1 + " CLOSED")
    if len(handles) == 0:
        cond = True
    conn.close()
    


#Start the thread
def start():
    count = 1
    server.listen()
    print("Tracker is listening now ...")
    while True:
       conn, addr = server.accept()
       thread = threading.Thread(target=handle_client, args=(conn,addr))
       thread.start()
       print("ACTIVE CONNECTION THREAD NUMBER " + str(count))
       count += 1
        
       
#Class for each user
class handle():

    def __init__(self,handleName,ipv4,port1,port2,port3):

        self.handleName = handleName
        self.ipv4 = ipv4
        self.port1 = port1
        self.port2 = port2
        self.port3 = port3
        self.followers = []
        self.following = []
    
#Defines the handles list
handles = []

#Register the handle if unique
def register(object):
    for i in handles:
        if object.handleName == i.handleName:
            return "out : FAILURE"
    handles.append(object)
    return "out : SUCCESS"
            
#Return the number of handles with its content
def query_handles():
    listOfHandlesNames = [i.handleName for i in handles]
    return("out : " + str(len(handles)) + " , " + str(listOfHandlesNames))

#The ability for handle A to follow handle B
def follow(handleA,handleB):
    handleB.followers.append(handleA)

    #For exit function only
    handleA.following.append(handleB)

#The ability for handle A to unfollow handle B
def drop(handleA,handleB): 
    handleB.followers.remove(handleA)
    handleA.following.remove(handleB)

#The ability for a spesific handle to tweet 
def tweet(handle):
    for i in handles:
        if i.handleName == handle:
            return buildLogic(handle)
    return "FAILURE"

#TODO end-tweet

#Exit handle A from the proccess
def exit(handle):
    for i in handle.following:
        drop(handle,i)
    handles.remove(handle)
    return handle.handleName + "out : exit succeccfully"

#To read a string from user and find the corresponding object to it
def find(handleName):
    for i in handles:
        if handleName == i.handleName:
            return i
    return 0

#To build a logic ring table
def buildLogic(handle):
    followers = find(handle).followers
    table = ""
    for i in followers:
        table += " " + str(i.ipv4 + "," + i.port2 + "," + i.port3)
    return table

#Start the thread and proccess
start()
