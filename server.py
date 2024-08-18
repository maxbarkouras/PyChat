# PyChat -- Server
# made by max

import socket
import random
import threading
from time import sleep
from sympy import nextprime

#define variables for server ip and port
HOST = "REPLACE WITH SERVER IP"
PORT = REPLACE WITH SERVER PORT

#create socket and start listening for incoming connections
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST,PORT))
s.listen()

#define global variables
exitsig = 1
exitsig2 = 1
data1 = 1
data2 = 1
activeusr = 0

#generate modular and base for encryption
base = random.randint(3, 99)
mod = nextprime(int(''.join([str(random.randint(1, 9)) for _ in range(1000)])))
print('mod and base generated. now listening...')

#define function for first connection
def client1():
    #accept connection and bring in global variables
    conn, addr = s.accept()
    global activeusr
    activeusr = activeusr+1
    global exitsig
    global data1
    global data2
    global key
    #loop until second client connects
    while activeusr < 2:
        conn.send(('1AU').encode('UTF-8'))
        sleep(0.5)
    #send base and modular to client
    conn.send((f'{base}:esab').encode('UTF-8'))
    conn.send((f'{mod}:dom').encode('UTF-8'))
    
    #define function for sending to client 1
    def sending():
        global exitsig
        global data1
        data1 = 1
        #while for exit signal is not active send the data
        while exitsig == 1:
            if data1 != 1:
                conn.send(data1)
                data1 = 1
                continue
            else:
                pass

    #define function for listening on client 1
    def listening():
        global exitsig
        global data2
        global data1
        global activeusr
        #while exit signal is not active receive the data
        while exitsig == 1:
            #assign data2 variable with received data
            data2 = (conn.recv(1024))
            #check for logout command from client and close connection if logout
            if '!logout' in ((data2).decode('UTF-8')):
                conn.close()
                exitsig=2
                break
            else:
                continue
        exitsig = 1
        activeusr = activeusr-1
        client1()

    #start thread on sending function
    x = threading.Thread(target=sending)
    x.daemon = True
    x.start()
    #send parent thread to listening function
    listening()

#define function for second connection
def client2():
    #accept connection and bring in global variables
    conn, addr = s.accept()
    global activeusr
    global exitsig2
    global data1
    global data2
    global key
    activeusr = activeusr+1
    #send base and modular to client
    conn.send((f'{base}:esab').encode('UTF-8'))
    conn.send((f'{mod}:dom').encode('UTF-8'))

    #define function for sending to client 2
    def sending():
        global exitsig2
        global data2
        data2 = 1
        #while for exit signal is not active send the data
        while exitsig2 == 1:
            if data2 != 1:
                conn.send(data2)
                data2 = 1
                continue
            else:
                pass

    #define function for listening on client 2
    def listening():
        global exitsig2
        global data1
        global data2
        global activeusr
        #while exit signal is not active receive the data
        while exitsig2 == 1:
            #assign data1 variable with received data
            data1 = (conn.recv(1024))
            #check for logout command from client and close connection if logout
            if '!logout' in ((data1).decode('UTF-8')):
                conn.close()
                exitsig2=2
                break
            else:
                continue
        exitsig2 = 1
        activeusr = activeusr-1
        client2()

    #start thread on sending function
    x = threading.Thread(target=sending)
    x.daemon = True
    x.start()
    #send parent thread to listening function
    listening()

#start thread on client1 function
x = threading.Thread(target=client1)
x.daemon = True
x.start()
#send parent thread to client2 function
client2()
