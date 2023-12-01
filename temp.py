from socket import *

sock = socket(AF_INET,SOCK_STREAM)
sock.connect(('127.0.0.1',23000))


while True:
    
    print(sock.recv(1024).decode())