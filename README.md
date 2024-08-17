# PyChat

A peer-to-peer encrypted 2 person chat client designed to be entirely self-hosted. PyChat uses the Diffie-Hellman key exchange to allow for encrypted and secure communication between both parties. The server solely acts as a relay on the public internet, allowing the two clients to connect, but does no encryption/decryption nor does it receive the encryption keys at any point. This project started as a POC for me to explore asymmetric encryption and how it works in an applied setting.

## Getting Started

Follow these simple steps to setup your server and use PyChat:

### Prerequisites

1. A VPS (or a machine on your home network that has been port-forwarded)
2. Python3 on all clients and the server

### Installation

1. Download the server.py to your VPS, and client.py to both parties that will be chatting

2. In all instances of the client.py and server.py YOU MUST CHANGE the host ip address to the external ip of your server

3. Launch the server with ```python3 server.py``` and wait for the "mod and base generated. now listening..." output
   
4. Launch the clients on both machines with ```python3 client.py``` and you should be connected!

---

Done!
