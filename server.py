import socket
import threading
from pywinauto import *
from pywinauto.keyboard import *
from PIL import ImageTk, Image
from mss import mss
import os
import wmi
import signal
import keyboard  # using module keyboard
import tkinter
from tkinter import *
import concurrent.futures
import winreg
import win32gui
import win32con

# import time
# import os
# import pyperclip

HEADER = 64
PORT = 2050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECTED"
MESSAGE_CMH = "CHUPMANHINH"
MESSAGE_PR = "PROCESSRUNNING"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def send(conn, message):
    # print("Start sending:  " + message)
    # message = message.encode(FORMAT)
    mes_lenth = str(len(message)).encode(FORMAT)
    mes_lenth += b' ' * (HEADER - len(mes_lenth))
    conn.send(mes_lenth)
    conn.send(message)


def send_process(conn, message):
    mes_lenth = str(len(message)).encode(FORMAT)
    mes_lenth += b' ' * (HEADER - len(mes_lenth))
    conn.send(mes_lenth)
    conn.send(message.encode(FORMAT))


# ----------image
def auto_screenshot():
    with mss() as sct:
        sct.shot(mon=-1, output='sth1.png')


def handle_image(conn):
    auto_screenshot()
    file = open('sth1.png', 'rb')
    os.stat('sth1.png')
    msg_leng = os.stat('sth1.png').st_size
    image = file.read(msg_leng)
    send(conn, image)
    '''
    while image:
        conn.send(image)
        image = file.read(2048)
        if not str(image):
            break
    '''


# -------process running
def check(list, process):
    for line in list:
        if line[1] == process.Name:
            line[2] += 1
            return True

    return False


def find_process():
    # Initializing the wmi constructor
    f = wmi.WMI()

    # Printing the header for the later columns
    print("pid   Process name")

    # Iterating through all the running processes

    list = []
    for process in f.Win32_Process():
        if check(list, process) == False:
            list.append([process.ProcessId, process.Name, 1])
    return list


def handle_process(conn):
    list_data = find_process()
    for line in list_data:
        msg_send = str(line[0]) + "|" + str(line[1]) + "|" + str(line[2])
        send_process(conn, msg_send)

    send_process(conn, "DONE")


def handle_kill(str_mes):
    try:
        os.kill(int(str_mes), signal.SIGTERM)
        return True
    except:
        return False


def handle_start(str_mes):
    try:

        app = Application().start(str_mes)
        f = wmi.WMI()
        print(str_mes)
        for process in f.Win32_Process():

            if str(process.Name) == str(str_mes):
                print("RESULT")
                listda = []
                listda.append(([process.ProcessId, process.Name, 1]))
                print("RESULT")
                msg_send = str(listda[0][1]) + "|" + str(listda[0][0]) + "|" + str(listda[0][2])
                print("RESULT")
                print(msg_send)
                return msg_send
    except:
        return False


global result
global Flag


def handle_keystroke():
    global result
    global Flag
    Flag = True

    list_keyboard = ['Escape', 'Space', 'BackSpace', 'Tab', 'Linefeed', 'Clear', 'Return', 'Pause', 'Scroll_Lock',
                     'Sys_Req', 'Delete', 'Home', 'Left', 'Up', 'Right', 'Down', 'Page_Up', 'Page_Down',
                     'End', 'Select', 'Print', 'Execute', 'Insert', 'Menu',
                     'Help', 'Break', 'Num_Lock', 'Enter',

                     'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10', 'F11', 'F12', 'F13',
                     'F14', 'F15', 'F16', 'F17', 'F18', 'F19', 'F20', 'F21',
                     'F22', 'F23', 'F24',
                     'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
                     'U', 'V', 'W', 'X', 'Y', 'Z',
                     '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
                     '/', '`', '~', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '_', '+', '=', '[', ']', '{',
                     '}', '|', ';', ':', '"', '/', '?', '.', '>', ',', '<']

    str_full = []

    while True:  # making a loop

        # used try so that if user pressed other than the given key error will not be shown
        try:
            key = keyboard.read_key()
            for char in list_keyboard:
                # print(key, " == ", char.lower())
                if key == char.lower():
                    str_full.append(key)
                    print(str_full)
        except:
            break

        if keyboard.is_pressed('a'):
            break
        if not Flag:
            break

    print("RESULT: ")
    print(str_full)

    result = []
    for i in range(0, len(str_full), 2):
        result.append(str_full[i])

    print(result)


def handle_inphim():
    global result
    result.pop()
    str_return = ''
    for char in result:
        if char != result[-1]:
            str_return += (char + '|')
        else:
            str_return += char

    return str_return


def handle_unhook():
    global Flag
    Flag = False
    send_keys('{ENTER}')


def handle_getvalue(state, path, name):
    try:
        registry_key = winreg.OpenKey(state, path, 0,
                                      winreg.KEY_READ)
        value, regtype = winreg.QueryValueEx(registry_key, name)
        winreg.CloseKey(registry_key)
        return value
    except WindowsError:
        return None


