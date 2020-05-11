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


class InviteUser(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'

        boardId = self.request.get('id')

        user = users.get_current_user()
        myuser_key = ndb.Key('MyUser', user.email())
        myuser = myuser_key.get()

        getBoard = TaskBoard.get_by_id(boardId)

        name_of_board = getBoard.tb_name
        creator = getBoard.creator

        allUsers = MyUser.query().fetch()

        template_values = {
            'myuser' : myuser,
            'board_name': name_of_board,
            'creator' : creator,
            'users' :allUsers,
            'board_id' : boardId
        }


        template = JINJA_ENVIRONMENT.get_template('invite.html')
        self.response.write(template.render(template_values))


    def post(self):
        self.response.headers['Content-Type'] = 'text/html'

        user = users.get_current_user()
        myuser_key = ndb.Key('MyUser', user.email())
        myuser = myuser_key.get()

        board_id = self.request.get('id')

        invited_user = self.request.get('invited_user')

        getBoard = TaskBoard.get_by_id(board_id)
        board_name = getBoard.tb_name

        get_member = MyUser.get_by_id(invited_user)

        action = self.request.get('button')


        if  action == 'invite':
            
            
            newMember = TaskBoardProperty(tb_name = board_name, tb_id = board_id)
            get_member.myuser_board.append(newMember)
            get_member.put()

            getBoard.tb_member.append(invited_user)
            getBoard.put()

            self.redirect('/')
        
        elif action == 'cancel':
            self.redirect('/view_board?id='+ board_id)