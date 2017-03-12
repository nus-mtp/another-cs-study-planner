'''
    This module contains the handler for web requests pertaining to
    the home page.
'''

from app import RENDER
import web
from components import model, session


class Index(object):
    '''
        This class is responsible for methods corresponding to the home page.
    '''
    def GET(self):
        '''
            This function is called when the '/' page (index.html) is loaded
            If user is not logged in, they are redirected to the login page.
        '''
        if not session.validate_session():
            raise web.seeother('/login')
        else:
            return RENDER.index()

