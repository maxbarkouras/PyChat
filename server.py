import socket
from time import sleep
import threading
import sys
import random
from sympy import nextprime

HOST = "REPLACE WITH SERVER IP"
PORT = REPLACE WITH SERVER PORT

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST,PORT))
s.listen()

exitsig = 1
exitsig2 = 1
data1 = 1
data2 = 1
activeusr = 0

base = random.randint(3, 99)
mod = nextprime(int(''.join([str(random.randint(1, 9)) for _ in range(1000)])))
print('mod and base generated. now listening...')

def client1():
    conn, addr = s.accept()
    global activeusr
    activeusr = activeusr+1
    global exitsig
    global data1
    global data2
    global key
    while activeusr < 2:
        conn.send(('1AU').encode('UTF-8'))
        sleep(0.5)
    conn.send((f'{base}:esab').encode('UTF-8'))
    conn.send((f'{mod}:dom').encode('UTF-8'))
    def sending():
        global exitsig
        global data1
        data1 = 1
        while exitsig == 1:
            if data1 != 1:
                conn.send(data1)
                data1 = 1
                continue
            else:
                pass

    def listening():
        global exitsig
        global data2
        global data1
        global activeusr
        while exitsig == 1:
            data2 = (conn.recv(1024))
            if '!users' in ((data2).decode('UTF-8')):
                data2 = 1
                users = (f'there are currently \x1b[32m{activeusr}\x1b[0m active user(s)')
                conn.send((f' ::{users}').encode('UTF-8'))
            elif '!logout' in ((data2).decode('UTF-8')):
                conn.close()
                exitsig=2
                break
            else:
                continue
        exitsig = 1
        activeusr = activeusr-1
        client1()

    x = threading.Thread(target=sending)
    x.daemon = True
    x.start()
    listening()

def client2():
    conn, addr = s.accept()
    global activeusr
    global exitsig2
    global data1
    global data2
    global key
    activeusr = activeusr+1
    while activeusr < 2:
        conn.send(('1AU').encode('UTF-8'))
        sleep(0.5)
    conn.send((f'{base}:esab').encode('UTF-8'))
    conn.send((f'{mod}:dom').encode('UTF-8'))
    def sending():
        global exitsig2
        global data2
        data2 = 1
        while exitsig2 == 1:
            if data2 != 1:
                conn.send(data2)
                data2 = 1
                continue
            else:
                pass

    def listening():
        global exitsig2
        global data1
        global data2
        global activeusr
        while exitsig2 == 1:
            data1 = (conn.recv(1024))
            if '!logout' in ((data1).decode('UTF-8')):
                conn.close()
                exitsig2=2
                break
            else:
                continue
        exitsig2 = 1
        activeusr = activeusr-1
        client2()

    x = threading.Thread(target=sending)
    x.daemon = True
    x.start()
    listening()

x = threading.Thread(target=client1)
x.daemon = True
x.start()
client2()
