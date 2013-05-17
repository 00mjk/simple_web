#file  :wsgiserver
#author:KelvinKuo
#date  :2013-05-17

class sw_WSGIServer(object):

    def setup(self,_host,_port):
        self.host=_host
        self.port=int(_port)

    def run(self, app): # pragma: no cover
        from wsgiref.simple_server import make_server
        srv = make_server(self.host, self.port, app)
        srv.serve_forever()
