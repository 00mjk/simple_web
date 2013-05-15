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