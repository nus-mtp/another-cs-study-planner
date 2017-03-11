'''
    This module handles account login.
'''

from app import RENDER, SESSION
import web
from components import model


## For login test
class Login(object):
    '''
        Class handles login (verifying if user is in database)
    '''
    def GET(self):
        '''
            This function is called when /login is accessed.
        '''
        return RENDER.login(SESSION['id'])


    def POST(self):
        '''
            This function is called when the login button is clicked.
            If both fields are empty, return to login page.
        '''
        '''
            Blank inputs are blocked by front-end. For full extent of validation
            we also perform validation here should the front-end happen to be
            bypassed in some manner. 
        '''
        credentials = web.input()

        try:
            input_id = credentials.id
            input_password = credentials.password
        except(AttributeError):
            SESSION['id'] = web.ACCOUNT_LOGIN_UNSUCCESSFUL
            raise web.seeother('/login')

        if credentials.id == '' or credentials.password == '':
            raise web.seeother('/login')

        is_valid = model.validate_admin(credentials.id, credentials.password)
        
        # If valid admin, go to index
        if is_valid:
            SESSION['id'] = web.ACCOUNT_LOGIN_SUCCESSFUL
            raise web.seeother('/')
        # Else go to error page
        else:
            SESSION['id'] = web.ACCOUNT_LOGIN_UNSUCCESSFUL
            raise web.seeother('/login')
