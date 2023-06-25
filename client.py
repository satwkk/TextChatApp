import socket
import pickle

from tkinter import *
from threading import Thread
from functools import partial
from message import Message

HOST = 'localhost'
PORT = 9001

# DEBUG
USERNAME = str()

def check_exit(message: Message) -> bool:
    ''' Checks if the message sent by user is an exit message '''
    return message.content.decode('utf-8').lower() == 'exit'

def show_message():
    txt.insert(user_input.get())

# UI STUFF
root = Tk()
root.title("Chatbot")

BG_GRAY = "#ABB2B9"
BG_COLOR = "#17202A"
TEXT_COLOR = "#EAECEE"
FONT = "Helvetica 14"
FONT_BOLD = "Helvetica 13 bold"


def cleanup(*args):
    for arg in args:
        if arg is socket.socket:
            arg.close()
        if arg is callable:
            arg()
    
def send_client_data(client_socket: socket.socket, user_input: Entry) -> None:
    # message = input('> ')
    message = user_input.get()
    msg = Message(USERNAME.encode('utf-8'), message.encode('utf-8'), None)
    msg_bytes = pickle.dumps(msg)
    client_socket.send(msg_bytes)
    if check_exit(msg):
        print('Closing connection to the server')
        cleanup(client_socket, exit(1))

def recieve_server_data(client_socket: socket.socket, txt: Text) -> None:
    while True:
        serialized_data = client_socket.recv(4096)
        if not serialized_data:
            break
        msg_obj = pickle.loads(serialized_data)
        txt.insert(END, '\n', msg_obj.content.decode('utf-8'))
        print(f'\n{USERNAME}: {msg_obj.content.decode("utf-8")}')

def main():

    # GUI Stuff
    txt = Text(root, bg=BG_COLOR, fg=TEXT_COLOR, font=FONT, width=60)
    txt.grid(row=1, column=0, columnspan=2)
    scrollbar = Scrollbar(txt)
    scrollbar.place(relheight=1, relx=0.974)
    user_input = Entry(root, bg="#2C3E50", fg=TEXT_COLOR, font=FONT, width=55)
    user_input.grid(row=2, column=0)
    # send_button = Button(root, text="Send", font=FONT_BOLD, bg=BG_GRAY, command=send_message).grid(row=2, column=1)

    #USERNAME = input("Enter your name: ")
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))
    Thread(target=recieve_server_data, args=(client_socket, txt)).start()
    send_button = Button(root, text="Send", font=FONT_BOLD, bg=BG_GRAY, command=partial(send_client_data, client_socket, user_input)).grid(row=2, column=1)

    # Thread(target=send_client_data, args=(client_socket,)).start()
    root.mainloop()

if __name__ == '__main__':
    main()
