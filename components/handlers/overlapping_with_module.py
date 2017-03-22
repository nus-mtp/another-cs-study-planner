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
        try:
            aysem = data_input.aysem
            #need to change to overlapping for one sem
            lst_of_mods = model.get_mod_taken_together_with_mod_and_aysem(code, aysem)
            return RENDER.overlappingWithModule(code, aysem, lst_of_mods, True)
        except AttributeError:
            aysem = 'All Semesters'
            #need to change to overlapping for one sem
            lst_of_mods = model.get_mod_taken_together_with(code)
            return RENDER.overlappingWithModule(code, aysem, lst_of_mods, False)
