import socket
from threading import Thread
from datetime import datetime


# create a TCP socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connect the client .eg. client.connect((target, port))
ServerIP = "127.0.0.1"
ServerPort = 8700
client.connect((ServerIP, ServerPort))

print(f"[**] Connecting => {ServerIP}:{ServerPort} --->")

# client listening server's response
response = client.recv(2048)

''' Response : Status of Connection :
	1 : Registeration successful 
	2 : Connection Successful
	3 : Login Failed
'''
separator_token = "<<#>>"

# Input UserName
username = input(response.decode())	
client.send(str.encode(username))   # sends username to server
response = client.recv(2048)        # receive server's response

# Input Password
password = input(response.decode())	
client.send(str.encode(password))   # sends password to server
response = client.recv(2048)        # receive server's response
response = response.decode()        # decoding the received response from the server

# function to listen for messages from different clients
def listen_for_messages():
    while True:
        message = client.recv(2048).decode()
        print("\n>>> " + message)

# make a thread that listens for messages to this client and print them on console
t = Thread(target=listen_for_messages)

# make the thread daemon so it ends whenever the main thread ends
t.daemon = True

# lastly start the thread
t.start()

while True:
    # input message we want to send to the server
    to_send = input(">>> ")
    # exit the program
    if to_send.lower() == "q":
        break
    # add the datetime, username of the sender
    date_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    to_send = f" [{date_now}][{username}]{separator_token}{to_send}"

    client.send(to_send.encode()) # finally send the message

# close the client socket
client.close()
