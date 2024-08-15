import socket
import os
import threading
import sys
from time import sleep
from cryptography.fernet import Fernet
import random

print('welcome to PyChat')

def username():
    global user
    user = input('please enter username:\x1b[1;35m ')

    if len(user) == 0 or user == ' ':
        print(f'\x1b[1;31musername "{user}" is not valid\x1b[0m')
        del user
        username()
    else:
        loading()

def xor_encrypt_decrypt(message, key):
    # Convert key to a list of smaller integers
    key = [int(digit) for digit in str(key)]
    
    # Encrypt/Decrypt the message
    encrypted_chars = [
        chr(ord(char) ^ key[i % len(key)]) for i, char in enumerate(message)
    ]
    encrypted_message = ''.join(encrypted_chars)
    
    return encrypted_message

def loading():
    if os.name == 'posix':
        os.system('clear')
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

username()

HOST = "147.182.247.60"
PORT = 4444

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect((HOST,PORT))

whoami='v2'

firstinput = (s.recv(1024)).decode('UTF-8')
cnt = 0
while firstinput == '1AU':
    whoami='v1'
    if cnt < 1:
        print('waiting for second user')
    firstinput = (s.recv(1024)).decode('UTF-8')
    cnt+=1

if os.name == 'posix':
    os.system('clear')
else:
    os.system('cls')

base = (((firstinput).split(':')[0]))
mod = ((((s.recv(1024)).decode('UTF-8')).split(':')[0]))
mynum = random.randint(11, 300)
mykey = (int(base)**int(mynum)) % int(mod)

if whoami == 'v1':
    s.send((f'{mykey}:yek').encode('UTF-8'))
    key = ((((s.recv(1024)).decode('UTF-8')).split(':')[0]))

else:
    key = ((((s.recv(1024)).decode('UTF-8')).split(':')[0]))
    s.send((f'{mykey}:yek').encode('UTF-8'))

finalkey = (int(key)**int(mynum))%int(mod)
print('\x1b[1;31mconnected to PyChat\x1b[0m')

global exitsig
exitsig = 1
def sending():
    global user
    global exitsig
    global key
    global fernet
    while exitsig == 1:
        command = input('\x1b[1;35m')
        if command == '!logout':
            enc = xor_encrypt_decrypt(command, finalkey)
            s.send((f'{user}::{enc}').encode('UTF-8'))
            print(f'\x1b[1;31myou have been logged out\x1b[0m')
            break
        else:
            enc = xor_encrypt_decrypt(command, finalkey)
            s.send((f'{user}::{enc}').encode('UTF-8'))
            continue
    s.close()
    sys.exit()

def listening():
    global exitsig
    global key
    global fernet
    while exitsig == 1:
        raw = ((s.recv(1024)).decode('UTF-8'))
        dataraw = raw.split('::')
        dec = xor_encrypt_decrypt((dataraw[1]),finalkey)
        if '!logout' in dec:
            print(f'\x1b[1;34m{dataraw[0]}\x1b[1;31m has logged out\x1b[1;35m')
            continue
        else:
            if dataraw[0] == ' ':
                print(f'\x1b[0m{dec}\x1b[1;35m')
            else:
                print(f'\x1b[1;34m{dataraw[0]}: \x1b[0m{dec}\x1b[1;35m')

x = threading.Thread(target=listening)
x.daemon = True
x.start()
sending()

# need to add:
    # usernames - done
    # client check - done
    # logout command - done
    # always on - done