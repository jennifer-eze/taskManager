import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
import os


from myuser import MyUser
from task import Task
from taskboard import TaskBoard
from new_tb import NewTaskBoard
from viewTaskBoard import ViewTaskBoard
#import random
from taskboardproperty import TaskBoardProperty
from addTask import AddTask


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)

class DeleteUser(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'

        boardId = self.request.get('id')

        user = users.get_current_user()
        myuser_key = ndb.Key('MyUser', user.email())
        myuser = myuser_key.get()


        getBoard = TaskBoard.get_by_id(boardId)
        board_name = getBoard.tb_name
        board_members = getBoard.tb_member


        template_values = {
            'myuser' : myuser,
            'board_name': board_name,
            'board_id' : boardId,
            'board_members': board_members
        }

        template = JINJA_ENVIRONMENT.get_template('delete_user.html')
        self.response.write(template.render(template_values))


    def post(self):
        boardId = self.request.get('id') 

        getBoard = TaskBoard.get_by_id(boardId)

        board_name = getBoard.tb_name

        board_members = getBoard.tb_member

        board_tasks = list(getBoard.tb_task)

        

        user = users.get_current_user()
        myuser_key = ndb.Key('MyUser', user.email())
        myuser = myuser_key.get()

        action = self.request.get('button')

        if action == 'remove_user':
            selected_user = self.request.get('selected_user')

            getUser = MyUser.get_by_id(selected_user)

            userBoards = getUser.myuser_board

            if (userBoards == selected_user):
                self.redirect('/')


            for a in board_members:
                if(selected_user == a):
                    board_members.remove(a)
                    getBoard.put()

            for b in list(userBoards):
                if(b.tb_name == board_name):
                    userBoards.remove(b)
                    getUser.put()

            for i in board_tasks:
                if(i.assigned_user == selected_user):
                    i.assigned_user = 'unassigned'
                    getBoard.put()
            
                
            self.redirect('/view_board?id=' + boardId)

        
        elif action == 'cancel':
            self.redirect('/view_board?id='+ boardId)

        template_values = {
            'myuser' : myuser,
            'board_id' : boardId,
            'board_members': board_members
        }


        template = JINJA_ENVIRONMENT.get_template('delete_user.html')
        self.response.write(template.render(template_values))



