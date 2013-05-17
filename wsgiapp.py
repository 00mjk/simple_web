#file  :wsgiapp
#author:KelvinKuo
#date  :2013-05-17

from util import sw_html_escape
from util import sw_tob
from util import sw_log
import sys
class sw_WSGIApp(object):
    """
    callable as a WSGI application
    """

    def wsgi(self, environ, start_response):
        """
        The WSGI-interface.
        """
        sw_log('%s:%s'%('PATH_INFO',environ['PATH_INFO']))
        try:
            start_response("200 OK", [
                ('Content-type', 'text/html;charset=utf-8'),
                ('Server', 'simple_web/0.1')
            ])
            return "<html><h1>Hello World</h1></html>"
        except (KeyboardInterrupt, SystemExit, MemoryError):
            raise
        except Exception:
            err = '<h1>Critical error while processing request: %s</h1>'\
                  % sw_html_escape(environ.get('PATH_INFO', '/'))

            environ['wsgi.errors'].write(err)
            headers = [('Content-Type', 'text/html; charset=UTF-8')]
            start_response('500 INTERNAL SERVER ERROR', headers, sys.exc_info())
            return [sw_tob(err)]

    def __call__(self, environ, start_response):
        """
        Each instance of :class:'sw_WSGIApp' is a WSGI application.
        """
        return self.wsgi(environ, start_response)
