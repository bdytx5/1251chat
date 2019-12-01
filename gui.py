from tkinter import *  
import socket
import logging
import threading
import time
import sys
import os





try:
    PORT = int(sys.argv[1])
except:
    PORT = 8820

UDP_IP = "128.206.19.255" # set it to destination IP.. RPi in this case
# msgSocket = socket.socket() # for sending messages 
server_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
server_socket.bind(("0.0.0.0", PORT))

msgSocket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
msgSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

#msgSocket.bind(('<LAN/Local IP address>', 8000))
# for pi
# UDP_IP = "128.206.19.255" # set it to destination IP.. RPi in this case
# UDP_PORT = 12345
# sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
# sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

username = 'by'
selectedConvo = '1251'
convos = {}
convos['1251'] = ['1251 Class Chat']

signupR = Tk()
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
mylist.insert(END, '1251')
msgs.config(width=60,height=10)
msgs.insert(END, '1251 Class Chat')



chkValue = BooleanVar() 
chkValue.set(True)
 
chkExample = Checkbutton(r, text='Sound On', var=chkValue) 
chkExample.grid(column=1, row=4)

def playSoundAndLight(): 
    os.system("gcc wpi.c -l wiringPi")
    os.system("./a.out")

def showLight(): 
    os.system("gcc wpiNoSound.c -l wiringPi")
    os.system("./a.out")

def newNotification():
    sounds = chkValue.get()
    if sounds:
        playSoundAndLight()
    else:
        showLight()

def OnSelect(event):
    global selectedConvo
    selectedConvo = event.widget.get(event.widget.curselection()[0])
    msgs.delete(0,'end')
    for msg in convos[selectedConvo]:
        msgs.insert(END,msg)


def thread_function(name):
    logging.info("Thread %s: starting", name)
    HOST = "128.206.19.255"  # Standard loopback interface address (localhost)
    PORT = 65432        # Port to listen on (non-privileged ports are > 1023)
    global username
    global selectedConvo
    # server_socket.listen(1)
    # (client_socket, client_address) = server_socket.accept()

    while True:
        client_data = server_socket.recvfrom(1024)
        msg = client_data[0].decode("utf-8")
        if msg == '!':
            print("done")
            client_socket.close()
            server_socket.close()
            return 
        try:
            sender = msg.split('-')[0]
            recip = msg.split('-')[1]
            msg = msg[(len(sender)+len(recip)+2):len(msg)]
            msg = '{}: {}'.format(sender, msg)
            if sender == username or recip == '1251': # just sent message 
                if sender != username: # for group Msg
                    newNotification()


                try:
                    convos[recip].append(msg)
                except:
                    convos[recip] = [msg]
                    mylist.insert(END,recip)
                    mylist.bind("<<ListboxSelect>>", OnSelect)
                if ((recip == selectedConvo) or (selectedConvo == '')):
                    selectedConvo = recip
                    msgs.insert(END, msg)
            if recip == username: # just recieved message
                newNotification()
                try:
                    convos[sender].append(msg)
                except:
                    convos[sender] = [msg]
                    mylist.insert(END,sender)
                    mylist.bind("<<ListboxSelect>>", OnSelect)
                if selectedConvo == sender or (selectedConvo == ''):
                    selectedConvo = sender
                    msgs.insert(END, msg)
        except:
            # (client_socket, client_address) = server_socket.accept()
            continue

                






def msg_ui():
    r.title('piMessage') 
    mylist.grid(row=1, column=1,)
    recipNameEntry = Entry(r) 
    recipNameEntry.grid(row=2, column=1) 
    scroll.config( command = mylist.yview) 
    msgs.grid(row=1, column=2,) 

    def create_convo():
        global selectedConvo
        rname = recipNameEntry.get()
        if rname == '':
            return 
        # need to check if there is a convo already 
        for key in convos.keys():
            if key == rname:
                return
        if selectedConvo == '':
            selectedConvo = rname
        

        # if not, add to convo list 
        convos[rname] = []
        mylist.insert(END,rname)
        recipNameEntry.delete(0, 'end')
        mylist.bind("<<ListboxSelect>>", OnSelect)


    createConvoBtn = Button(r, text='Create Convo', width=10, command=create_convo)
    createConvoBtn.grid(row=3,column=1)
    msgEntry = Entry(r) 
    msgEntry.grid(row=2, column=2) 


    def sendMsg():
        global PORT
        global selectedConvo
        msg = msgEntry.get()
        msgEntry.delete(0, 'end')
        if selectedConvo != '' and username != '':
            encodedMsg = '{}-{}-{}'.format(username,selectedConvo,msg)
            try:
                msgSocket.sendto(encodedMsg.encode("utf-8"), (UDP_IP, PORT))
                # msgSocket.send(encodedMsg.encode("utf-8"))
            except:
                try:
                    #msgSocket.connect(("127.0.0.1", PORT))
                    msgSocket.sendto(encodedMsg.encode("utf-8"), (UDP_IP, PORT))
                except:
                    print('error')
        # FOR PI
        # sock.sendto(b'LED=0\n', (UDP_IP, PORT))

    sendBtn = Button(r, text='Send', width=25, command=sendMsg) 
    sendBtn.grid(row=3, column=2) 




def uiThread():
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
    datefmt="%H:%M:%S") 
    logging.info("Main    : before creating thread")
    thread = threading.Thread(target=thread_function, args=(1,))
    thread.start()





msg_ui()
uiThread()
r.mainloop() 
