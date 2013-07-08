#file  :wsgiserver
#author:KelvinKuo
#date  :2013-05-17

import SocketServer
import socket # For gethostbyaddr()
from wsgiref.simple_server import WSGIRequestHandler
from wsgiref.simple_server import ServerHandler
from util import sw_log
import errno

class sw_WSGIServer(SocketServer.TCPServer):
    """sw_WSGIServer that implements the Python WSGI protocol"""

    application = None
    allow_reuse_address = 1    # Seems to make sense in testing environment

    def __init__(self,addr,**kargs):

        SocketServer.TCPServer.__init__(self,addr,sw_WSGIRequestHandler)

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

    def _handle_request_noblock(self):
        """Handle one request, without blocking.

        fix the exception handle func
        """
        try:
            request, client_address = self.get_request()
        except socket.error:
            return
        if self.verify_request(request, client_address):
            try:
                self.process_request(request, client_address)
            except IOError as e:
                if e.errno != errno.EPIPE:
                    self.handle_error(request, client_address)
                self.close_request(request)
            except:
                self.handle_error(request, client_address)
                self.close_request(request)

class sw_WSGIRequestHandler(WSGIRequestHandler):

    def handle(self):
        """Handle a single HTTP request"""

        self.raw_requestline = self.rfile.readline()
        if not self.parse_request(): # An error code has been sent, just exit
            return

        handler = sw_ServerHandler(
            self.rfile, self.wfile, self.get_stderr(), self.get_environ()
        )
        handler.request_handler = self      # backpointer for logging
        handler.run(self.server.get_app())

    def log_message(self, format, *args):

        sw_log("%s %s" %(self.address_string(),format%args))

class sw_ServerHandler(ServerHandler):
    """sw_Serverhandler fix the bug of ServerHandler in func finish_response

    it iterator every char of the string 'self.result'
    """

    def finish_response(self):
        try:
            if not self.result_is_file() or not self.sendfile():
                if isinstance(self.result, basestring):
                    self.write(self.result)
                else:
                    for data in self.result:
                        self.write(data)
                self.finish_content()
        except IOError as e:
            if e.errno == errno.EPIPE:
                sw_log("Browser closed")
        finally:
            self.close()