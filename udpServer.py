from socket import *
import threading
from datetime import datetime
import json

serverPort = 12100
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('localhost', serverPort))

now = datetime.now()
current_time = now.strftime("%H:%M:%S")

clients = {}
names = []

server_waiting = current_time+" Server waiting for Clients on port 12100"
print(server_waiting)
print("Thread trying to create Object Input/Output Streams")


def broadcast(message):
    for client in clients:
        serverSocket.sendto(message, clients[client])


def handle(client, *args):
    while True:
        try:
            message, address = serverSocket.recvfrom(2048)
            now = datetime.now()
            message_time = now.strftime("%H:%M:%S")
            plus_time_message = message_time + " " + str(message.decode())
            name = message.decode().split(":")[0]
            if name in clients:
                print(plus_time_message)
                broadcast(plus_time_message.encode('ascii'))
            else:
                broadcast(
                    f'{datetime.now().strftime("%H:%M:%S")} *** {name} has joined the chat ***'.encode('ascii'))
                print(
                    f'{datetime.now().strftime("%H:%M:%S")} *** {name} has joined the chat ***'.encode('ascii'))

        except:
            index = clients[client]
            clients.pop(client)
            serverSocket.close()
            name = names[index]
            broadcast(f'{name} left the chat'.encode('ascii'))
            names.remove(name)
            break


def receive():
    while True:
        now = datetime.now()
        time = now.strftime("%H:%M:%S")
        client, address = serverSocket.recvfrom(1024)
        name = client.decode('ascii')
        cleaned_name = name.split(":")[0]
        print(cleaned_name)

        if cleaned_name not in clients:
            names.append(cleaned_name)
            clients[cleaned_name] = address
            serverSocket.sendto('NICK'.encode('ascii'), address)
            print(
                f'{datetime.now().strftime("%H:%M:%S")} *** {cleaned_name} has joined the chat room ***')
            print(
                f'{datetime.now().strftime("%H:%M:%S")} Server waiting for Clients on port 55555')
            print("Thread trying to create Object Input/Output Streams")

            broadcast(
                f'{datetime.now().strftime("%H:%M:%S")} *** {name} has joined the chat ***'.encode('ascii'))
            serverSocket.sendto(
                'Connected to the server!'.encode('ascii'), address)

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


receive()
