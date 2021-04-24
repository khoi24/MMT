import socket
import tkinter
from tkinter import *
from tkinter.ttk import Treeview

from PIL import ImageTk, Image
import os
from tkinter import filedialog
from PIL import ImageFile
import wmi

ImageFile.LOAD_TRUNCATED_IMAGES = True
import time

HEADER = 64
PORT = 2050
SERVER = "192.168.100.12"
FORMAT = "utf-8"
ADDR = (SERVER, PORT)
DISCONNECT_MESSAGE = "!DISCONNECTED"
MESSAGE_CMH = "CHUPMANHINH"
MESSAGE_PR = "PROCESSRUNNING"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


# client.connect(ADDR)

def send(message):
    print("Start sending:  " + message)
    message = message.encode(FORMAT)
    mes_lenth = str(len(message)).encode(FORMAT)
    mes_lenth += b' ' * (HEADER - len(mes_lenth))
    client.send(mes_lenth)
    client.send(message)


def receive():
    msg_length = client.recv(HEADER)
    if msg_length:
        print(msg_length)
        msg_len = int(msg_length)
        msg = client.recv(msg_len)
    return msg


# ---------------------------

IP_SERVER = ''
MESSAGE_TODO = ""

Client = Tk()
Client.title("Client")

T_nhapip = Entry(justify=LEFT, width=50)
T_nhapip.grid(column=0, row=0, padx=5, pady=5, columnspan=5)
T_nhapip.insert(0, "Nhập IP")


def click_ketnoi():
    IP_SERVER = T_nhapip.get()
    sth = Tk()
    try:
        client.connect((T_nhapip.get(), PORT))

        newT = Label(sth, text="[TESTING] Server IP: " + IP_SERVER)
        newT.grid()
    except:
        newF = Label(sth, text="False")
        newF.grid()

    sth.mainloop()


# ------------------Chuc nang chup man hinh----------------
def click_luu(data):
    mask = [
        ("PNG", "*.png"),
        ("Text files", "*.txt"),
        ("Python files", "*.py *.pyw"),
        ("All files", "*.*")
    ]

    # if the filename does not have extension
    # it will add the specified defaultextension
    file_save = ""
    fout = filedialog.asksaveasfile(
        mode='wb',
        title="Save As",
        initialdir="C:/Python27/Atest27/Bull",
        initialfile=file_save,
        defaultextension="*.png",
        filetypes=mask)

    # test write a file
    '''
    data = """\
    1
    2
    3
    4
    """
    '''
    fout.write(data)
    fout.close()


def display_image():
    my_image = Image.open("sth.png")
    my_image_rs = my_image.resize((450, 350), Image.ANTIALIAS)
    my_new_image = ImageTk.PhotoImage(my_image_rs)
    return my_new_image


global data
global my_label


def callback():
    global data
    global my_label
    send(MESSAGE_CMH)
    time.sleep(3)
    file = open('sth.png', 'wb')

    data = receive()
    file.write(data)
    file.close()

    img2 = Image.open("sth.png")
    img2_rs = img2.resize((450, 350), Image.ANTIALIAS)
    img2_new = ImageTk.PhotoImage(img2_rs)
    my_label.configure(image=img2_new)
    my_label.image = img2_new


def click_chupmanhinh():
    global data
    global my_label

    send(MESSAGE_CMH)

    file = open('sth.png', 'wb')

    data = receive()
    file.write(data)
    file.close()

    print("DONE")
    new_cmh = tkinter.Toplevel()

    new_cmh.title("pic")

    my_new_image = display_image()
    my_label = Label(new_cmh, image=my_new_image, width=500, height=500)
    my_label.grid(row=0, column=0, padx=5, pady=5, columnspan=3, rowspan=4)

    B_chup = Button(new_cmh, text="Chụp", width=15, height=13, command=callback)
    B_chup.grid(row=0, column=3, padx=5, pady=10, rowspan=3)

    B_luu = Button(new_cmh, text="Lưu", width=15, height=5, command=lambda: click_luu(data))
    B_luu.grid(row=3, column=3, padx=5, pady=10)

    new_cmh.mainloop()


# ------------------------------

global str_data
global ID_count


