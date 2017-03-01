'''
    This module contains the handler for web requests pertaining to
    the list of modules usually taken together in the same
    semester
'''

from app import RENDER, SESSION
import web
from components import model


class DummyQuery(object):
    '''
        This class contains the implementations of the GET
        requests.
    '''
    def GET(self):
        '''
            Renders the modules page if users requested
            for the page through the GET method.
        '''
        if SESSION['id'] != web.ACCOUNT_LOGIN_SUCCESSFUL:
            raise web.seeother('/login')

        list_of_mod_taken_with_1010 = model.get_mod_taken_together_with('CS1010')

        return RENDER.dummyQuery(list_of_mod_taken_with_1010)
