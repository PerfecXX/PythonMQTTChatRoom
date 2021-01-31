from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import random as rd
import string
import paho.mqtt.client as mqtt

hostname = "test.mosquitto.org"
RoomName = "TNIRobot/"
ConnectionStatus = False
global DummyVar
DummyVar = "\n"
nickname = "FRANK"
port = 1883


def check_name(name):
    if not name:
        return FALSE
    else:
        return TRUE


def set_nickname(new_name):
    global nickname
    if check_name(new_name) == FALSE:
        messagebox.showerror("Error", "Invalid name")
        pass
    else:
        Msgbox = messagebox.askquestion("Confirm",
                                        "Are your sure to change your name from {} to {}".format(nickname, new_name))
        if Msgbox == 'yes':
            nickname = str(new_name)
            messagebox.showinfo("Name changed", "Your name has been changed to {}".format(nickname))
        else:
            pass


def user_setting():
    USWin = Toplevel()
    USWin.title("User Setting")
    USWin.wm_minsize(250, 50)
    USWin.resizable(0, 0)
    USWin.grab_set()
    USLabel = Label(USWin, text="Change name")
    USLabel.grid(row=0, column=0)
    global USEntry
    USEntry = Entry(USWin)
    USEntry.grid(row=0, column=1)
    USOKButt = Button(USWin, text="Apply", command=lambda: set_nickname(USEntry.get()))
    USOKButt.grid(row=1, column=1)


def on_connection(client, user_data, flag, rc):
    global conn_status  # global variable in this file
    status_decoder = {  # swtich case in python style using dictionary
        0: "Successfully Connected",
        1: "Connection refused: Incorrect Protocol Version",
        2: "Connection refused: Invalid Client Identifier",
        3: "Connection refused: Server Unavailable",
        4: "Connection refused: Bad Username/Password",
        5: "Connection refused: Not Authorized",
    }
    conn_text = ("System>>{} has connected to broker with status: \n\t{}.\n".format(client_id, status_decoder.get(rc)))
    ChatFill.configure(state="normal")
    ChatFill.insert(INSERT, str(conn_text))
    client.subscribe(RoomName)
    conn_status = True
    ChatFill.configure(state="disabled")


def on_message(client, user_data, msg):
    # check incoming payload to prevent owner echo text
    global incoming_massage
    incoming_massage = msg.payload.decode("utf-8")
    if incoming_massage.find(DummyVar) >= 0:
        pass
    else:
        ChatFill.configure(state="normal")
        ChatFill.insert(INSERT, str(incoming_massage))
        ChatFill.configure(state="disabled")


def send_message():
    global DummyVar
    get_message = str(MassageFill.get("1.0", END))
    if get_message == " ":
        pass
    else:
        send_message = "\n{}>>\t{}".format(nickname, get_message)
        DummyVar = send_message
        ChatFill.configure(state="normal")
        client.publish(RoomName, send_message)
        ChatFill.insert(INSERT, str(send_message))
        MassageFill.delete("1.0", END)
        ChatFill.configure(state="disabled")


window = Tk()
window.title("Chat room")
window.minsize(600, 400)
window.resizable(0, 0)

Frame1 = LabelFrame(window, text="Chat Window", width=600, height=300)
Frame1.place(y=0, x=0)
Frame2 = LabelFrame(window, text="Enter Massage", width=600, height=100)
Frame2.place(y=300, x=0)

YChatFillScroll = Scrollbar(Frame1)
YChatFillScroll.place(y=0, x=550, height=250)
XChatFillScroll = Scrollbar(Frame1, orient=HORIZONTAL)
XChatFillScroll.place(y=251, x=0, width=550)

ChatFill = Text(Frame1, yscrollcommand=YChatFillScroll.set, xscrollcommand=XChatFillScroll.set)
ChatFill.place(x=0, y=0, width=550, height=250)
ChatFill.configure(state="disabled")
YChatFillScroll.config(command=ChatFill.yview)
XChatFillScroll.config(command=ChatFill.xview)

MassageFill = Text(Frame2, font=("", 16))
MassageFill.place(x=0, y=0, width=475, height=75)

SendButton = Button(Frame2, text="Send", command=send_message)
SendButton.place(x=480, y=0, width=100, height=75)

WindowMenu = Menu(window)
FileMenuBar = Menu(WindowMenu, tearoff=0)
FileMenuBar.add_command(label="Disconnect Current Server", command=...)
FileMenuBar.add_command(label="New Connection", command=...)
FileMenuBar.add_separator()
FileMenuBar.add_command(label="Exit", command=...)
WindowMenu.add_cascade(label="File", menu=FileMenuBar)

SettingMenuBar = Menu(WindowMenu, tearoff=0)
SettingMenuBar.add_command(label="User Setting", command=user_setting)
SettingMenuBar.add_command(label="Connection Setting", command=...)
SettingMenuBar.add_command(label="Interface Setting", command=...)
WindowMenu.add_cascade(label="Setting", menu=SettingMenuBar)
window.config(menu=WindowMenu)

client_id = 'Client-' + ''.join(rd.choices(string.ascii_uppercase + string.digits, k=9))
client = mqtt.Client(client_id)

client.on_connect = on_connection
client.on_message = on_message

client.connect(hostname, port)
client.loop_start()
window.mainloop()
