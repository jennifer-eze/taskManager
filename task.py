from google.appengine.ext import ndb


class Task(ndb.Model):
    task_name = ndb.StringProperty()
    deadline = ndb.StringProperty()
    completed = ndb.StringProperty()
    assigned_user = ndb.StringProperty()
    time_completed = ndb.StringProperty()
    date_completed = ndb.StringProperty()