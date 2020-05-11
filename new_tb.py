import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb


import os


from myuser import MyUser
from taskboard import TaskBoard
from task import Task
from taskboardproperty import TaskBoardProperty
import random


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)


class NewTaskBoard(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'


        user = users.get_current_user()
        myuser_key = ndb.Key('MyUser', user.email())
        myuser = myuser_key.get()

        template_values = {
            'myuser' : myuser
            #'create_tb' : create_tb
        }


        template = JINJA_ENVIRONMENT.get_template('new_tb.html')
        self.response.write(template.render(template_values))


    def post(self):
        self.response.headers['Content-Type'] = 'text/html'

        user = users.get_current_user()
        myuser_key = ndb.Key('MyUser', user.email())
        myuser = myuser_key.get()

        action = self.request.get('button')


        if  action == 'Create':
            new_board_name = self.request.get('tb_name')

            id = str(random.randint(0,1000000))

            newBoard = TaskBoardProperty(tb_name = new_board_name, tb_id = id)
            myuser.myuser_board.append(newBoard)
            myuser.put()

            new_entry = TaskBoard(id= id, tb_name = new_board_name, creator = myuser.email)
            new_entry.tb_member.append(myuser.email)
            new_entry.put()

            self.redirect('/new_tb')