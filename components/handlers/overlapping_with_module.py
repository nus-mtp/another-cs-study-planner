'''
    this module handles get messages for the overlapping modules template.
'''

from app import RENDER
import web
from components import model, session


class OverlappingWithModule(object):
    '''
        define get
    '''
    def GET(self):
        '''
            renders list of modules that overlapps with this module
        '''
        if not session.validate_session():
            raise web.seeother('/login')

        data_input = web.input()
        code = data_input.code
        lst_of_mods = model.get_mod_taken_together_with(code)
        return RENDER.overlappingWithModule(code, lst_of_mods)
