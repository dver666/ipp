#!/usr/bin/env python3
import cgi
import cgitb
cgitb.enable()
print("Content-Type: text/html")
print()
print("<html><head><title>QUIZ</title><link rel=icon type=image/png href=tml.png /></head><body bgcolor=#d8da3d></body></html>")
form=cgi.FieldStorage()
try:
    q1=form.getfirst("q1","").upper()
    q3=form.getfirst("q3","").upper()
    for value in form.getlist("value"):
        if isinstance(value,list):
            keys=list(form.keys())
            q2=form.getvalue("q2",keys)
            q4=form.getvalue("q4",keys)
    else:
        if "q1" not in form:
            raise KeyError
            pass
        print("<p>Q1 you selected: ",form["q1"].value)
        if "q2" not in form:
            raise KeyError
            pass
        print("<p>Q2 you selected: ",form.getvalue("q2"))
        if "q3" not in form:
            raise KeyError
            pass
        print("<p>Q3 you selected: ",form["q3"].value)
        if "q4" not in form:
            raise KeyError
            pass
        print("<p>Q4 you selected: ",form.getvalue("q4"))
except KeyError:
    try:
        from urllib.request import Request,urlopen
        from urllib.request import HTTPRedirectHandler
        from urllib.error import URLError,HTTPError
    except ImportError as e:
            print(e)
    print("<p>Please answer all question to submit. Redirecting back to Quiz page....")
except:
    cgitb.handler()
else:
    print("<p>No exceptions have been caught. Do math here")
finally:
    print("<p>finally block always executes,include code to clean up after any exception handling (closing files,resetting vars,and so on)")
#cgi.test()
