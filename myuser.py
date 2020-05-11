from google.appengine.ext import ndb
from taskboardproperty import TaskBoardProperty


class MyUser(ndb.Model):
    email = ndb.StringProperty()
    myuser_board = ndb.StructuredProperty(TaskBoardProperty, repeated=True)