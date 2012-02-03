"""
echo server, usage:

python echo_server.py <port>

Port is optional, default: 50000
"""

import socket
import sys

host=''
port=50000

if len(sys.argv)>1:
    port=int(sys.argv[1])

backlog=5
size=1024

s=socket.socket(socket.AF_INET6,socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
s.bind((host,port))
print 'echo_server listening on port',port
s.listen(backlog)

while True:
    client,address=s.accept()
    data=client.recv(size)
    if data:
        client.send('polymerjazz: %s'%data)
    print 'from %s: %s'%(address,data)
    client.close()

# main loop of the web server will look similar to this
# there are 3 ways in which this loop could work:
# -dispatching a thread to handle clientsocket
# -create a new process to handle clientsocket
# -use non-blocking sockets to multiplex between our server socket and
# any active clientsockets using select.
# while True:
#    # accept connections from outside
#    (clientsocket,address)=serversocket.accept()
#    # handle client socket threads
#    # thus, we pretend it is a threaded server
#    ct=client_thread(clientsocket)
#    ct.run()
