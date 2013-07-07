#file  :wsgiapp
#author:KelvinKuo
#date  :2013-05-17

from util import sw_html_escape
from util import sw_tob
from util import sw_log
from util import sw_err_print

import sys
import os
#######################
# application for WSGI
#######################
class sw_WSGIApp(object):
    """
    callable as a WSGI application
    """
    def __init__(self):
        sw_Resource.setup()
        self.response_status = "200 OK"
        self.response_head = [
            ('Content-type', 'text/html;charset=utf-8'),
            ('Server', 'simple_web/0.1')
        ]

    def __call__(self, environ, start_response):
        """
        Each instance of :class:'sw_WSGIApp' is a WSGI application.
        """
        return self.wsgi(environ, start_response)

    def wsgi(self, environ, start_response):
        """
        The WSGI-interface.
        """
        sw_log('%s:%s'%('PATH_INFO',environ['PATH_INFO']))
        try:
            path = self.get_path(environ)
            func = route_super(path)

            #
            start_response(self.response_status, self.response_head)
            return func(path)
        except (KeyboardInterrupt, SystemExit, MemoryError):
            raise
        except Exception:
            err = '<h1>Critical error while processing request: %s</h1>'\
                  % sw_html_escape(environ.get('PATH_INFO', '/'))

            environ['wsgi.errors'].write(err)
            headers = [('Content-Type', 'text/html; charset=UTF-8')]
            start_response('500 INTERNAL SERVER ERROR', headers, sys.exc_info())
            return [sw_tob(err)]

    def get_path(self, environ):
        """get request path from environ"""
        return environ['PATH_INFO']

#######################
# Resource Engine
# single thread
#######################
class sw_Resource(object):
    """a resource search engine"""

    res_list = []
    root = ""

    @classmethod
    def setup(cls):
        #load all static files
        #you can control which file to be seen here
        sw_log("building resource ...")
        cls.root = os.path.join(os.getcwd(),"resource")
        for root,dirs,cls.res_list in os.walk(cls.root): pass
        if len(cls.res_list) == 0: sw_err_print("no resources found")

    @classmethod
    def clear(cls):
        cls.res_list = []
        cls.root = ""

#    @classmethod
#    def get_res_fname(cls,fname):
#        if fname in cls.res_list:
#            return open(os.path.join(cls.root,fname)).read()
#        sw_err_print("%s not found" % fname)
#        return ""

    @classmethod
    def get_res_path(cls,path):
        path = path[1:] if path[0] == '/' else path
        if path in cls.res_list:
            return open(os.path.join(cls.root,path)).read()
        sw_err_print("%s not found" % path)
        return cls.get_res_path("error404.html")

#######################
# route
#######################
def route(path):
    """Decorator for route parse"""
    def _route(response_fun):
        routeMap.set_route(path,response_fun)
        def add_route(path):
            response_fun(path)
        return add_route
    return _route

def route_super(path):
    """top level route"""
    #static file
    resource = [".js",".JS",".css",".CSS",".html",".jpg",".png",".ico",".avi",".gif"]
    for i in resource:
        if i in path: return route_static

    #other route
    return routeMap.get_route(path)

def route_static(path):
    return sw_Resource.get_res_path(path)

class routeMap(object):

    routemap = {}

    @classmethod
    def set_route(cls,k,w):
        if not k or not w: return
        cls.routemap[k] = w

    @classmethod
    def get_route(cls,k):
        return cls.routemap[k] if k in cls.routemap else cls.routemap["default"]
