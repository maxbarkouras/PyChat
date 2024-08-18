# PyChat -- Client
# made by max

import os
import sys
import random
import socket
import threading
from time import sleep

print('welcome to PyChat')

#define function for username input
def username():
    global user
    user = input('please enter username:\x1b[1;35m ')
    #ensure username is valid
    if len(user) == 0 or user == ' ':
        print(f'\x1b[1;31musername "{user}" is not valid\x1b[0m')
        del user
        #restart username function if invalid username
        username()
    else:
        #send to loading function if valid username
        loading()

#define method for message encryption/decryption
def xor_encrypt_decrypt(message, key):
    key = [int(digit) for digit in str(key)]
    encrypted_chars = [
        chr(ord(char) ^ key[i % len(key)]) for i, char in enumerate(message)
    ]
    encrypted_message = ''.join(encrypted_chars)
    return encrypted_message

#define function for PyChat startup, just so it looks pretty
def loading():
    #if using linux run 'cls'
    if os.name == 'posix':
        os.system('clear')
    #if using windows run 'clear'
    else:
        os.system('cls')

    print('\x1b[32mconnecting')
    sleep(1)

    if os.name == 'posix':
        os.system('clear')
    else:
        os.system('cls')

    print('\x1b[32mconnecting.')
    sleep(1)

    if os.name == 'posix':
        os.system('clear')
    else:
        os.system('cls')

    print('\x1b[32mconnecting..')
    sleep(1)

    if os.name == 'posix':
        os.system('clear')
    else:
        os.system('cls')

    print('\x1b[32mconnecting...')
    sleep(1)

    if os.name == 'posix':
        os.system('clear')
    else:
        os.system('cls')

#call username function
username()

#define variables for server ip and port
HOST = "REPLACE WITH SERVER IP"
PORT = REPLACE WITH SERVER PORT

#create socket and send connection
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST,PORT))

#define 'whoami' variable so the client knows if it is client 1 or 2
whoami='v2'

#recieves first message from server
firstinput = (s.recv(1024)).decode('UTF-8')
cnt = 0
#if client is first connection, loop until second client is online
while firstinput == '1AU':
    whoami='v1'
    if cnt < 1:
        print('waiting for second user')
    firstinput = (s.recv(1024)).decode('UTF-8')
    cnt+=1

#clear screen
if os.name == 'posix':
    os.system('clear')
else:
    os.system('cls')

#recieve base and modular for creating encryption key
base = (((firstinput).split(':')[0]))
mod = ((((s.recv(1024)).decode('UTF-8')).split(':')[0]))

#generate random number to create key
mynum = random.randint(11, 300)
mykey = (int(base)**int(mynum)) % int(mod)

#if client is client 1, send key and then receive key
if whoami == 'v1':
    s.send((f'{mykey}:yek').encode('UTF-8'))
    key = ((((s.recv(1024)).decode('UTF-8')).split(':')[0]))

#if client is client 2, receive key and then send key
else:
    key = ((((s.recv(1024)).decode('UTF-8')).split(':')[0]))
    s.send((f'{mykey}:yek').encode('UTF-8'))

#get final key and output connection success
finalkey = (int(key)**int(mynum))%int(mod)
print('\x1b[1;31mconnected to PyChat\x1b[0m')

global exitsig
exitsig = 1

#define sending function
def sending():
    global user
    global exitsig
    global key
    global fernet
    #if exit signal is not active take user message input
    while exitsig == 1:
        command = input('\x1b[1;35m')
        #if input is logout
        if command == '!logout':
            enc = xor_encrypt_decrypt(command, finalkey)
            s.send((f'{user}::{enc}').encode('UTF-8'))
            print(f'\x1b[1;31myou have been logged out\x1b[0m')
            break
        else:
            #if not logout, encrypt message and send
            enc = xor_encrypt_decrypt(command, finalkey)
            s.send((f'{user}::{enc}').encode('UTF-8'))
            continue
    s.close()
    sys.exit()

#define listening function
def listening():
    global exitsig
    global key
    global fernet
    #if exit signal is not active receive message
    while exitsig == 1:
        #receive and decrypt message
        raw = ((s.recv(1024)).decode('UTF-8'))
        dataraw = raw.split('::')
        dec = xor_encrypt_decrypt((dataraw[1]),finalkey)
        #if message is logout command, print logout message 
        if '!logout' in dec:
            print(f'\x1b[1;34m{dataraw[0]}\x1b[1;31m has logged out\x1b[1;35m')
            continue
        #otherwise print decoded message
        else:
            print(f'\x1b[1;34m{dataraw[0]}: \x1b[0m{dec}\x1b[1;35m')

#start thread on listening function
x = threading.Thread(target=listening)
x.daemon = True
x.start()
#send parent thread to sending function
sending()
