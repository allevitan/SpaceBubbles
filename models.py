from mongoengine import Document, StringField, FloatField, ImageField, ListField, ReferenceField
import datetime

class Page(Document):
    creation = DatetimeField(default=datetime.datetime.now, required=True)
    slug = StringField(max_length=100)
    url = StringField(max_length=255)
    author = ReferenceField('User')
    readby = ListField(ReferenceField('User'))

class Comment(Document):
    creation = DatetimeField(default=datetime.datetime.now, required=True)
    author = ReferenceField('User')
    site = ReferenceField('Node')

class Node(Document):
    creation = DatetimeField(default=datetime.datetime.now, required=True)
    url = StringField(max_length=255)
    favicon = ImageField()
    title = StringField(max_length=100)
    score = FloatField()
    pages = ListField(ReferenceField('Page'))
    comments = ListField(ReferenceField('Comment'))

class Space(Document):
    creation = DatetimeField(default=datetime.datetime.now, required=True)
    title = StringField(max_length=100)
    nodes = ListField(ReferenceField('Node'))

class User(Document):
    creation = DatetimeField(default=datetime.datetime.now, required=True)
    name = StringField(max_length=50)
    spaces = ListField(ReferenceField('Space'))
    friends = ListField(ReferenceField('User'))
    password = StringField(max_length=255)
    avatar = StringField()
