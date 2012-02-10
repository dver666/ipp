import os
import socket
import sys
import datetime
defaults=['','8080']
mime_types={'.jpg':'image/jpg',\
            '.gif':'image/gif',\
            '.png':'image/png',\
            '.html':'text/html',\
            '.pdf':'application/pdf'}
response={}
response[200]="""HTTP/1.1 200 OK
Server: webserver
Content-type: %s

%s
"""
response[301]="""HTTP/1.1 301 Moved
Server: webserver
Content-type: text/plain
Location: %s

moved
"""
response[404]="""HTTP/1.1 404 Not Found
Server: webserver
Content-type: text/plain

%s Nothing matches the given URI
"""
response[501]="""HTTP/1.1 501 Not Implemented
Server: webserver
Content-type: text/plain

%s Server does not support this operation
"""
DIRECTORY_LISTING="""<html>
<head><title>%s</title></head>
<body>
<a href="%s..">..</a><br>
%s
</body>
</html>
"""
DIRECTORY_LINE='<a href="%s">%s</a><br>'
def server_socket(host,port):
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    s.bind((host,port))
    s.listen(1)
    return s

def listen(s):
    connection,client=s.accept()
    return connection.makefile('r+')

def get_request(stream):
    method=None
    while True:
        line=stream.readline()
        print line
        if not line.strip(): 
            break
        elif not method: 
            method,uri,protocol=line.split()
    return uri

def list_directory(uri):
    entries=os.listdir('.'+uri)
    entries.sort()
    return DIRECTORY_LISTING % (uri,uri,'\n'.join([DIRECTORY_LINE % (e,e) for e in entries]))

def get_file(path):
    f=open(path)
    try:
        return f.read()
    except IOError,e:
        print e
        sys.exit(1)
    finally: 
        f.close()

def get_content(uri):
    print 'fetching:',uri
    try:
        path='.'+uri
        if uri.endswith('date.html'):
            return(200,'text/plain','localhost: %s'%datetime.datetime.now())
        if os.path.isfile(path):
            if path.endswith('.py'):
                try:
                    output=os.popen('python '+path).read()
                    return(200,'text/plain',output)
                except IOError,e:
                    print e
                    sys.exit(1)

            return (200,get_mime(uri),get_file(path))
        if os.path.isdir(path):
            if(uri.endswith('/')):
                return (200,'text/html',list_directory(uri))
            else:
                return (301,uri+'/')
        else:
            return (404,uri)
    except NameError,e:
        f=str(e)
        print 'Missing module name:',f.split()[2]
        return (501,e)  
    except IOError,e:
        return (404,e)

def get_mime(uri):
    return mime_types.get(os.path.splitext(uri)[1],'text/plain')

def send_response(stream, content):
    stream.write(response[content[0]]%content[1:])

if __name__ == '__main__':
    args,nargs=sys.argv[1:],len(sys.argv)-1
    host,port=(args+defaults[-2+nargs:])[0:2]
    server=server_socket(host,int(port))
    print 'starting %s on %s...'%(host,port)
    try:
        while True:
            stream=listen(server)
            send_response(stream,get_content(get_request(stream)))
            stream.close()
    except KeyboardInterrupt:
        print 'Received keyboard interrupt! Shutting down the server...'
    server.close()
