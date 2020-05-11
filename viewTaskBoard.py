import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
import os
import datetime


from myuser import MyUser
from task import Task
from taskboard import TaskBoard
from new_tb import NewTaskBoard
#from editTask import EditTask
import random


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)


class ViewTaskBoard(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'

        boardId = self.request.get('id')

        user = users.get_current_user()
        myuser_key = ndb.Key('MyUser', user.email())
        myuser = myuser_key.get()
        email = myuser.email

        getBoard = TaskBoard.get_by_id(boardId)
        tasks= getBoard.tb_task

        name_of_board = getBoard.tb_name
        creator = getBoard.creator

        template_values = {
            'myuser' : myuser,
            'email':email,
            'board_name': name_of_board,
            'creator' : creator,
            'board_id' : boardId,
            'tasks' : tasks
        }


        template = JINJA_ENVIRONMENT.get_template('viewTaskBoard.html')
        self.response.write(template.render(template_values))


    def post(self):
        self.response.headers['Content-Type'] = 'text/html'
        user = users.get_current_user()
        myuser_key = ndb.Key('MyUser', user.user_id())
        myuser = myuser_key.get()
        action = self.request.get('button')

        current_time = datetime.datetime.now().strftime("%X")
        current_date = datetime.datetime.now().strftime("%x")


        
        
        if action == 'mark_task':
            boardId = self.request.get('id')

            task_name = self.request.get('task_name')

            getBoard = TaskBoard.get_by_id(boardId)

            tasks = getBoard.tb_task

            for a in list(tasks):
                if (task_name == a.task_name):
                    a.completed = 'Yes'
                    a.time_completed = current_time
                    a.date_completed = current_date
                    getBoard.put()


            self.redirect('/view_board?id=' + boardId)

        elif action == 'delete_task':
                boardId = self.request.get('id')

                task_name = self.request.get('task_name')

                getBoard = TaskBoard.get_by_id(boardId)

                tasks = getBoard.tb_task

                for n in tasks:
                    if (n.task_name == task_name):
                        tasks.remove(n)
                        getBoard.put()
                
                        self.redirect('/view_board?id=' + boardId)

        # elif action =='editTask':

        #         boardId = self.request.get('id')

        #         task_name = self.request.get('task_name')

        #         getBoard = TaskBoard.get_by_id(boardId)

        #         tasks = getBoard.tb_task

        #         for n in tasks:
        #             if (n.task_name == task_name): 
        #                 self.redirect('/ediTask?id=' + boardId)

        # elif action == 'remove_user':
        #         boardId = self.request.get('id')

        #         tb_name = self.request.get('tb_name')

        #         getBoard = TaskBoard.get_by_id(boardId)

        #         board_member = getBoard.tb_member

        #         for n in tasks:
        #             if (n.task_name == task_name):
        #                 tasks.remove(n)
        #                 getBoard.put()
                
        #                 self.redirect('/view_board?id=' + boardId)

        # elif action == 'rename':
        #     boardId = self.request.get('id')
        #     getBoard = TaskBoard.get_by_id(boardId)

        #     boardName = self.request.get('tb_name')

        #     if (boardName == )