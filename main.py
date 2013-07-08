#file  :main
#author:KelvinKuo
#date  :2013-05-14

#python main.py 'host' 'port' launch the website

import sys
from util import sw_log
from util import sw_err_print
import simple_web
from wsgiapp import route
from wsgiapp import sw_Resource
from wsgiapp import sw_Form

@route("/")
def route_index(environ):
    return sw_Resource.get_res_path("index.html")

@route("/index")
def route_welcome(environ):
    return sw_Resource.get_res_path("index.html")

@route("/login")
def route_login(environ):
    name = sw_Form.get(environ,"name")
    pwd = sw_Form.get(environ,"pass")

    if not name or name == "": return "please input name"
    return sw_Resource.get_res_path("login.html").replace("""<%name%>""",name)

@route("default")
def route_default(environ):
    return sw_Resource.get_res_path("error404.html")

if __name__ == '__main__':
    #wellcome
    sw_log('simple_web a handmade website,enjoy the building by hand!')
    #get the args

    host = "0.0.0.0" if len(sys.argv) < 3 else sys.argv[1]
    port = "80" if len(sys.argv) < 3 else sys.argv[2]

    simple_web.run(_app='simple_web_app',_server='simple_web_server',_host=host,_port=port)

