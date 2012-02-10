"""Python 3 recho_client"""
import socket
import sys
host='localhost'
port=47648
size=16384
client=None
nargs=len(sys.argv)
if nargs>1:
    host=sys.argv[1]
if nargs>2:
    port=int(sys.argv[2])
try:
    client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client.connect((host,port))
    print('Connection accepted by (%s,%s)'%(host,port))
    print('Client info:',client)
except socket.error as msg:
    print('Socket error was:',msg)
    client.close()
    client=None

if client is None:
    print("Could not open socket, check socket constructor")
    sys.exit(1)

while True:
    msg=input('recho_client> ')
    if msg:
        client.send(msg.encode())
        data=client.recv(size)
        print(data.decode())
    else:
        client.close()
        break
