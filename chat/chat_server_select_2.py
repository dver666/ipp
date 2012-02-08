import select
import socket
import sys
import datetime

host=''
port=50003

if len(sys.argv)>1:
    port = int(sys.argv[1])

backlog=5
size=1024

server=socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
server.bind((host,port))
print 'chat_server listening on port %s, to exit type return'% port
server.listen(backlog)

timeout=60
input=[server,sys.stdin]
running=True
while running:
    inputready,outputready,exceptready=select.select(input,[],[],timeout)
    if not inputready:  
        print 'Server running: %s'%datetime.datetime.now()

    for s in inputready:
        if s == server:
            client,address=server.accept()
            input.append(client)
            print 'accepted connection from',address
        elif s==sys.stdin:
            junk=sys.stdin.readline()
            running=False
            print 'Input %s from stdin, exiting.'%junk.strip('\n')
        elif s:
            id=s.getpeername()
            data=s.recv(size)
            print '%s: %s'%(id,data)
            if data:
                for c in input:
                    if c != server and c != sys.stdin:
                        print c
                        c.send('polymerjazz %s: %s' % (id, data))
            else:
                s.close()
                print 'Server closed connection'
                input.remove(s)

s.close()
