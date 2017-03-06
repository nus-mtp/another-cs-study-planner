'''
    This module handles account registration and logging in.
'''

import hashlib
import uuid
from app import RENDER, SESSION
import web
from components import model


def create_login_form():
    '''
        Creates a 'Login' form that will appear on the webpage
    '''
    username_textbox = web.form.Textbox('username',
                                        web.form.notnull,
                                        post="<br><br>",
                                        description="Username")

    password_textbox = web.form.Password('password',
                                         web.form.notnull,
                                         post="<br><br>",
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
        self.login_form = create_login_form()
        self.registration_form = self.create_registration_form()


    def GET(self):
        '''
            This function is called when /login is accessed.
        '''
        login_form = self.login_form()
        registration_form = self.registration_form()
        if web.cookies().get('user') is None:
            return RENDER.login(login_form, registration_form, 0)
        else:
            return RENDER.login(login_form, registration_form, web.ctx.session._initializer['loginStatus'])


    def POST(self):
        '''
            This function is called when the register button is clicked.

            1) If both fields are empty, form will show error messages.
            2) If username is taken, an alert will indicate that username
               is taken.
            3) If all validations pass, the account is inserted into the database.
        '''
        login_form = self.login_form()
        registration_form = self.registration_form()

        # returns to page without creating
        if not registration_form.validates():
            return RENDER.login(login_form, registration_form)
        else:
            if model.is_userid_taken(registration_form.d.username):
                web.ctx.session._initializer['loginStatus'] = web.ACCOUNT_CREATED_UNSUCCESSFUL
            else:
                salt = uuid.uuid4().hex
                hashed_password = hashlib.sha512(registration_form.d.password
                                                 + salt).hexdigest()
                model.add_admin(registration_form.d.username, salt, hashed_password)
                web.ctx.session._initializer['id'] = web.ACCOUNT_CREATED_SUCCESSFUL

            raise web.seeother('/login')


    def create_registration_form(self):
        '''
            Creates a 'Register' form that will appear on the webpage
        '''
        username_validation_alphanumeric = web.form.regexp(
            r"^\w+$", 'Username should be alphanumeric.')

        username_textbox = web.form.Textbox('username',
                                            web.form.notnull,
                                            username_validation_alphanumeric,
                                            post="<br><br>",
                                            description="Username")

        password_textbox = web.form.Password('password',
                                             web.form.notnull,
                                             post="<br><br>",
                                             description="Password")

        register_button = web.form.Button('Register',
                                          class_="btn btn-info")

        registration_form = web.form.Form(username_textbox,
                                          password_textbox,
                                          register_button)
        return registration_form


class verifyLogin(object):
    '''
        Class handles login authentication.
    '''
    def POST(self):
        '''
            This function is called when the login button is clicked.
            If both fields are empty, return to login page.
        '''
        form = create_login_form()
        # returns to login page
        if not form.validates():
            web.ctx.session._initializer['loginStatus'] = web.ACCOUNT_LOGIN_UNSUCCESSFUL
            raise web.seeother('/login')
        else:
            # If valid admin, go to index
            is_valid = model.validate_admin(form.d.username, form.d.password)
            if is_valid:
                web.ctx.session._initializer['loginStatus'] = web.ACCOUNT_LOGIN_SUCCESSFUL
                web.setcookie('user', form.d.username)
                raise web.seeother('/')
            # Else go to error page
            else:
                web.ctx.session._initializer['loginStatus'] = web.ACCOUNT_LOGIN_UNSUCCESSFUL
                raise web.seeother('/login')
            