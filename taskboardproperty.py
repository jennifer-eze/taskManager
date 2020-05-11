from google.appengine.ext import ndb


class TaskBoardProperty(ndb.Model):
    tb_name = ndb.StringProperty()
    tb_id = ndb.StringProperty()