import socket

SERVER_ADDR = '192.168.1.10'
SERVER_PORT = 10050 

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind((SERVER_ADDR, SERVER_PORT))

print('udpserver start')

while True:
    data,(addr, port) = server.recvfrom(1024)
    print(data,addr,port)

