# Twitter Peer-2-Peer Project


# Description 
##### This project is a small application that works on the basis of the Peer-2-Peer protocol (no server needed). The application consists of handles (users). Each handle (user) can have none or more followers. Each handle (user) has the ability to tweet, then all his followers will receive the tweet through those followers (since it is Peer-2-Peer, the tweet will be passed between the followers in alphabetical order until it reaches all of them). All users will receive the tweet as long as they are still followeres. No fancy UI is provided

# How to Run
* The application consist of two python files, "User.py" and "Tracker.py". 
* To take full advantage of this application try to run these files on diffrent end host on the same subnet. 
* If two or more users have the same IP address, they will assigned different port numbers automatically.

##### 1 - You should run the Tracker file first.
##### 2 - You should run the User file on separate mechine or terminal. 
##### 3 - There are two arguments for User.py to run properly, 
* First argument: The IP address of the Tracker.
* Second argument: The Port number of the Tracker. 
##### 5 - You can run as many User.py file as you wish, as long as you run each file on diffrent mechine or terminal (diffrent end host) on same subnet.
##### 4 - Finally, follow the instructions appear on the app menu! 
