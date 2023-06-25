import socket
import pickle

from threading import Thread
#from utils import check_exit
from message import Message

HOST = 'localhost'
PORT = 9001
BUFSIZE = 4096

def check_exit(message: Message) -> bool:
    ''' Checks if the message sent by user is an exit message '''
    return message.content.decode('utf-8').lower() == 'exit'

clients = list()

def recv_client_data(client_socket: socket.socket) -> object:
    serialized_data = client_socket.recv(BUFSIZE)
    data = pickle.loads(serialized_data)
    return data

def broadcast_message(client_socket: socket.socket, serialized_data) -> None:
    for client in clients:
        if client is not None and client_socket is not client:
            client.send(serialized_data)

def handle_client(client_socket: socket.socket) -> None:
    while True:
        '''
        msg = recv_client_data(client_socket)
        '''
        serialized_data = client_socket.recv(BUFSIZE)
        msg = pickle.loads(serialized_data)
        if check_exit(msg):
            print('Bye Bye {}'.format(msg.author.decode('utf-8')))
            client_socket.close()
            clients.remove(client_socket)
            return
        broadcast_message(client_socket, serialized_data)
        print('{}: {}'.format(msg.author.decode('utf8'), msg.content.decode('utf-8')))

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    while True:
        print('Listening at {} on port {}'.format(HOST, PORT))
        server_socket.listen()
        client_socket, client_addr = server_socket.accept()
        print('Client connected: {}'.format(client_socket.getsockname()))
        clients.append(client_socket)
        Thread(target=handle_client, args=(client_socket,)).start()
    
if __name__ == '__main__':
    main()
