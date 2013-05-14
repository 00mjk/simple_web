#file  :main
#author:KelvinKuo
#date  :2013-05-14

#python main.py 'host' 'port' launch the website

import sys
import socket

if __name__ == '__main__':
    #wellcome
    print('\nsimple_web a handmade website,enjoy the building by hand!\n')
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

    print('listening at:\nhost:%s\nport:%s'%(host,port))

    while True:
        conn, sockname = s.accept()
        print('We have accepted a connection from %s:%s'%(sockname[0],sockname[1]))

        msg=conn.recv(2048)
        if len(msg) > 0:
            print(msg)
            #get request url
            pos1 = msg.find('GET /')+3
            pos2 = msg.find('HTTP/')-1
            if 0 <= pos1 < pos2:
                url=msg[pos1:pos2]
                print(url)
            #response the request
            webpage='<html>Hello World</html>'
            conn.sendall(
                """
HTTP/1.0 200 OK
Server: BWS/1.0
Content-Length: %d
Content-Type: text/html;charset=utf-8
Cache-Control: private

%s
                """%(len(webpage),webpage)
            )
        conn.close()
