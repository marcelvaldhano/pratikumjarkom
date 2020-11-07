from socket import *
import threading
import json

serverName = 'localhost'
serverPort = 12100
clientSocket = socket(AF_INET, SOCK_DGRAM)

name = input('Enter the username: ')
user_has_been_created = False
if not user_has_been_created:
    clientSocket.sendto(name.encode(), (serverName, serverPort))
    user_has_been_created = True

print('Connection accepted to localhost')
print('Hello Welcome to the groupchat.')


def receive():
    while True:
        try:
            message = clientSocket.recv(2048).decode('ascii')
            if message == 'NICK':
                clientSocket.sendto(name.encode('ascii'),
                                    (serverName, serverPort))
            else:
                print(message)

        except:
            print('An error occurred!')
            clientSocket.close()
            break


def write():
    while True:
        if user_has_been_created:
            msg_string = input(name + " => ")
            message = f'{name}: {msg_string}'
            clientSocket.sendto(message.encode('ascii'),
                                (serverName, serverPort))


receive_thread = threading.Thread(target=receive)
receive_thread.start()

if user_has_been_created:
    write_thread = threading.Thread(target=write)
    write_thread.start()
