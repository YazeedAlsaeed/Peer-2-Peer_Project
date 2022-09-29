import socket

class handle():
    def __init__(self,handleName,ipv4,port1,port2,port3):
        self.handleName = handleName
        self.ipv4 = ipv4
        self.port1 = port1
        self.port2 = port2
        self.port3 = port3
        slef.followers = []
    
#Form the handles dictionary
handles = []
#register the handle if unique
def register(handleName,ipv4,port1,port2,port3):
    for i in handles:
        if handleName == i.handleName:
            return "FAILURE"
    handleA = handle(handleName,ipv4,port1,port2,port3)
    handles.append(handleA)
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
    
    
    followers = handles[handleB][1]
    followers.append(handleA)
    followers.sort()
    ip = handles[handleB][0]
    handles[handleB] = (ip, followers)

#The ability for handle A to unfollow handle B
def drop(handleA,handleB): 
    followers = handles[handleB][1]
    followers.remove(handleA)
    followers.sort()
    ip = handles[handleB][0]
    handles[handleB] = (ip, followers)
def find(handleName):
    count=0
    for i in handles:
        if handleName == i.handleName:
            return count:
        count++
    return -1:

#Test
print(register("khalid","4","1","2","3"))
print(register("khalid2","4","1","2","3"))
#print(register("moh",4,4))
#register("zezo",4,4)
#register("moath",4,4)
#register("abrar",4,4)
print(query_handles())

#follow("salih","khalid")
#follow("moath","khalid")
#follow("abrar","khalid")
#follow("zezo","khalid")
#drop("zezo","khalid")
#print(handles["khalid"])
print(handles)
print(handles[0].handleName)
