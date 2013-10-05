from mongoengine import *

class Page(Document):
    slug = StringField(max_length=100)
    url = StringField(max_length=255)

class Site(Document):
    url = StringField(max_length=255)
    #favicon = ???
    title = StringField(max_length=100)
    score = IntField()
    pages = ListField(ReferenceField(Page))

class Space(Document):
    sites = ListField(ReferenceField(Site))

class User(Document):
    name = StringField(max_length=50)
    spaces = ListField(ReferenceField(Space))
    #friends = ???
    #Auth stuff??? Facebook?
    
class Comment(Document):
    author = ReferenceField(User)
    site = ReferenceField(Site)
