import socket 
import sys
page="""HTTP/1.0 200 OK
Content-Type text/html

<html>
<body>
echo_www: %s
</body>
</html>
"""
host='' 
port=8082 
if len(sys.argv)>1:
    port=int(sys.argv[1])
backlog=5
size=1024
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
s.bind((host,port)) 
print 'echo_www listening on port:',port
s.listen(backlog) 
while True:
    try:
        client,address=s.accept()
        req=client.recv(size)
        string=req.split()
        path=string[1]
        client.send(page%path)
        client.close()
    except KeyboardInterrupt,e:
        print 'Received keyboard interrupt! Shutting down the server...'
        client.close()
        s.close()
        sys.exit(0)
