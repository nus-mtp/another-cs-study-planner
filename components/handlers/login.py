'''
    Dummy handler for registration and logging in.
'''

from app import RENDER
import web
from components import model
import hashlib
import uuid

def create_login_form(self):
        '''
            Creates a 'Login' form that will appear on the webpage
        '''

        username_textbox = web.form.Textbox('username',
                                            web.form.notnull,
                                            description="Username")

        password_textbox = web.form.Password('password',
                                             web.form.notnull,
                                             description="Password")

        login_button = web.form.Button('Login',
                                       class_="btn btn-primary")

        login_form = web.form.Form(username_textbox,
                                   password_textbox,
                                   login_button)
        return login_form

## For login test
class Login(object):
    '''
        Class handles registration (put user in database)
        and login (verifying if user is in database)
    '''


    def __init__(self):
        model.CONNECTION.rollback()
        self.login_form = create_login_form(self)
        self.registration_form = self.create_registration_form()


    def GET(self):
        '''
            This function is called when /login is accessed.
        '''
        return RENDER.login(self.login_form, self.registration_form)


    def POST(self):
        '''
            This function is called when the register button is clicked.
            If both fields are not empty, admin is added.
        '''
        form = self.registration_form()
        
        # returns to page without creating
        if not form.validates(): 
            return RENDER.login(self.login_form, self.registration_form)
        else:
            salt = uuid.uuid4().hex
            hashed_password = hashlib.sha512(form.d.password + salt).hexdigest()
            model.add_admin(form.d.username, salt, hashed_password)
            raise web.seeother('/login')


    def create_registration_form(self):
        '''
            Creates a 'Register' form that will appear on the webpage
        '''

        username_textbox = web.form.Textbox('username',
                                            web.form.notnull,
                                            description="Username")

        password_textbox = web.form.Password('password',
                                             web.form.notnull,
                                             description="Password")

        register_button = web.form.Button('Register',
                                          class_="btn btn-info")

        registration_form = web.form.Form(username_textbox,
                                          password_textbox,
                                          register_button)
        return registration_form
    
class verifyLogin(object):
    def POST(self):
        '''
            This function is called when the login button is clicked.
            If both fields are empty, return to login page.
        '''
        form = create_login_form(self)
        # returns to login page
        if not form.validates(): 
            raise web.seeother('/login')
        else:
            # If valid admin, go to index
            is_valid = model.validate_admin(form.d.username, form.d.password)
            if is_valid:
                raise web.seeother('/')
            # Else go to error page
            else:
                raise web.seeother('/404')
            