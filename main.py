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
from invite import InviteUser
from addTask import AddTask
from editTask import EditTask
from delete_user import DeleteUser
from rename_board import RenameTaskBoard


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)


class MainPage(webapp2.RequestHandler):
    # defines the get method
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'


        # welcome messages
        url = ''
        url_string = ''
        welcome = 'Welcome back'


        user = users.get_current_user()

        if user:
            url = users.create_logout_url(self.request.uri)
            url_string = 'logout'
            email = user.email()


            myuser_key = ndb.Key('MyUser', user.email())
            myuser = myuser_key.get()


            if myuser == None:
                welcome = 'Welcome to the application'
                myuser = MyUser(id=user.email())
                myuser.email = user.email()
                myuser.put()

        else:
            url = users.create_login_url(self.request.uri)
            url_string = 'login'
    

        template_values = {
            'url' : url,
            'url_string' : url_string,
            'user' : user,
            'welcome' : welcome
        }


        template = JINJA_ENVIRONMENT.get_template('main.html')
        self.response.write(template.render(template_values))


# starts the web applivation we specify the full routing table here as well
app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/task', Task),
    ('/taskboard', TaskBoard),
    ('/new_tb', NewTaskBoard),
    ('/view_board', ViewTaskBoard),
    ('/invite', InviteUser),
    ('/addTask', AddTask),
    ('/editTask', EditTask),
    ('/deleteUser', DeleteUser),
    ('/renameBoard', RenameTaskBoard)
], debug=True)