# encoding=utf8
import cherrypy
import os
import json
from my_sql import find_all_names, find_name_info
from aggregates import find_name_info_with_cobirths


class GameOfThrones(object):
    @cherrypy.expose
    def index(self):
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
          <div id = "characterDiv"></div>
          <div id = "yearDiv"><input type="number" id="yearValue" /></div>
          <script src="/static/scripts/script.js"></script>
          </body>
        </html>
        """
    @cherrypy.expose
    def character_list(self):
    	name_list = find_all_names()
    	return json.dumps(name_list)
    @cherrypy.expose
    def character_info(self, character_id, year_gap):
		if year_gap == '':
			character_values = find_name_info(character_id)
		else:
			character_values = find_name_info_with_cobirths(character_id, year_gap)
		return json.dumps(character_values)


if __name__ == '__main__':
    conf = {
        '/': {
            'tools.sessions.on': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd())
        },
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './public'
        }
    }
    cherrypy.config.update({'server.socket_host': '0.0.0.0',
							'server.socket_port': 80,
                            'tools.proxy.on': True
            })
    cherrypy.quickstart(GameOfThrones(), '/', conf);
