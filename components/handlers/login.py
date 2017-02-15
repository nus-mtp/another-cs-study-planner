'''
    Handler for registration and logging in.
'''

from app import RENDER
import web
from components import model

## For login test
class Login(object):
    '''
        Class handles registration (put user in database)
        and login (verifying if user is in database)
    '''

    def __init__(self):
        self.login_form = self.create_login_form()
        self.registration_form = self.create_registration_form()

    def GET(self):
        '''
            This function is called when /login is accessed.
        '''
        return RENDER.login(self.login_form, self.registration_form)

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
    