def click_processrunning():
    send(MESSAGE_PR)

    prr = Tk()
    prr.title("process")

    table_process = Treeview(prr, selectmode='browse')

    table_process.pack(side='right')  # column=0, row=1, columnspan=4)

    scrollbar = Scrollbar(prr, orient="vertical", command=table_process.yview)
    scrollbar.pack(side='right', fill='x')
    table_process.configure(xscrollcommand=scrollbar.set)

    table_process['columns'] = ["1", "2", "3"]

    table_process['show'] = 'headings'

    table_process.column("1", width=120, anchor=W)
    table_process.column("2", width=120, anchor=CENTER)
    table_process.column("3", width=120, anchor=CENTER)

    table_process.heading("1", text="Name Process", anchor=W)
    table_process.heading("2", text="ID Process", anchor=CENTER)
    table_process.heading("3", text="Count Thread", anchor=W)
    global ID_count
    ID_count = 1
    list_table = []
    while True:
        line = receive()
        line = line.decode(FORMAT)
        if line == "DONE":
            break
        data = line.split('|')
        list_table.append([str(data[1]), data[0], str(data[2])])

        table_process.insert("", 'end', text="L" + str(ID_count),
                             values=(str(data[1]), data[0], str(data[2])))
        ID_count += 1

    def click_kill():
        kill_obj = Tk()
        kill_obj.title("Kill")

        obj = Entry(kill_obj)
        obj.pack()

        def remove():
            send("KILL|" + obj.get())
            if (receive().decode(FORMAT) == "True"):
                for i in table_process.get_children():
                    table_process.delete(i)
                global id
                id = 0
                n = len(list_table)
                while id < n:
                    if list_table[id][1] != obj.get():
                        '''
                        print(line[1])
                        print(type(line[1]))
                        print(" = ")
                        print(id_obj)
                        print(type(id_obj))
                        print("\n")
                        '''
                        table_process.insert("", 'end', text="L" + str(ID_count),
                                             values=(str(list_table[id][1]), list_table[id][0], str(list_table[id][2])))
                    else:
                        list_table.remove(list_table[id])
                        id -= 1
                        n -= 1
                    id += 1
            else:
                print("False")

        b_start = Button(kill_obj, text="Start", command=remove)
        b_start.pack()
        kill_obj.mainloop()

    b_kill = Button(prr, text="Kill", command=click_kill)
    b_kill.pack()

    def click_startOUT():
        startP = Tk()
        startP.title("Start")
        start_input = Entry(startP)
        start_input.pack()

        def add_process():
            send("START|" + start_input.get())
            str_start = receive().decode(FORMAT)
            list_start = str_start.split('|')
            global ID_count
            table_process.insert("", 'end', text="L" + str(ID_count),
                                 values=(str(list_start[0]), str(list_start[1]), str(list_start[2])))
            ID_count += 1

        b_start_process = Button(startP, text="Start", command=add_process)
        b_start_process.pack()

    b_startOUT = Button(prr, text="Start", command=click_startOUT)
    b_startOUT.pack()

    prr.mainloop()


# -----------------------APP


# -------------------------keystroke-------------------
def click_keystroke():
    key_stroke = Tk()
    key_stroke.title("KeyStroke")

    def click_hook():
        send("KEYSTROKE")

    button_hook = Button(key_stroke, text="Hook", command=click_hook)
    button_hook.pack()

    def click_inphim():
        send("INPHIM")
        result_phim = receive()
        print(result_phim)

    button_inphim = Button(key_stroke, text="In Phím", command=click_inphim)
    button_inphim.pack()

    def click_unhook():
        send("UNHOOK")

    button_unhook = Button(key_stroke, text="UnHook", command=click_unhook)
    button_unhook.pack()

    key_stroke.mainloop()


# --------------Registry------------------
global filename
global namevalue
global giatri
global g_name
global g_value
global g_type
global g_mode


