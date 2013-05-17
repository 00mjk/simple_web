#file  :simple_web
#author:KelvinKuo
#date  :2013-05-17

from wsgiserver import sw_WSGIServer
from wsgiapp import sw_WSGIApp

server_names={
    'simple_web_server':sw_WSGIServer
}

application_names={
    'simple_web_app':sw_WSGIApp
}

def run(_app='simple_web_app', _server='simple_web_server', _host='127.0.0.1', _port=8080):
        #,interval=1, reloader=False, quiet=False, plugins=None,debug=False, **kargs):
    """
    launch the whole website
    """

    try:
        if _app in application_names:
            app = application_names.get(_app)
            if isinstance(app,type): app = app()
            if not callable(app):
                raise ValueError("Application is not callable: %r" % _app)
        else:
            raise ValueError("Application is not supplied" % _app)
        #for plugin in plugins or []:
        #    app.install(plugin)

        if _server in server_names:
            server = server_names.get(_server)
            if isinstance(server,type): server = server()
        else:
            raise ValueError("Server is not supplied: %s" % _server)

        server.setup(_host,_port)
        server.run(app)

    except KeyboardInterrupt:
        pass
    except (SystemExit, MemoryError):
        raise