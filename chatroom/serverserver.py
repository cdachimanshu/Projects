import socket
import os
import threading
import hashlib

# create a TCP connection
ServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ServerHost = "127.0.0.1"
ServerPort = 8700

try:
    ServerSocket.bind((ServerHost, ServerPort))
except socket.error as e:
    print(str(e))


print("[***] WAITING for a Connection ...")
ServerSocket.listen(5)

HashTable = {} # Dictionary to store the username and hashed password

# Function for handling each client
def handle_client(conn):
    # request username from the client
    conn.send(str.encode("Enter Username:"))
    username = conn.recv(2048)
    # request user's password
    conn.send(str.encode("Enter Password:"))
    password = conn.recv(2048)

    # decode received messages
    username = username.decode()
    password = password.decode()
    # password hash using SHA256
    password = hashlib.sha256(str.encode(password)).hexdigest()

    # If new user, register and store their values in Dictionary
    if username not in HashTable:
        HashTable[username]=password
        conn.send(str.encode("Registration Successfull..."))
        print("Registered: ", username)
        print("{:<8} {:<20}" . format("
