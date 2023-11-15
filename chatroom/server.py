# server with no authentication

import socket
from threading import Thread

# server's IP address
SERVER_HOST = "10.252.7.59"
#SERVER_HOST = socket.gethostbyaddr(socket.gethostname())

#host_name = socket.gethostname()
#s_ip = socket.gethostbyname(host_name)

SERVER_PORT = 5002 # port we want to use
separator_token = "<SEP>" # we will use this to separate the client name & message

# initialize set of all connected client's sockets
client_sockets = set()

# create a TCP socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# make the port as reusable port
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# bind the socket to the address we specified
s.bind((SERVER_HOST, SERVER_PORT))

# listen for upcoming connections
s.listen(5)

print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")

def listen_for_client(cs):
    """
    Adding authentication:
        >> to each client server will send  messages requesting username and password 
        >> receive the response from the clients
        >> store the values in a dictionary. Dictionary will store the username as key and hashed password as corresponding value.
        >> checks if username exists in Dictionary.
        >> if new user, then add username and password into dictionary
        >> else if already existing user, then check the entered password with the stored password 
        >> if password is correct then send "connection successful" msg
        >> if not then send "Authentication failed" msg
    This function keep listening for a message from `s` socket
    Whenever a message is received, broadcast it to all other connected clients

    """
    while True:
        try:
            # keep listening for a message from `cs` socket
            msg = cs.recv(1024).decode()
            
        except Exception as e:
            # client no longer connected
            # remove it from the set
            print(f"[!] Error: {e}")
            client_sockets.remove(cs)
        else:
            # if we received a message, replace the <SEP> 
            # token with ": " for nice printing
            msg = msg.replace(separator_token, ": ")
        # iterate over all connected sockets
        for client_socket in client_sockets:
            # and send the message
            client_socket.send(msg.encode())


while True:
    # we keep listening for new connections all the time
    client_socket, client_address = s.accept()
    print(f"[+] {client_address} connected...")
    # add the new connected client to connected sockets
    client_sockets.add(client_socket)
    # start a new thread that listens for each client's messages
    t = Thread(target=listen_for_client, args=(client_socket,))
    # make the thread daemon so it ends whenever the main thread ends
    t.daemon = True
    # start the thread
    t.start()

# close client sockets
for cs in client_sockets:
    cs.close()
# close server socket
s.close()
