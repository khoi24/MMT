import socket
import threading
from pywinauto import *
from pywinauto.keyboard import *
from mss import mss
import os
import wmi
import signal

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


def handle_client(conn, addr):
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

start_process()
