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
    handle_condiditon = False
    while connected:
        msg = conn.recv(HEADER).decode(FORMAT)
        print(msg)
        msg_split = msg.split()
        if msg and not(handle_condiditon):
            msgList = msg.split(":")
            obj = handle(msgList[0],msgList[1],msgList[2],msgList[3],msgList[4])
            message = register(obj)
            print(f"{addr} , {msgList}")
            print(message)
            handle_condiditon = True
        elif msg[0] == "1":
            print(query_handles())
            msg = pickle.dumps(query_handles())
            print(msg)
            user = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            user.bind(msgList[0],msgList[1])
            user.send(msg)
        elif msg[0] == "2":
            indexOfFollowing = find(msg[1])
            if(indexOfFollowing == -1):
                print("The user can not be found")
            else:
                follow(msgList[0],handles[indexOfFollowing])
        elif msg[0] == "3":
            indexOfFollowing = find(msg[1])
            if(indexOfFollowing == -1):
                print("The user can not be found")
            else:
                drop(msgList[0],handles[indexOfFollowing])  
        if msg == "!":
            connected = False
    print("Closed")
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
       count += 1
       cond = True
    
#For UI menu propose   
    #    while cond:
    #         print('Enter "C" to go to commands or "L" to liseten to other users')
    #         count += 1

    #         condition_follow = False
    #         condition_drop = False
    #         condition_exit = False

    #         for line in sys.stdin:
    #                 if 'C' == line.rstrip().upper():
    #                     print("Choose one of the following :\n")
    #                     print("Enter 1 for query handles\n")
    #                     print("Enter 2 for follow\n")
    #                     print("Enter 3 for drop\n")
    #                     print("Enter 4 to exit\n")
    #                 elif 'L' == line.rstrip().upper():
    #                     cond = False
    #                     break
    #                 elif '1' == line.rstrip():
    #                     print(query_handles())
    #                     break

    #                 elif condition_follow or ('2' == line.rstrip()):
    #                     if condition_follow:
    #                         condition_follow = False
    #                         words = line.split()
    #                         handle_1 = find(words[0])
    #                         handle_2 = find(words[1])
    #                         if handle_1 and handle_2:
    #                             follow(handle_1,handle_2)
    #                             print("Followed Succecfully")
    #                             break
    #                         else:
    #                             print("Failed!")
    #                             break
    #                     else :
    #                         print("Enter the two handles :\n")
    #                         condition_follow = True
    #                 elif condition_drop or ('3' == line.rstrip()):
    #                     if condition_drop:
    #                         condition_drop = False
    #                         words = line.split()
    #                         handle_1 = find(words[0])
    #                         handle_2 = find(words[1])
    #                         if handle_1 and handle_2:
    #                             drop(handle_1,handle_2)
    #                             print("Dropped Succecfully")
    #                             break
    #                         else:
    #                             print("Failed!")
    #                             break
    #                     else :
    #                         print("Enter the two handles :\n")
    #                         condition_drop = True
    #                 elif condition_exit or '4' == line.rstrip():
    #                     if condition_exit:
    #                         condition_exit = False
    #                         word = line.rstrip()
    #                         handle = find(word)
    #                         if handle:
    #                             exit(handle)
    #                             print("Exit Succecfully")
    #                             if len(handles) == 0:
    #                                 print("Since it's last handle the program has terminated.")
    #                                 sys.exit()
    #                             break
    #                         else:
    #                             print("Failed!")
    #                             break
    #                     else :
    #                         print("Enter handle \n")
    #                         condition_exit = True
    #                 else :
    #                     print('wrong input')
    #                     break 
        
       
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

#Exit handle A from the proccess
def exit(handle):
    for i in handle.following:
        drop(handle,i)
    handles.remove(handle)

#To read a string from user and find the corresponding object to it
def find(handleName):
    for i in handles:
        if handleName == i.handleName:
            return i
    return 0


#Start the thread and proccess
start()
