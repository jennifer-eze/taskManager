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
from addTask import AddTask


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)

class EditTask(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'

        boardId = self.request.get('id')
        taskName = self.request.get('task_name')

        user = users.get_current_user()
        myuser_key = ndb.Key('MyUser', user.email())
        myuser = myuser_key.get()

        old_task_name = ''
        old_deadline = ''
        old_assigned_user = ''

        getBoard = TaskBoard.get_by_id(boardId)
        board_tasks = getBoard.tb_task
        board_members = getBoard.tb_member

        name_of_board = getBoard.tb_name
        creator = getBoard.creator

        for a in board_tasks:
            if(a.task_name == taskName):
                old_task_name = a.task_name
                old_deadline = a.deadline
                old_assigned_user = a.assigned_user


        template_values = {
            'myuser' : myuser,
            'board_name': name_of_board,
            'creator' : creator,
            'board_id' : boardId,
            'board_members': board_members,
            'old_task_name' : old_task_name,
            'old_deadline' : old_deadline,
            'old_assigned_user' : old_assigned_user,
            'task_name' : taskName
            #'task_id' :taskId
        }

        template = JINJA_ENVIRONMENT.get_template('editTask.html')
        self.response.write(template.render(template_values))


    def post(self):
        boardId = self.request.get('id')
        task_name = self.request.get('task_name')

        getBoard = TaskBoard.get_by_id(boardId)
        board_members = getBoard.tb_member

        tasks = getBoard.tb_task

        

        error = ''

        

        action = self.request.get('button')


        if  action == 'update':
            newtaskName = self.request.get('new_task_name')
            Deadline = self.request.get('deadline')
            assignedUser = self.request.get('assigned_user')

            # for i in getBoard.tb_task:
            #     if(i.task_name == task_name):
            #         i.task_name = newtaskName
            #         i.deadline = Deadline
            #         i.assigned_user = assignedUser
            #         getBoard.put()
            #         self.redirect('/')

            existingNames = []

            for i in getBoard.tb_task:
                existingNames.append(i.task_name)

            for i in list(getBoard.tb_task):
                if (i.task_name == task_name):
                    if(newtaskName == task_name):
                        i.task_name = newtaskName
                        i.deadline = Deadline
                        i.assigned_user = assignedUser
                        getBoard.put()
                        self.redirect('/view_board?id=' + boardId)
                    elif(newtaskName != task_name):
                        if(newtaskName in existingNames):
                            error = 'Task Name exists'
                        else:
                            i.task_name = newtaskName
                            i.deadline = Deadline
                            i.assigned_user = assignedUser
                            getBoard.put()
                            self.redirect('/view_board?id=' + boardId)

        if action == 'cancel':
            self.redirect('/view_board?id=' + boardId)


        template_values = {
            'error' : error,
            'board_members' :board_members
        }

        template = JINJA_ENVIRONMENT.get_template('editTask.html')
        self.response.write(template.render(template_values))



