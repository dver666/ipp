import re,sys
import urllib2
try:
    from urllib2 import Request,urlopen
    from urllib2 import URLError,HTTPError
    from urlparse import urlparse
except ImportError,e:
    print e

import datetime
print """time: %s"""%(datetime.datetime.now())
print '-'*10

def get_img(url):
    """get_img(url) lists and counts most of the images in a given HTML web page"""
    imgpat=re.compile(r'''< *img +src *= *["'](.+?)["'] *''',re.I)
    try:
        f=urllib2.urlopen(url)
    except IOError:
        sys.stderr.write("Can't connect to [%s]"%url)
        sys.exit(1)
    try:
        getu=f.geturl()
    except urllib.error.ContentTooShortError as msg:
        sys.stderr.write("The amount of downloaded data from url [%s] is less than expected amount.\nmessage: %s"%url,msg)
        sys.exit(1)
    contents=str(f.read())
    f.close()
    img=imgpat.findall(contents)
    total=0
    for i in img:
        total+=1
        print "Found [{%s}] image(s): [{%s}]"%(total,i)
        print "-"*(len(i)+2)
        return "Page [{0}] has [{1}] images(s)\n".format(getu,total)

import socket
timeout=10
socket.setdefaulttimeout(timeout)
url3='http://localhost:8080/server-status'
username='proxy'
password='test123'
realm='Proxy Test'

passman=urllib2.HTTPPasswordMgr()
passman.add_password(realm,url3,username,password)
authhandler=urllib2.HTTPDigestAuthHandler(passman)

try:
    proxy_support=urllib2.ProxyHandler({"http":"http://localhost:8080"})
except URLError,e:
    print 'error: ',e

opener=urllib2.build_opener(proxy_support,authhandler)
urllib2.install_opener(opener)

req=Request(url3)
try:
    handle=urllib2.urlopen(req)
    print handle.geturl()
    print '-'*10
    print handle.info()
    print '-'*10
except HTTPError,e:
    print e
    handle.close()

print get_img(handle.geturl())
