'''
    This module contains the handler for web requests pertaining to
    the list of modules usually taken together in the same
    semester
'''

from app import RENDER
import web
from components import model, session


class OverlappingModules(object):
    '''
        define get and post for overlappingModules.html
    '''
    def GET(self):
        '''
            Renders the modules page if users requested
            for the page through the GET method.
        '''
        if not session.validate_session():
            raise web.seeother('/login')
        lst_of_mods = model.get_all_mods_taken_together()
        return RENDER.overlappingModules(lst_of_mods)
