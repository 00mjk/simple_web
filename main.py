#file  :main
#author:KelvinKuo
#date  :2013-05-14

#python main.py 'host' 'port' launch the website

import sys
import socket
from util import sw_log
from util import sw_request
from util import sw_response

if __name__ == '__main__':
    #wellcome
    sw_log('simple_web a handmade website,enjoy the building by hand!')
    #get the args
    host=sys.argv[1]
    port=sys.argv[2]

    #try
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((host, int(port)))
    s.listen(10)
    #catch
    #exception

    sw_log('listening at host:%s port:%s'%(host,port))

    while True:
        conn, sockname = s.accept()
        sw_log('a connection accepted from %s:%s'%(sockname[0],sockname[1]))

        msg=conn.recv(2048)
        if len(msg) > 0:
            #get request header
            method,url=sw_request(msg)
            sw_log('method:%s url:\'%s\''%(method,url))
            #response the request
            webpage=''
            if url == '/aaa':
                webpage='<html><h1>aaa</h1></html>'
            else:
                webpage='<html><h1>Hello World</h1></html>'
            conn.sendall(sw_response(webpage))
        conn.close()