def click_suaregistry():
    OPTIONS = [
        "Get value", "Set value", "Delete value", "Create key", "Delete key"
    ]
    OPT = ["String", "Binary", "DWORD", "QWORD", "Multi-String", "Expandable String"]

    global filename
    registry = Tk()
    registry.title('Application')
    duongdan = Text(registry, width=70, height=1)
    duongdan.grid(row=0, column=0, padx=5, pady=5, columnspan=2)
    mo_ta = Text(registry, width=70, height=5)
    mo_ta.grid(row=1, column=0, padx=5, pady=5, columnspan=2, rowspan=4)

    def click_browser():
        global filename
        filename = filedialog.askopenfilename(initialdir="/", title="Open", filetypes=(
            ("jpeg files", "*.jpg"), ("gif files", "*.gif*"), ("png files", "*.png"), ("All files", "*.*")))
        duongdan.insert(tkinter.END, filename)

        file = open(filename, 'r', encoding='utf-16')
        list_line_from_file = file.readlines()
        file.close()

        for i in range(0, len(list_line_from_file)):
            mo_ta.insert(tkinter.END, list_line_from_file[i])

        print(mo_ta.get("1.0", "end-1c"))

    b_browser = Button(registry, text="Browser... ", command=click_browser)
    b_browser.grid(row=0, column=2, padx=5, pady=5)

    def click_guinoidung():
        filew = open(filename, 'w', encoding='utf-16')
        print(filename)
        filew.write(mo_ta.get("1.0", "end-1c"))

    b_guinoidung = Button(registry, text='Gửi nội dung', command=click_guinoidung)
    b_guinoidung.grid(row=1, column=2, padx=5, pady=5, rowspan=4)

    registry.columnconfigure(0, weight=1)
    registry.rowconfigure(0, weight=1)

    frame_suagiatri = LabelFrame(registry, text="Sửa giá trị trực tiếp", width=70)
    frame_suagiatri.grid(row=5, column=0, columnspan=3, rowspan=4)

    clicked = StringVar(frame_suagiatri)
    clicked.set("Get value")

    opt_value = OptionMenu(frame_suagiatri, clicked, *OPTIONS)
    opt_value.grid(row=5, column=0, columnspan=3)
    # menu = opt_value.children["menu"]
    # menu.delete(0, "end")
    subpath = Text(frame_suagiatri, width=50, height=1)
    subpath.grid(row=6, column=0, columnspan=3, padx=5, pady=5)

    def w_chinhsua(str_state):

        w_batdauchinhsua = Tk()
        print(clicked.get())
        list_opt = []
        if clicked.get() == OPTIONS[0]:
            name_value = Text(w_batdauchinhsua, height=1, width=15)
            name_value.grid(row=0, column=0, padx=5, pady=5)
            print("here " + name_value.get("1.0", 'end-1c'))
            list_opt.append(name_value.get("1.0", 'end-1c'))

        elif clicked.get() == OPTIONS[1]:
            name_value = Text(w_batdauchinhsua, height=1, width=15)
            name_value.grid(row=0, column=0, padx=5, pady=5)

            t_value = Text(w_batdauchinhsua, height=1, width=15)
            t_value.grid(row=0, column=1, padx=5, pady=5)
            g_value = t_value.get("1.0", 'end-1c')

            choose = StringVar(w_batdauchinhsua)
            choose.set(OPT[0])

            opt = OptionMenu(w_batdauchinhsua, choose, *OPT)
            opt.grid(row=5, column=0, columnspan=3)

        elif clicked.get() == OPTIONS[2]:
            name_value = Text(w_batdauchinhsua, height=1, width=15)
            name_value.grid(row=0, column=0, padx=5, pady=5)
            print("here " + name_value.get("1.0", 'end-1c'))
            list_opt.append(name_value.get("1.0", 'end-1c'))
        elif clicked.get() == OPTIONS[3]:
            notice = Label(w_batdauchinhsua, text = "Click để gửi yêu cầu")
            notice.grid(row = 0,column=0,padx=5,pady=5)
        elif clicked.get() == OPTIONS[3]:
            notice = Label(w_batdauchinhsua, text = "Click để gửi yêu cầu")
            notice.grid(row = 0,column=0,padx=5,pady=5)

        def click_gui():
            global g_name
            global g_value
            global g_type
            global g_mode
            g_name = '_'
            g_value = '_'
            g_type = '_'
            g_mode = '_'
            try:
                g_mode = clicked.get()
                g_mode = g_mode.replace(" ", "")
                g_mode = g_mode.upper()
                g_name = name_value.get("1.0", 'end-1c')
                g_value = t_value.get("1.0", 'end-1c')
                g_type = choose.get().upper()

            except:
                pass

            send_msg = "REGISTRY" + "|" + g_mode + "|" + subpath.get("1.0",
                                                                     'end-1c') + "|" + g_name + "|" + g_value + "|" + g_type
            send(send_msg)
            print(receive())

        b_gui = Button(w_batdauchinhsua, text="Gửi", command=click_gui)
        b_gui.grid()

        w_batdauchinhsua.mainloop()

    # for value in OPTIONS:
    #  menu.add_command(label=value, command=lambda v=value: w_chinhsua(v))
    b_start_chinhsua = Button(registry, text='Bắt đầu chỉnh sửa', command=lambda v=clicked.get(): w_chinhsua(v))
    b_start_chinhsua.grid(row=6, column=2, padx=5, pady=5)

    registry.mainloop()


B_ketnoi = Button(Client, text="Kết nối", width=10, command=click_ketnoi)
B_ketnoi.grid(column=5, row=0, padx=5, pady=20, columnspan=2)

B_processrunning = Button(Client, text="Process Running", justify=LEFT, width=15, height=15,
                          command=click_processrunning)
B_processrunning.grid(column=0, row=1, padx=5, pady=5, columnspan=2, rowspan=6)

B_apprunning = Button(Client, text="App Running", width=23, height=5)
B_apprunning.grid(column=2, row=1, padx=5, pady=5, columnspan=3, rowspan=2)

B_tatmay = Button(Client, text="Tắt máy", justify=LEFT, width=7, height=4)
B_tatmay.grid(column=2, row=3, padx=5, pady=5, rowspan=2)

B_suaregistry = Button(Client, text="Sửa Registry", justify=LEFT, width=22, height=3, command=click_suaregistry)
B_suaregistry.grid(column=2, row=5, padx=5, pady=5, columnspan=4, rowspan=2)

B_chupmanhinh = Button(Client, text="Chụp màn hình", width=13, height=4, command=click_chupmanhinh)
B_chupmanhinh.grid(column=3, row=3, padx=5, pady=5, columnspan=2)

B_thoat = Button(Client, text="Thoát", width=10, height=3)
B_thoat.grid(column=6, row=5, padx=5, pady=5, rowspan=2)

B_ketstoke = Button(Client, text="Keystoke", width=10, height=10, command=click_keystroke)
B_ketstoke.grid(column=5, row=1, padx=5, pady=5, columnspan=2, rowspan=4)

print(IP_SERVER)

Client.mainloop()
os.remove("sth.png")
