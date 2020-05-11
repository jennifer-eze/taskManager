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
import random
from taskboardproperty import TaskBoardProperty


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)

class AddTask(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'

        boardId = self.request.get('id')
        #taskId = self.request.get('id')

        user = users.get_current_user()
        myuser_key = ndb.Key('MyUser', user.email())
        myuser = myuser_key.get()

        getBoard = TaskBoard.get_by_id(boardId)
        board_members = getBoard.tb_member

        name_of_board = getBoard.tb_name
        creator = getBoard.creator

        template_values = {
            'myuser' : myuser,
            'board_name': name_of_board,
            'creator' : creator,
            'board_id' : boardId,
            'board_members': board_members
            #'task_id' :taskId
        }

        template = JINJA_ENVIRONMENT.get_template('addTask.html')
        self.response.write(template.render(template_values))


    def post(self):
        self.response.headers['Content-Type'] = 'text/html'

        boardId = self.request.get('id')

        getBoard = TaskBoard.get_by_id(boardId)
        board_members = getBoard.tb_member

        action = self.request.get('button')

        error = ''


        if  action == 'addTask':
            taskName = self.request.get('task_name')
            Deadline = self.request.get('deadline')
            assignedUser = self.request.get('assigned_user')

            existingNames = []

            for a in getBoard.tb_task:
                existingNames.append(a.task_name)


            if(taskName in existingNames):
                error = 'task name exists'
            else:
                new_task = Task(task_name = taskName, deadline = Deadline, completed = 'No', assigned_user = assignedUser, date_completed = '', time_completed ='')
                getBoard.tb_task.append(new_task)
                getBoard.put()
                self.redirect('/view_board?id='+ boardId)

        elif action == 'cancel':
            self.redirect('/view_board?id='+ boardId)


            template_values = {
            'error' : error,
            'board_members' :board_members
            }

            template = JINJA_ENVIRONMENT.get_template('addTask.html')
            self.response.write(template.render(template_values))



