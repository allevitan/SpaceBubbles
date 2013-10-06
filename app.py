import os
from flask import Flask
from mongoengine import *
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

app = Flask(__name__)
MONGO_URL = os.environ.get('MONGOHQ_URL')

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
    app.register_blueprint(home)
    app.register_blueprint(static)

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
