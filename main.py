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


@route("/")
def route_index(path):
    return sw_Resource.get_res_path("welcome.html")

@route("/welcome")
def route_welcome(path):
    return sw_Resource.get_res_path("welcome.html")

#@route("/result")
#def route_result():
#    return sw_Resource.get_resource_file("result.html")

@route("default")
def route_default(path):
    return sw_Resource.get_res_path("error404.html")

if __name__ == '__main__':
    #wellcome
    sw_log('simple_web a handmade website,enjoy the building by hand!')
    #get the args

    host = "127.0.0.1" if len(sys.argv) < 3 else sys.argv[1]
    port = "80" if len(sys.argv) < 3 else sys.argv[2]

    simple_web.run(_app='simple_web_app',_server='simple_web_server',_host=host,_port=port)

