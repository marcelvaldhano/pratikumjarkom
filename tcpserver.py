import threading
from socket import *
from datetime import *

host = '127.0.0.1'
port = 55555

server = socket(AF_INET, SOCK_STREAM)
server.bind((host, port))
server.listen(1)

clients = []
nicknames = []

now = datetime.now()
current_time = now.strftime("%H:%M:%S")

server_waiting=current_time+" Server waiting for Clients on port 55555"
print(server_waiting)
print("Thread trying to create Object Input/Output Streams")

def broadcast(message):
    for client in clients:
        client.send(message)

def handle(client):
    while True:
        try:
            message = client.recv(1024)
            now = datetime.now()
            message_time = now.strftime("%H:%M:%S")
            plus_time_message = message_time + " " + str(message.decode())
            print(plus_time_message)
            broadcast(plus_time_message.encode('ascii'))
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f'{nickname} left the chat'.encode('ascii'))
            nicknames.remove(nickname)
            break

def receive():
    while True:
        now = datetime.now()
        time= now.strftime("%H:%M:%S")
        client, address = server.accept()

        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)

        print(f'{datetime.now().strftime("%H:%M:%S")} *** {nickname} has joined the chat room ***')
        print(f'{datetime.now().strftime("%H:%M:%S")} Server waiting for Clients on port 55555')
        print("Thread trying to create Object Input/Output Streams")

        broadcast(f'{datetime.now().strftime("%H:%M:%S")} *** {nickname} has joined the chat ***'.encode('ascii'))
        client.send('Connected to the server!'.encode('ascii'))

        thread = threading.Thread(target=handle, args = (client,))
        thread.start()


receive()
