import select
import socket
import sys
import datetime

bsize=1024

class ChatServerSelect(object):

    def __init__(self,host='localhost',port=50005,backlog=5):
        self.server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        self.server.bind((host,port))
        print 'chat_server_select listening on port %s, to exit type return'%port
        self.server.listen(backlog)

    def serve(self):
        input=[self.server,sys.stdin]
        running=True
        while running:
            try:
                inputready,outputready,exceptready=select.select(input,[],[],60)
            except select.error, e:
                print e
                break
            except socket.error, e:
                print e
                break
            
            if not inputready:
                print 'Server running... %s'%datetime.datetime.now()
    
            for s in inputready:
                if s==self.server:
                    client,address=self.server.accept()
                    input.append(client)
                    print 'Accepted connection from client:',address
                elif s==sys.stdin:
                    junk=sys.stdin.readline()
                    running=False
                    print 'Input %s from stdin, exiting!'%junk.strip('\n')
                elif s:
                    id=s.getpeername()
                    data=s.recv(bsize)
                    print '%s: %s'%(id,data)
                    if data:
                        for c in input:
                            if c != self.server and c != sys.stdin:
                                c.send('polymerjazz %s: %s'%(id,data))
                    else:
                        s.close()
                        print 'Server closed connection!'
                        input.remove(s)

        self.server.close()

if __name__=='__main__':
    if len(sys.argv)>1:
        port=int(sys.argv[1])

    ChatServerSelect().serve()
