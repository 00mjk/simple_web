#file  :util
#author:KelvinKuo
#date  :2013-05-15

import datetime

def sw_log(msg,disk=False):
    """
    log api,print to the screen or store on disk
    """
    if not disk:
        print('[%s]%s'%(datetime.datetime.today(),msg))

def sw_err_print(msg,disk=False):
    """
    print error msg
    """
    if not disk:
        print('[%s]ERROR:%s'%(datetime.datetime.today(),msg))

def sw_request(request):
    """
    analyze the raw http request,get the method and request url
    """
    #get method and url
    method=request.split('\n')[0].split(' ')[0]
    url=request.split('\n')[0].split(' ')[1]

    return method,url

def sw_response(webpage):
    """
    make webpage(html) to a http msg
    """
    http ="""
HTTP/1.0 200 OK
Server: BWS/1.0
Content-Length: %d
Content-Type: text/html;charset=utf-8
Cache-Control: private

%s
"""%(len(webpage),webpage)

    return http

def sw_html_escape(string):
    """
    Escape HTML special characters ``&<>`` and quotes ``'"``.
    """
    return string.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')\
    .replace('"','&quot;').replace("'",'&#039;')

def sw_tob(s, enc='utf8'):
    return s.encode(enc) if isinstance(s, unicode) else bytes(s)