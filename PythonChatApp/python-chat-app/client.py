import socket
import threading

import tkinter
from tkinter import simpledialog, scrolledtext
import traceback

#Creadit to "Simple GUI Chat in Python" by NeuralNine on youtube

class Client():
    def __init__(self, server, port) -> None:

        self.FORMAT = 'utf-8'

        self.DISCONNECT_MESSAGE = "!disconnect"
        #If users do not propperly disconnect by sending this message, the server may keep their connection ope, then they can't reconnect
        self.SET_NICKNAME_MESSAGE = "!nick"

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #SOCK_STREAM is TCP
        self.sock.connect((server, port))

        msg = tkinter.Tk()
        msg.withdraw()

        self.nickname = simpledialog.askstring("Nickname", "Please choose a nickname", parent=msg)

        self.gui_done = False
        self._running = True

        gui_thread = threading.Thread(target=self.gui_loop)
        recieve_thread = threading.Thread(target=self.recieve)

        gui_thread.start()
        recieve_thread.start()

    def gui_loop(self):
        self.window = tkinter.Tk()
        self.window.configure(bg="lightgray")

        self._chat_label = tkinter.Label(self.window, text="Chat", bg="lightgray")
        self._chat_label.pack()

        self._text_area = scrolledtext.ScrolledText(self.window)
        self._text_area.pack()
        self._text_area.config(state='disabled')
        #Need to set the state to 'default' when making changes.

        self._message_label = tkinter.Label(self.window, text="Message:", bg="lightgray")
        self._message_label.pack()

        self._input_area = tkinter.Text(self.window, height=3)
        self._input_area.pack()

        self._send_button = tkinter.Button(self.window, text="send", command=self.write)
        self._send_button.pack()

        self.gui_done = True

        self.window.protocol("WM_DELETE_WINDOW", self.stop)

        self.window.mainloop()

    def recieve(self):
        while self._running:
            try:
                message = self.sock.recv(1024).decode(self.FORMAT)
                print(message)
                #TODO a debug thing

                
                if message == self.SET_NICKNAME_MESSAGE:
                    #GET AND SEND NICKNAME
                    self.sock.send(self.nickname.encode(self.FORMAT))
                elif self.gui_done:
                    self._text_area.config(state='normal')
                    #Allow changing the text
                    self._text_area.insert('end', message)
                    #Add recieved messages to the end
                    self._text_area.yview('end')
                    #scroll to the end
                    self._text_area.config(state='disabled')

            except ConnectionAbortedError:
                break
            except:
                traceback.print_exc()
                self.sock.close()
                break

    def write(self):

        message = self._input_area.get('1.0', 'end') + "\n"
        self.sock.send(message.encode(self.FORMAT))
        self._input_area.delete("1.0", "end")

        if message == self.DISCONNECT_MESSAGE:
            self.stop()

    def stop(self):
        self._running = False
        self.window.destroy()
        self.sock.close()
        exit(0)

SERVER = "172.28.210.193"
PORT = 5050

new_client = Client(SERVER, PORT)