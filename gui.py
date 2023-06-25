from tkinter import *

# GUI
root = Tk()
root.title("Chatbot")

BG_GRAY = "#ABB2B9"
BG_COLOR = "#17202A"
TEXT_COLOR = "#EAECEE"

FONT = "Helvetica 14"
FONT_BOLD = "Helvetica 13 bold"


def run():
    # Send function
    def send():
        send = "You -> " + user_input.get()
        txt.insert(END, "\n" + send)
        user = user_input.get().lower()
        user_input.delete(0, END)
 
    txt = Text(root, bg=BG_COLOR, fg=TEXT_COLOR, font=FONT, width=60)
    txt.grid(row=1, column=0, columnspan=2)

    scrollbar = Scrollbar(txt)
    scrollbar.place(relheight=1, relx=0.974)

    user_input = Entry(root, bg="#2C3E50", fg=TEXT_COLOR, font=FONT, width=55)
    user_input.grid(row=2, column=0)

    send = Button(root, text="Send", font=FONT_BOLD, bg=BG_GRAY,
                command=send).grid(row=2, column=1)

    root.mainloop()
