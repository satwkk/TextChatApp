import socket
import pickle

from tkinter import *
from threading import Thread
from functools import partial
from message import Message
from utils import check_exit

HOST = 'localhost'
PORT = 9001

# DEBUG
USERNAME = str()
USERNAME = input('Enter username: ')

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
    message = user_input.get()
    msg = Message(USERNAME.encode('utf-8'), message.encode('utf-8'), None)
    msg_bytes = pickle.dumps(msg)
    client_socket.send(msg_bytes)
    user_input.delete(0, len(user_input.get()))
    if check_exit(msg):
        print('Closing connection to the server')
        cleanup(client_socket, exit(1))

def recieve_server_data(client_socket: socket.socket, msg_field: Text) -> None:
    while True:
        serialized_data = client_socket.recv(4096)
        if not serialized_data:
            break
        msg_obj = pickle.loads(serialized_data)
        msg_author, msg_content = msg_obj.author.decode('utf-8'), msg_obj.content.decode('utf-8')
        msg_field.insert(END, f'{msg_author} : {msg_content}' + '\n')
        msg_field.see(END)

def main():
    # GUI Stuff
    # TODO: Abstract it into separate files
    msg_field = Text(root, bg=BG_COLOR, fg=TEXT_COLOR, font=FONT, width=60)
    msg_field.grid(row=1, column=0, columnspan=2)
    scrollbar = Scrollbar(msg_field)
    scrollbar.place(relheight=1, relx=0.974)
    user_input_field = Entry(root, bg="#2C3E50", fg=TEXT_COLOR, font=FONT, width=55)
    user_input_field.grid(row=2, column=0)
    
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))
    
    # Receives data from the server
    Thread(target=recieve_server_data, args=(client_socket, msg_field)).start()
    
    # Sending the data when we click the button
    send_button = Button(root, text="Send", font=FONT_BOLD, bg=BG_GRAY, command=partial(send_client_data, client_socket, user_input_field))
    send_button.grid(row=2, column=1)
    
    # Binding the enter button to send_button
    root.bind('<Return>', lambda event: send_client_data(client_socket, user_input_field))
    
    # Main tkinter loop
    root.mainloop()

if __name__ == '__main__':
    main()
