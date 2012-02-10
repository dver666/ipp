"""Python 3 recho_server"""
import socket
import sys
host=''
port=47648
s=None
if len(sys.argv)>1:
    port=int(sys.argv[1])
backlog=5
size=16384
try:
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    s.bind((host,port))
    print('recho_server listening on port:',port)
    s.listen(backlog)
except socket.error as msg:
    print('Socket error was:',msg)
    s.close()
    s=None

if s is None:
    print("Could not open socket, check socket constructor")
    sys.exit(1)

while True:
    try:
        client,address=s.accept()
        print('Accepted connection from client:',address)
        print('Client info:',client)
        while True:
            data=client.recv(size)
            if data:
                try:
                    client.send('recho_server> '.encode()+data)
                except TypeError as msg:
                    print(msg)
            else:
                client.close()
                print('Closed connection with client:',address)
                break
    except KeyboardInterrupt:
        print("Received Keyboard Interrupt Signal! Shutting down the server...")
        client.close()
        s.close()
        sys.exit(0)
