import socket

#Form the handles dictionary
handles = {"":("",[""])}

#register the handle if unique
def register(handle,ipv4,port):
    
    for i in handles.keys():
        if handle == i:
            return("FAILURE")
        else : 
            handles[handle] = (ipv4+":"+port,[])
            return("SUCCESS")

#Return the number of handles with its content
def query_handles():
    handles.pop("")
    return(len(handles),list(handles.keys()))

#The ability for handle A to follow handle B
def follow(handleA,handleB):
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


#Test
print(register("khalid","4","4"))
#print(register("moh",4,4))
#register("zezo",4,4)
#register("moath",4,4)
#register("abrar",4,4)
print(query_handles())

follow("salih","khalid")
follow("moath","khalid")
follow("abrar","khalid")
follow("zezo","khalid")
drop("zezo","khalid")

print(handles["khalid"])
