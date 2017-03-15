'''
    This module handles starring of modules.
'''

import web
from app import RENDER
from components import model, session
from components.handlers.outcome import Outcome


class StarModules(object):
    '''
        Class handles starring and unstarring of modules.
    '''

    def GET(self):
        '''
            This function is called when /starModule is accessed.
        '''
        if not session.validate_session():
            raise web.seeother('/login')
        else:
            return RENDER.index()

class StarListing(object):
    '''
        Class handles showing of starredModules
    '''

    def GET(self):
        '''
            This function is called when /starredModules is accessed.
        '''
        if not session.validate_session():
            raise web.seeother('/login')
        else:
            return RENDER.index()    