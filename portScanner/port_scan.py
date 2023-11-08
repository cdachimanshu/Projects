#!/usr/bin/env python3

import socket
import subprocess
import sys
from datetime import datetime

# blank the screen if there is something on it.
subprocess.call("cls", shell=True)

remoteServer = input("Enter a host to scan:")
remoteIP = socket.gethostbyname(remoteServer)

print("Give the range of ports you want to scan separate by space")
start = int(input("Enter start port number >>> "))
end = int(input("Enter end port number >>> "))

print("*****" * 10)
print(f"Remote Server : {remoteServer} & Remote Server's IP: {remoteIP}")
print("Wait, Scanning is in process....")
print("*****" * 10)

# checking date and time scan started
time1 = datetime.now()

try:
    for port  in range(start, end):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex((remoteIP, port))
        print(f"[*] Scanning port number :{port} [*]")
        if result == 0:
            print(f"        |---> Port : {port} => Open")
            sock.close()
except KeyboardInterrupt:
    print(">>> Press Ctrl+C <<<")
    sys.exit()
except socket.gaierror:
    print("Hostname is not resolved successfully...")
    sys.exit()
except socket.error:
    print("Unable to establish connection with remote server....")
    sys.exit()

# checking time when scan stopped
time2 = datetime.now()

# taking difference between time1 and time2 to check time duration of scan
total_time = time2 - time1
print(f"Scan completed. It took :{total_time} ")
