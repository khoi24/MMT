import tkinter
from tkinter import *
from PIL import ImageTk, Image
import tkinter.font
IP_SERVER = ''
MESSAGE_TODO = ""


Client = Tk()
Client.title("Client")

T_nhapip = Entry(justify=LEFT,width=50)
T_nhapip.grid(column = 0,row = 0,padx =5,pady=5,columnspan=5)
T_nhapip.insert(0,"Nhập IP")

def click_ketnoi():
   IP_SERVER = T_nhapip.get()
   sth =Tk()
   newT= Label(sth,text = "[TESTING] Server IP: "+IP_SERVER)
   newT.grid()
   sth.mainloop()

def click_luu():
   pass

def click_chupmanhinh():
   print("sthherer")

   new_cmh = tkinter.Toplevel()

   new_cmh.title("pic")
   my_image = Image.open("sth1.png")
   my_image_rs = my_image.resize((450, 350), Image.ANTIALIAS)
   my_new_image = ImageTk.PhotoImage(my_image_rs)
   my_label = Label(new_cmh,image = my_new_image,width=500,height=500)
   my_label.grid(row = 0 ,column=0,padx=5,pady=5,columnspan=3,rowspan=4)

   B_chup = Button(new_cmh,text = "Chụp",width=15,height=13)
   B_chup.grid(row = 0 ,column=3,padx=5,pady=10,rowspan=3)

   B_luu = Button(new_cmh,text ="Lưu",width=15,height=5)
   B_luu.grid(row =3,column=3,padx=5,pady=10)


   new_cmh.mainloop()


B_ketnoi = Button(Client,text = "Kết nối",width=10,command = click_ketnoi)
B_ketnoi.grid(column = 5, row=0,padx=5,pady=20,columnspan=2)

B_processrunning = Button(Client,text ="Process Running",justify=LEFT,width=15,height=15)
B_processrunning.grid(column=0,row=1,padx=5,pady=5,columnspan=2,rowspan=6)

B_apprunning = Button(Client, text = "App Running",width=23,height=5)
B_apprunning.grid(column=2, row=1,padx=5,pady=5,columnspan=3,rowspan=2)

B_tatmay = Button(Client,text ="Tắt máy",justify=LEFT,width=7,height=4)
B_tatmay.grid(column=2,row=3,padx=5,pady=5,rowspan=2)

B_suaregistry = Button(Client,text = "Sửa Registry",justify=LEFT,width=22,height=3)
B_suaregistry.grid(column=2,row=5,padx=5,pady=5,columnspan=4,rowspan=2)


B_chupmanhinh = Button(Client,text = "Chụp màn hình",width=13,height=4,command = click_chupmanhinh)
B_chupmanhinh.grid(column=3,row=3,padx=5,pady=5,columnspan=2)

B_thoat =  Button(Client,text ="Thoát",width=10,height=3)
B_thoat.grid(column = 6,row=5,padx=5,pady=5,rowspan=2)

B_ketstoke = Button(Client, text ="Keystoke",width=10,height=10)
B_ketstoke.grid(column=5,row=1,padx=5,pady=5,columnspan=2 ,rowspan=4)






print(IP_SERVER)









































Client.mainloop()