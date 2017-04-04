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

        input_data = model.validate_input(web.input(), ["aysem"],
                                          aysem_specific=False, attr_required=False)
        try:
            target_ay_sem = input_data.aysem
        except AttributeError:
            target_ay_sem = model.get_current_ay_sem()

        lst_of_mods = model.get_all_mods_taken_together(aysem=target_ay_sem)
        # Get a list of all AY-Sems (for users to select)
        all_ay_sems = model.get_all_ay_sems()

        return RENDER.overlappingModules(lst_of_mods, all_ay_sems, target_ay_sem)
