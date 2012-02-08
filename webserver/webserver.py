import os
import socket
import sys

defaults=['127.0.0.1','8080']

mime_types={'.jpg':'image/jpg',\
            '.gif':'image/gif',\
            '.png':'image/png',\
            '.html':'text/html',\
            '.pdf':'application/pdf',}   

response={}

responses={100: ('Continue', 'Request received, please continue'),\
           101: ('Switching Protocols','Switching to new protocol; obey Upgrade header'),\
           200: ('OK', 'Request fulfilled, document follows'),\
           201: ('Created', 'Document created, URL follows'),\
           202: ('Accepted','Request accepted, processing continues off-line'),\
           203: ('Non-Authoritative Information', 'Request fulfilled from cache'),\
           204: ('No Content', 'Request fulfilled, nothing follows'),\
           205: ('Reset Content', 'Clear input form for further input.'),\
           206: ('Partial Content', 'Partial content follows.'),\
           300: ('Multiple Choices','Object has several resources -- see URI list'),\
           301: ('Moved Permanently', 'Object moved permanently -- see URI list'),\
           302: ('Found', 'Object moved temporarily -- see URI list'),\
           303: ('See Other', 'Object moved -- see Method and URL list'),\
           304: ('Not Modified','Document has not changed since given time'),\
           305: ('Use Proxy','You must use proxy specified in Location to access this ... resource.'),\
           307: ('Temporary Redirect','Object moved temporarily -- see URI list'),\
           400: ('Bad Request','Bad request syntax or unsupported method'),\
           401: ('Unauthorized','No permission -- see authorization schemes'),\
           402: ('Payment Required','No payment -- see charging schemes'),\
           403: ('Forbidden','Request forbidden -- authorization will not help'),\
           404: ('Not Found', 'Nothing matches the given URI'),\
           405: ('Method Not Allowed','Specified method is invalid for this server.'),\
           406: ('Not Acceptable', 'URI not available in preferred format.'),\
           407: ('Proxy Authentication Required', 'You must authenticate with ... this proxy before proceeding.'),\
           408: ('Request Timeout', 'Request timed out; try again later.'),\
           409: ('Conflict', 'Request conflict.'),\
           410: ('Gone','URI no longer exists and has been permanently removed.'),\
           411: ('Length Required', 'Client must specify Content-Length.'),\
           412: ('Precondition Failed', 'Precondition in headers is false.'),\
           413: ('Request Entity Too Large', 'Entity is too large.'),\
           414: ('Request-URI Too Long', 'URI is too long.'),\
           415: ('Unsupported Media Type', 'Entity body in unsupported format.'),\
           416: ('Requested Range Not Satisfiable','Cannot satisfy request range.'),\
           417: ('Expectation Failed','Expect condition could not be satisfied.'),\
           500: ('Internal Server Error', 'Server got itself in trouble'),\
           501: ('Not Implemented','Server does not support this operation'),\
           502: ('Bad Gateway', 'Invalid responses from another server/proxy.'),\
           503: ('Service Unavailable','The server cannot process the request due to a high load'),\
           504: ('Gateway Timeout','The gateway server did not receive a timely response'),\
           505: ('HTTP Version Not Supported', 'Cannot fulfill request.'),
}

response[200]="""HTTP/1.1 200 Okay
Server: localhost
Content-type: %s

%s
"""

response[301]="""HTTP/1.1 301 Moved
Server: localhost
Content-type: text/plain
Location: %s

moved
"""

response[401]="""HTTP/1.1 401 Unauthorized
Server: localhost
Content-type: text/plain
 
%s No permission -- see authorization schemes
"""

response[404]="""HTTP/1.1 404 Not Found
Server: localhost
Content-type: text/plain

%s Not found
"""

response[407]="""HTTP/1.1 407 Proxy Authentication Required
Server: localhost
Content-type: text/plain
 
%s You must authenticate with ... this proxy before proceeding
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
    s.bind((host,port))
    s.listen(5)
    return s

def listen(s):
    connection,client=s.accept()
    return connection.makefile('r+')

def get_request(stream):
    method=None
    while True:
        try:
            line=stream.readline()
            print line
        except IOError,e:
            print e
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
                output=os.popen('python '+path).read()
                return(200,'text/plain',output)

            return (200,get_mime(uri),get_file(path))
        if os.path.isdir(path):
            if(uri.endswith('/')):
                return (200,'text/html',list_directory(uri))
            else:
                return (301,uri+'/')
        else:
            return (404,uri)
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
        print 'shutting down...'
    server.close()
    #server serve
