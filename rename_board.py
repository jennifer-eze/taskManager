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


class RenameTaskBoard(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'

        boardId = self.request.get('id')

        user = users.get_current_user()
        myuser_key = ndb.Key('MyUser', user.email())
        myuser = myuser_key.get()


        getBoard = TaskBoard.get_by_id(boardId)

        board_name = getBoard.tb_name


        template_values = {
            'myuser' : myuser,
            'board_name': board_name,
            'board_id' : boardId
        }

        template = JINJA_ENVIRONMENT.get_template('rename_board.html')
        self.response.write(template.render(template_values))


    def post(self):
        new_board_name = self.request.get('new_board_name')

        boardId = self.request.get('id')

        getBoard = TaskBoard.get_by_id(boardId)
        board_name = getBoard.tb_name

        getAllUsers = MyUser.query().fetch()


        action = self.request.get('button')

        if action == 'rename':

            for a in list(getAllUsers):
                for b in list(a.myuser_board):
                    if(b.tb_name == board_name):
                        b.tb_name = new_board_name
                        a.put()

                        getBoard.tb_name = new_board_name
                        getBoard.put()
                        self.redirect('/view_board?id='+ boardId)


        elif action == 'cancel':
            self.redirect('/view_board?id='+ boardId)