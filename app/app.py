import os
from urlparse import urlparse
from flask import Flask
from pymongo import Connection
 
app = Flask(__name__)
MONGO_URL = os.environ.get('MONGOHQ_URL')
 
if MONGO_URL:
  # Get a connection
  connection = Connection(MONGO_URL)
  # Get the database
  db = connection[urlparse(MONGO_URL).path[1:]]
  app.debug = False
else:
  # Not on an app with the MongoHQ add-on, do some localhost action
  connection = Connection('localhost', 27017)
  db = connection['MyDB']
  app.debug = True
 
@app.route('/')
def hello():
  myObj = db.analytics.find_one({'event':'page_views'})
  if not myObj:
    myObj = {'event':'page_views', 'count':1}
  else:
    myObj['count'] += 1
  db.analytics.save(myObj)
  return 'Hello World! ' + str(myObj['count'])
 
if __name__ == '__main__':
  # Bind to PORT if defined, otherwise default to 5000.
  port = int(os.environ.get('PORT', 5000))
  app.run(host='0.0.0.0', port=port)
