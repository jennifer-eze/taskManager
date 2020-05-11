from google.appengine.ext import ndb
from task import Task


class TaskBoard(ndb.Model):
    #tb_id = ndb.IntegerProperty()
    tb_name = ndb.StringProperty()
    creator = ndb.StringProperty()
    tb_member = ndb.StringProperty(repeated=True)
    tb_task = ndb.StructuredProperty(Task, repeated=True)