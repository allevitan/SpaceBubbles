import os
from flask import Flask
from mongoengine import *
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

app = Flask(__name__)
MONGO_URL = os.environ.get('MONGOHQ_URL')
app.config['SECRET_KEY'] = 'AJ592ej^9&srehgre034539jrgre'

if MONGO_URL:
  # Get a connection
  connect('spacebubbles', host=MONGO_URL)
  # Get the database
  app.debug = True #=False for demo
else:
  # Not on an app with the MongoHQ add-on, do some localhost action
  connect('spacebubbles',host='localhost', port=27017)
  app.debug = True

def register_blueprints(app):
    from blueprints.home import home
    from blueprints.static import static
    from blueprints.api import api
    from blueprints.signup import signup
    from blueprints.login import login
    from blueprints.logout import logout
    from blueprints.myspace import myspace
    from blueprints.my_graph import my_graph
    from blueprints.outer_space import outer_space
    from blueprints.expand import expand
    app.register_blueprint(home)
    app.register_blueprint(static)
    app.register_blueprint(api)
    app.register_blueprint(signup)
    app.register_blueprint(login)
    app.register_blueprint(logout)
    app.register_blueprint(myspace)
    app.register_blueprint(my_graph)
    app.register_blueprint(outer_space)
    app.register_blueprint(expand)

register_blueprints(app)

if __name__ == '__main__':

  #
  port = int(os.environ.get('PORT', 5000))

  #The tornado stuff
  http_server = HTTPServer(WSGIContainer(app))
  http_server.listen(port)
  IOLoop.instance().start()

  # Bind to PORT if defined, otherwise default to 5000.
  #app.run(host='0.0.0.0', port=port)
