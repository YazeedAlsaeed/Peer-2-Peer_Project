import socket


SERVER = "10.157.83.97"
PORT = 36500
handle = "Mosaab"
ADDR = (SERVER,PORT)
IP = socket.gethostbyname(socket.gethostname())
FORMAT = "utf-8"

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect(ADDR)

def register(handle):
    message = handle.encode(FORMAT)
    client.send(message)

register(handle)