def handle_setvalue(state, path, name, value, type_INT):
    try:
        winreg.CreateKey(state, path)
        registry_key = winreg.OpenKey(state, path, 0,
                                      winreg.KEY_WRITE)
        winreg.SetValueEx(registry_key, name, 0, type_INT, value)
        winreg.CloseKey(registry_key)
        return True
    except WindowsError:
        return False


def handle_deletevalue(state, path, name):
    try:
        key = winreg.OpenKey(state, path, 0,
                             winreg.KEY_ALL_ACCESS)
        winreg.DeleteValue(key, name)
        winreg.CloseKey(key)
        win32gui.SendMessage(
            win32con.HWND_BROADCAST, win32con.WM_SETTINGCHANGE, 0, 'Environment')
        return True
    except WindowsError:
        return False


def handle_createkey(state, path):
    try:
        winreg.CreateKey(state, path)

        return True
    except WindowsError:
        return False


def handle_deletekey(state, path):
    try:
        key = winreg.OpenKey(state, path, 0, winreg.KEY_ALL_ACCESS)
        winreg.DeleteKey(key, 'Test1')
        return True
    except WindowsError:
        return False


def handle_registry(list_mes):
    mode = list_mes[1]
    path = list_mes[2]
    name = list_mes[3]
    value = list_mes[4]
    datatype = list_mes[5]

    subpath = path.split('\\', 1)
    global state
    if subpath[0] == 'HKEY_CURRENT_USER':
        state = winreg.HKEY_CURRENT_USER
    elif subpath[0] == 'HKEY_CLASSES_ROOT':
        state = winreg.HKEY_CLASSES_ROOT
    elif subpath[0] == 'HKEY_LOCAL_MACHINE':
        state = winreg.HKEY_LOCAL_MACHINE
    elif subpath[0] == 'HKEY_USERS':
        state = winreg.HKEY_USERS
    elif subpath[0] == 'HKEY_CURRENT_CONFIG':
        state = winreg.HKEY_CURRENT_CONFIG

    global type_INT
    if datatype == 'STRING':
        type_INT = winreg.REG_SZ
    elif datatype == 'BINARY':
        type_INT = winreg.REG_BINARY
    elif datatype == 'DWORD':
        type_INT = winreg.REG_DWORD
    elif datatype == 'STRING':
        type_INT = winreg.REG_SZ
    elif datatype == 'QWORD':
        type_INT = winreg.REG_DWORD
    elif datatype == 'MUlTSTRING':
        type_INT = winreg.REG_MULTI_SZ
    elif datatype == 'EXSTRING':
        type_INT = winreg.REG_EXPAND_SZ

    if mode == "GETVALUE":
        return handle_getvalue(state, subpath[1], name)
    elif mode == "SETVALUE":
        return handle_setvalue(state, subpath[1], name, value, type_INT)
    elif mode == "DELETEVALUE":
        return handle_deletevalue(state, subpath[1], name)
    elif mode == "CREATEKEY":
        return handle_createkey(state, subpath[1])
    elif mode == "DELETEKEY":
        return handle_deletekey(state, subpath[1])




def handle_client(conn, addr):
    global Flag
    print(f"[NEW CONNECTION] {addr} connected ")
    connected = True

    while connected:

        msg_len = conn.recv(HEADER).decode(FORMAT)

        if msg_len:
            print(msg_len)
            msg_len = int(msg_len)
            msg = conn.recv(msg_len).decode(FORMAT)
            print(f"[{addr}]{msg}")

            if msg == DISCONNECT_MESSAGE:
                connected = False
            list_mes = msg.split('|')

            if msg == MESSAGE_CMH:
                handle_image(conn)
            elif msg == MESSAGE_PR:
                handle_process(conn)
            elif list_mes[0] == "KILL":
                send_process(conn, str(handle_kill(list_mes[1])))
            elif list_mes[0] == "START":
                send_process(conn, str(handle_start(list_mes[1])))
            elif list_mes[0] == "KEYSTROKE":
                thread = threading.Thread(target=handle_keystroke)
                thread.start()
            elif list_mes[0] == "INPHIM":
                # ------------
                handle_unhook()
                # ------------
                send_process(conn, str(handle_inphim()))
                # -----------------
                thread = threading.Thread(target=handle_keystroke)
                thread.start()

            elif list_mes[0] == "UNHOOK":
                handle_unhook()
            elif list_mes[0] == "REGISTRY":
                send_process(conn, str(handle_registry(list_mes)))

    conn.close()


def start_process():
    server.listen()
    print(f"[LISTENING] Server is listen on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTION] {threading.activeCount() - 1}")


print("[SERVER] is starting . .  .")

# start_process()
global Flag
Flag = False


def turn_on():
    thread = threading.Thread(target=start_process)
    thread.start()


class App(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.start()

    def callback(self):
        self.root.quit()

    def run(self):
        self.root = Tk()
        self.root.protocol("WM_DELETE_WINDOW", self.callback)

        button_start = Button(self.root, text="Start", comman=turn_on)
        button_start.pack()

        self.root.mainloop()


app = App()
print('Now we can continue running code while mainloop runs!')
print("=")
