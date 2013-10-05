import os
from urlparse import urlparse
from flask import Flask
from mongoengine import *
from app import models

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
  users =  models.User.objects
  if users:
    return users[0].name

if __name__ == '__main__':
  # Bind to PORT if defined, otherwise default to 5000.
  port = int(os.environ.get('PORT', 5000))
  app.run(host='0.0.0.0', port=port)
