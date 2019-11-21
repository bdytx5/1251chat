from tkinter import *  
import socket
import logging
import threading
import time


signupR = Tk()
name = ''
username = 'sds'

currentChat = ''
convos = {}


def signupPage():  
    
    signupR.title('1251 Chat') 
    e1 = Entry(signupR) 
    e1.grid(row=2, column=1) 
    def setName():
        global username
        n = e1.get()
        if n != '':
            username = e1.get()
            signupR.destroy()
    label = Label(signupR, text="Enter your name to chat!")
    label.grid(row=1,column=1)
    signUpBtn = Button(signupR, text='Create Convo', width=10, command=setName)
    signUpBtn.grid(row=3, column=1) 



    

signupPage()
signupR.mainloop() 





r = Tk()
scroll = Scrollbar(r)
scroll2 = Scrollbar(r)
msgs = Listbox(r, yscrollcommand = scroll2.set ) 
mylist = Listbox(r, yscrollcommand = scroll.set ) 


def thread_function(name):
    logging.info("Thread %s: starting", name)
    HOST = "128.206.19.255"  # Standard loopback interface address (localhost)
    PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

    server_socket = socket.socket()
    server_socket.bind(('', 8820))
    global username
    while True:

        server_socket.listen(1)

        (client_socket, client_address) = server_socket.accept()

        client_data = client_socket.recvfrom(1024)
        print("Received: %s" % client_data)
        msg = client_data.decode("utf-8")
        if msg == '!':
            print("done")
            client_socket.close()
            server_socket.close()
            return 
        try:
            sender = msg.split('-')[0]
            recip = msg.split('-')[1]
            if sender == username: # just sent message 
                convos[recip].append(msg)
                msgs.insert(END, msg)
            if recip == username: # just recieved message 
                convos[sender] = [convos[sender], msg]
                if currentChat == recip:
                    msgs.insert(msg)
        except:
            continue

                







def msg_ui():
    r.title('1251 Chat') 
    mylist.grid(row=1, column=1,)
    recipNameEntry = Entry(r) 
    recipNameEntry.grid(row=2, column=1) 
    scroll.config( command = mylist.yview) 
    msgs.grid(row=1, column=2,) 
   
    def OnSelect(event):
        selectedConvo = event.widget.get(event.widget.curselection()[0])
        name = selectedConvo
        msgs.delete(0,'end')
        for msg in convos[selectedConvo]:
            msgs.insert(END,msg)
        
    def create_convo():
        rname = recipNameEntry.get()
        if rname == '':
            return 
        # need to check if there is a convo already 
        for key in convos.keys():
            if key == rname:
                return
        

        # if not, add to convo list 
        convos[rname] = []
        mylist.insert(END,rname)
        recipNameEntry.delete(0, 'end')
        mylist.bind("<<ListboxSelect>>", OnSelect)


    createConvoBtn = Button(r, text='Create Convo', width=10, command=create_convo)
    createConvoBtn.grid(row=3,column=1)
    sendBtn = Button(r, text='Send', width=25, command=create_convo) 
    e1 = Entry(r) 
    e1.grid(row=2, column=2) 
    sendBtn.grid(row=3, column=2) 




def uiThread():
    # need to recieve from pipe ! (in thread)
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
    datefmt="%H:%M:%S") 
    logging.info("Main    : before creating thread")
    x = threading.Thread(target=thread_function, args=(1,))
    logging.info("Main: before running thread")
    x.start()







msg_ui()






uiThread()
r.mainloop() 
