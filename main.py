#file  :main
#author:KelvinKuo
#date  :2013-05-14

#python main.py 'host' 'port' launch the website

import sys
from util import sw_log
from util import sw_err_print
import simple_web

if __name__ == '__main__':
    #wellcome
    sw_log('simple_web a handmade website,enjoy the building by hand!')
    #get the args
    try:
        host=sys.argv[1]
        port=sys.argv[2]
    except:
        sw_err_print('please launch simple_web like "python main.py 127.0.0.1 80"')
        sys.exit()

    simple_web.run(_app='simple_web_app',_server='simple_web_server',_host=host,_port=port)

