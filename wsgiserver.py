#file  :wsgiserver
#author:KelvinKuo
#date  :2013-05-17

from BaseHTTPServer import HTTPServer

class sw_WSGIServer(HTTPServer):

    """BaseHTTPServer that implements the Python WSGI protocol"""

    application = None

    def __init__(self,addr,**kargs):
        from wsgiref.simple_server import WSGIRequestHandler
        HTTPServer.__init__(self,addr,WSGIRequestHandler)

    def server_bind(self):
        """Override server_bind to store the server name."""
        HTTPServer.server_bind(self)
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
