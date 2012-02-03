import socket
import sys
import select
import datetime

def prompt():
    sys.stdout.write('> ')
    sys.stdout.flush()

host='localhost' 
port=50003
size=1024

nargs=len(sys.argv)
if nargs>1:
    host=sys.argv[1]
if nargs>2:
    port=int(sys.argv[2])

server=socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
server.connect((host,port)) 
print 'Connection accepted by (%s,%s)'%(host, port)
prompt()

timeout=60
input=[server, sys.stdin]
running=True
while running:
    inputready,outputready,exceptready=select.select(input,[],[],timeout)
    if not inputready:
        print 'chat client running at %s'%datetime.datetime.now()
        prompt()

    for s in inputready:
        if s==sys.stdin:
            msg=sys.stdin.readline().strip('\n')
            if msg:
                server.send(msg) 
            else:
                server.close() 
                running=False
        elif s:
            data=server.recv(size)
            print data
            prompt()
