import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('localhost', 8081))

s.listen(2)

while True:
    print(">>> Waiting for connection <<<")
    (recvSocket, address) = s.accept()
    print("http request received :")
    print(recvSocket.recv(1024))
    recvSocket.send(bytes("HTTP/1.1 200 OK\r\n\r\n<html><body><h1> Hello, Everyone !!!</h1></body></html> \r\n", "utf-8"))
    recvSocket.close()

