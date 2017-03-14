'''
    This module handles account login.
'''

import web
from app import RENDER
from components import model, session
from components.handlers.outcome import Outcome


class Login(object):
    '''
        Class handles login (verifying if user is in database)
    '''
    URL_THIS_PAGE = '/login'


    def GET(self):
        '''
            This function is called when /login is accessed.
        '''
        return RENDER.login(session.validate_session())


    def POST(self):
        '''
            Blank inputs are blocked by front-end. For full extent of validation
            we also perform validation here should the front-end happen to be
            bypassed in some manner.
        '''
        credentials = web.input()

        try:
            input_id = credentials.id
            input_password = credentials.password
        except AttributeError:
            return Outcome().POST("login_user", False, None)

        if credentials.id == '' or credentials.password == '':
            return Outcome().POST("login_user", False, None)

        is_valid = model.validate_admin(credentials.id, credentials.password)

        # If valid admin, go to index
        if is_valid:
            session.clean_up_sessions()
            session.init_session(credentials.id)
            raise web.seeother('/')
        # Else go to error page
        else:
            return Outcome().POST("login_user", False, None)
