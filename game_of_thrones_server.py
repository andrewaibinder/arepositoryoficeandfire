# encoding=latin1
import cherrypy
import os
import json

from config import get_main_configurations
from cgi import escape
from sql import find_all_names, find_name_info
from log import log


def add_AC_BC(year):
    if type(year) == long:
        if year > 0:
            return "{} AC".format(year)
        elif year < 0:
            return "{} BC".format(year)
    return year


def born_express(start, end):
    start, end = add_AC_BC(start), add_AC_BC(end)
    if start == None and end == None:
        return "Unknown"
    elif start == None:
        return "At or before {}".format(end)
    elif end == None:
        return "At or after {}".format(start)
    if start == end:
        return start
    return "{} - {}".format(start, end)


def character_raw_to_html(data):
    if type(data) == list:
        html = """
            Name: {}
        <br>Gender: {}
        <br>House: {}
        <br>Born:  {}
        """.format(escape(data[0]), escape(data[1]),
                   "/".join([escape(house) for house in data[2]]),
                   born_express(data[3], data[4]))
    else:
        html = "No Data For This Character"
    return html


class GameOfThrones(object):
    @cherrypy.expose
    def index(self):
        log("New User")
        log(cherrypy.request.headers)
        return """
        <!DOCTYPE html>
        <html>
        <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
        <meta http-equiv="X-UA-Compatible" content="IE=edge" />
        <title>A Coding Project of Ice and Fire</title>
        <script src="/static/scripts/jquery.js"></script>
        <link rel="stylesheet" type="text/css" href="static/css/style.css">
        </head>
        <body>
        <div id="myModal" class="modal">
            <!-- Modal content -->
            <div class="modal-content">
                <span class="close">&times;</span>
                <p id = "modal_text"></p>
            </div>
        </div>
        <div id = "characterDiv"></div>
        <script src="/static/scripts/script.js"></script>
        </body>
        </html>
        """

    @cherrypy.expose
    def character_list(self):
        name_list = find_all_names()
        return json.dumps(name_list)

    @cherrypy.expose
    def character_info(self, character_id):
        log(character_id)
        character_values = find_name_info(character_id)
        log(character_values)
        character_html = character_raw_to_html(character_values)
        return json.dumps(character_html, encoding='latin1')


if __name__ == '__main__':
    configs = get_main_configurations()
    conf = {
        '/': {
            'tools.sessions.on': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd())
        },
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': configs['Public']
        }
    }
    cherrypy.config.update({'server.socket_host': configs['IP'],
                            'server.socket_port': configs['Port'],
                            'tools.proxy.on': True
                            })
    cherrypy.quickstart(GameOfThrones(), '/', conf)
