from socket import *
import threading
import json

serverName = 'localhost'
serverPort = 12100
clientSocket = socket(AF_INET, SOCK_DGRAM)

name = input('Enter the username: ')

clientSocket.sendto(name.encode(),(serverName, serverPort))

print('Connection accepted to localhost')
print('Hello Welcome to the groupchat.')

def receive():
    while True:
        try:
            message = clientSocket.recv(2048).decode('ascii')
            if message == 'NICK':
                clientSocket.sendto(name.encode('ascii'),(serverName,serverPort))
            else:
                print(message)

        except:
            print('An error occurred!')
            clientSocket.close()
            break

def write():
    while True:
        message = f'{name}: {input("")}'
        clientSocket.sendto(message.encode('ascii'),(serverName,serverPort))

receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()