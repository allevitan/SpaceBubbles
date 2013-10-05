import os
from urlparse import urlparse
from flask import Flask, render_template, send_from_directory
from mongoengine import *
from server import models

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


@app.route('/')
def hello():
  return render_template('home.html')

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static',filename)

if __name__ == '__main__':
  # Bind to PORT if defined, otherwise default to 5000.
  port = int(os.environ.get('PORT', 5000))
  app.run(host='0.0.0.0', port=port)
