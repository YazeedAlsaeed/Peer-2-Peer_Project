# Twitter Peer-2-Peer Project


# Description 
##### This project is a small application that works on the basis of the Peer-2-Peer protocol (no server needed). The application consists of handles (users). each handle (user) can have none or more followers. each handle (user) has the ability to tweet, then all his followers will receive the tweet through those followers (since it is Peer-2-Peer, the tweet will be passed between the followers in alphabetical order until it reaches all of them). all users will receive the tweet as long as they are still followeres. 

* The program do not have a Graphical User Interface

# How to Run
* The application consist of two python files, "User.py" and "Tracker.py". 
* To take full advantage of this application try to run these files on diffrent end host on the same subnet. 
* If two or more users have the same IP address, they will assigned different port numbers automatically.

##### 1 - You should run the Tracker file first.
##### 2 - You should run the User file on separate terminal. 
##### 3 - There are two arguments for User.py to run properly, 
* first argument: the IP address of the Tracker.
* second argument: the Port number of the Tracker. 
##### 5 - You can run as many User.py file as you wish, as long as you run each file on diffrent terminal (diffrent end host) on same subnet.
##### 4 - Finally, follow the instructions appear on the app menu! 
