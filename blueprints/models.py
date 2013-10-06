from mongoengine import Document, StringField, FloatField, ImageField, ListField, ReferenceField, DateTimeField, IntField
import datetime

class Page(Document):
    creation = DateTimeField(default=datetime.datetime.now, required=True)
    slug = StringField(max_length=100)
    url = StringField(max_length=255)
    author = ReferenceField('User')
    readby = ListField(ReferenceField('User'))

class Comment(Document):
    creation = DateTimeField(default=datetime.datetime.now, required=True)
    author = ReferenceField('User')
    site = ReferenceField('Node')

class Node(Document):
    creation = DateTimeField(default=datetime.datetime.now, required=True)
    url = StringField(max_length=255)
    favicon = ImageField()
    title = StringField(max_length=100)
    score = FloatField()
    pages = ListField(ReferenceField('Page'))
    comments = ListField(ReferenceField('Comment'))

class Space(Document):
    creation = DateTimeField(default=datetime.datetime.now, required=True)
    title = StringField(max_length=100)
    nodes = ListField(ReferenceField('Node'))

class User(Document):
    creation = DateTimeField(default=datetime.datetime.now, required=True)
    uid = IntField()
    salt = StringField(max_length=10)
    hashedpass = StringField()
    name = StringField(max_length=50)
    spaces = ListField(ReferenceField('Space'))
    friends = ListField(ReferenceField('User'))
    password = StringField(max_length=255)
    avatar = StringField()
