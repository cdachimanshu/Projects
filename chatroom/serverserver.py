import socket
import os
import threading
import hashlib

# create a TCP connection
ServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ServerHost = "127.0.0.1"
ServerPort = 8700

# making the port as reusable port
ServerSocket.setsockopt(socket.AF_INET, socket.SOCK_STREAM)

# creating a set to store all connected client's sockets
client_sockets = set()

# a seperator to distinguish client name and message
separator_token = "<<#>>"

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
        print("{:<8} {:<20}" . format("USER", "PASSWORD"))
        for k,v in HashTable.items():
            label, num = k, v
            print("{:<8} {:<20}" . format(label, num))
        print("*****************************************************")
    else:
        # if user already exist, check if the entered password is correct
        if(HashTable[username] == password):
            conn.send(str.encode("Connection successful...")) # responded to client
            print("Connected: ", username)
        else:
            conn.send(str.encode("Login Failed....")) # respond if login fails
            print("Connection denied: ", username)

    while True:
        try:
            # keep listening for messages from the socket
            msg = ServerSocket.recv(1024).decode()
        except Exception as e:
            # client no longer connected, then remove it from the set
            print(f"[!!!] ERROR: {e}")
            client_sockets.remove(ServerSocket)
        else:
            # if message is received, replace the the <<#>> token with ">>>" for printing
            msg = msg.replace(separator_token, ">>> ")

        # iterate over all connected sockets
        for client_socket in client_sockets:
            client_socket.send(msg.encode())

    #conn.close() # close the connection

# Accepting user connection
while True:
    Client, address = ServerSocket.accept()
    print(f"[+] {Client} connected ....")

    # add the new connected client to connected sockets
    client_sockets.add(Client)

    # start a new thread that listen for each client's messages
    client_handler = threading.Thread(target=handle_client, args=(Client,))
    
    # make the thread daemon so it ends whenever the main thread ends
    client_handler.daemon = True

    # starting the thread ...
    client_handler.start() 

# close client sockets
for cs in client_sockets:
    cs.close()

# closing server socket    
ServerSocket.close() # closing the socket
