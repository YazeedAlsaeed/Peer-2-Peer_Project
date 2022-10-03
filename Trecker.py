import socket
import threading
import sys
import pickle


#Defines the varaibles
HEADER = 1024
SERVER = socket.gethostbyname(socket.gethostname())
PORT = 36500
ADDR = (SERVER,PORT)
FORMAT = "utf-8"

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
                conn.send("Error".encode(FORMAT))
            else:
                handlesOfFollowing = find(message[1])
                if(not handlesOfFollowing):
                    conn.send(("Error: The user can not be found").encode(FORMAT))
                else:
                    follow(obj,handlesOfFollowing)
                    conn.send(("Followed Succecfully").encode(FORMAT)) 
        
        #To drop other handles    
        elif msg[0] == "3":
            message = msg.split()
            if len(message) != 2:
                conn.send("Error".encode(FORMAT))
            else:
                handlesOfDropped = find(message[1])
                if(not handlesOfDropped):
                    conn.send(("Error: The user can not be found").encode(FORMAT))
                else:
                    try:
                        drop(obj,handlesOfDropped)
                        conn.send(("Dropped Succecfully").encode(FORMAT))
                    except:
                        conn.send(("Error has occured").encode(FORMAT))
             
         #To exit   
        elif msg[0] == "0":
            connected = False
            message = exit(obj)
            conn.send(message.encode(FORMAT))
    print("\nCONNECTION WITH " + obj.ipv4 + ":" + obj.port1 + " CLOSED")
    conn.close()
    


#Start the thread
def start():
    count = 1
    server.listen()
    print("Server " + SERVER + " is listening now ...")
    while True:
       conn, addr = server.accept()
       thread = threading.Thread(target=handle_client, args=(conn,addr))
       thread.start()
       print("ACTIVE CONNECTION THREAD NUMBER " + str(count))
       if len(handles) == 0:
        print("Since there is no connection, The program has terminated :)")
        sys.exit()
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
            return "FAILURE"
    handles.append(object)
    return "SUCCESS"
            
#Return the number of handles with its content
def query_handles():
    listOfHandlesNames = [i.handleName for i in handles]
    return(str(len(handles)) + " , " + str(listOfHandlesNames))

#The ability for handle A to follow handle B
def follow(handleA,handleB):
    handleB.followers.append(handleA)
    handleB.followers.sort()

    #For exit function only
    handleA.following.append(handleB)

#The ability for handle A to unfollow handle B
def drop(handleA,handleB): 
    handleB.followers.remove(handleA)
    handleA.following.remove(handleB)

#Exit handle A from the proccess
def exit(handle):
    for i in handle.following:
        drop(handle,i)
    handles.remove(handle)
    return handle.handleName + " exit succeccfully"

#To read a string from user and find the corresponding object to it
def find(handleName):
    for i in handles:
        if handleName == i.handleName:
            return i
    return 0


#Start the thread and proccess
start()
