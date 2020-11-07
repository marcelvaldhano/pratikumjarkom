from socket import *
import threading
from datetime import datetime
import json

serverPort = 12100
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('localhost', serverPort))

now = datetime.now()
current_time = now.strftime("%H:%M:%S")

clients={}
names=[]

server_waiting=current_time+" Server waiting for Clients on port 12100"
print(server_waiting)
print("Thread trying to create Object Input/Output Streams")

def broadcast(message):
    for client in clients:
        serverSocket.sendto(message, clients[client])

def handle(client):
    while True:
        try:
            message, address = serverSocket.recvfrom(2048)
            now = datetime.now()
            message_time = now.strftime("%H:%M:%S")
            plus_time_message = message_time + " " + str(message.decode())
            print(plus_time_message)
            broadcast(plus_time_message.encode('ascii'))
        except:
            index = clients[client]
            clients.remove(client)
            serverSocket.close()
            name = names[index]
            broadcast(f'{name} left the chat'.encode('ascii'))
            names.remove(name)
            break

def receive():
    while True:
        now = datetime.now()
        time= now.strftime("%H:%M:%S")
        client, address = serverSocket.recvfrom(1024)
        print(address) #test debug

        client.decode()
        serverSocket.sendto('NICK'.encode('ascii'),address)
        name = client.decode('ascii')
        names.append(name)
        clients[client] = address
        print(clients) #test debug

        print(f'{datetime.now().strftime("%H:%M:%S")} *** {name} has joined the chat room ***')
        print(f'{datetime.now().strftime("%H:%M:%S")} Server waiting for Clients on port 55555')
        print("Thread trying to create Object Input/Output Streams")

        broadcast(f'{datetime.now().strftime("%H:%M:%S")} *** {name} has joined the chat ***'.encode('ascii'))
        serverSocket.sendto('Connected to the server!'.encode('ascii'),address)

        thread = threading.Thread(target=handle, args = (client,))
        thread.start()


receive()

# while 1:
#     name, clientAddress = serverSocket.recvfrom(2048)
#     client_addres.append(clientAddress)
#     names.append(name)
 
#     now = datetime.now()
#     current_time = now.strftime("%H:%M:%S")
#     joined=current_time+" *** "+name.decode()+" has joined the chat room ***"
#     server_waiting1=current_time+" Server waiting for Clients on port 12100"

#     print(joined)
#     print(server_waiting1)
#     print("Thread trying to create Object Input/Output Streams")
    
#     for x in range (0,len(client_addres)-1):
#         serverSocket.sendto(joined.encode(),client_addres[x])


    # print('Message from client',name)
    # print('Message answer for client',joining)
    # serverSocket.sendto(joining.encode(), clientAddress)
