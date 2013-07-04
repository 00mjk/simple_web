#file  :wsgiserver
#author:KelvinKuo
#date  :2013-05-17

import SocketServer
import socket # For gethostbyaddr()

class sw_WSGIServer(SocketServer.TCPServer):
    """sw_WSGIServer that implements the Python WSGI protocol"""

    application = None
    allow_reuse_address = 1    # Seems to make sense in testing environment

    def __init__(self,addr,**kargs):
        from wsgiref.simple_server import WSGIRequestHandler
        SocketServer.TCPServer.__init__(self,addr,WSGIRequestHandler)

    def server_bind(self):
        """Override server_bind to store the server name."""
        SocketServer.TCPServer.server_bind(self)
        host, port = self.socket.getsockname()[:2]
        self.server_name = socket.getfqdn(host)
        self.server_port = port
        self.setup_environ()

    def setup_environ(self):
        # Set up base environment
        env = self.base_environ = {}
        env['SERVER_NAME'] = self.server_name
        env['GATEWAY_INTERFACE'] = 'CGI/1.1'
        env['SERVER_PORT'] = str(self.server_port)
        env['REMOTE_HOST']=''
        env['CONTENT_LENGTH']=''
        env['SCRIPT_NAME'] = ''

    def get_app(self):
        return self.application

    def set_app(self,application):
        self.application = application

    def run(self,app):
        self.set_app(app)
        self.serve_forever()
