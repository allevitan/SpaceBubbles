from mongoengine import Document, StringField, FloatField, ImageField, ListField, ReferenceField

class Page(Document):
    slug = StringField(max_length=100)
    url = StringField(max_length=255)

class Comment(Document):
    author = ReferenceField('User')
    site = ReferenceField('Node')

class Node(Document):
    url = StringField(max_length=255)
    favicon = ImageField()
    title = StringField(max_length=100)
    score = FloatField()

    pages = ListField(ReferenceField('Page'))
    comment = ListField(ReferenceField('Comment'))

class Space(Document):
    nodes = ListField(ReferenceField('Node'))

class User(Document):
    name = StringField(max_length=50)
    spaces = ListField(ReferenceField('Space'))
    friends = ListField(ReferenceField('User'))
    password = StringField(max_length=255)
    avatar = StringField()
