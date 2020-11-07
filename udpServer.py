from socket import *
import threading
from datetime import datetime
import json

serverPort = 12100
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('localhost', serverPort))

now = datetime.now()
current_time = now.strftime("%H:%M:%S")

clients=[]
names=[]

server_waiting=current_time+" Server waiting for Clients on port 12100"
print(server_waiting)
print("Thread trying to create Object Input/Output Streams")

def broadcast(message):
    for client in clients:
        client.sendto(message,names)

def handle(client):
    while True:
        try:
            message = client.recv(2048)
            now = datetime.now()
            message_time = now.strftime("%H:%M:%S")
            print(f'{message_time}: {str(message)}')
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            name = names[index]
            broadcast(f'{name} left the chat'.encode('ascii'))
            names.remove(name)
            break

def receive():
    while True:
        now = datetime.now()
        time= now.strftime("%H:%M:%S")
        client, address = serverSocket.recvfrom(1024)

        client.sendto('NICK'.encode('ascii'),address)
        name = client.decode('ascii')
        names.append(name)
        clients.append(client)

        print(f'{time} *** {name} has joined the chat room ***')
        print(f'{time} Server waiting for Clients on port 55555')
        print("Thread trying to create Object Input/Output Streams")

        broadcast(f'{time} *** {name} has joined the chat ***'.encode('ascii'))
        client.sendto('Connected to the server!'.encode('ascii'),address)

        thread = threading.Thread(target=handle, args = (client,))
        thread.start()


receive()
