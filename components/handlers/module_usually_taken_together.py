'''
    This module contains the handler for web requests pertaining to
    the list of modules usually taken together in the same
    semester
'''

from app import RENDER, SESSION
import web
from components import model


class ModuleUsuallyTakenTogether(object):
    '''
        
    '''
    def GET(self):
        '''
            Renders the modules page if users requested
            for the page through the GET method.
        '''
        if SESSION['id'] != web.ACCOUNT_LOGIN_SUCCESSFUL:
            raise web.seeother('/login')
        data = web.input()
        common_mod = data.code
        if len(common_mod) > 0:
            #if invalid, empty table will be returned
            lst_of_mods = model.get_mod_taken_together_with(common_mod)
        else:
            lst_of_mods = model.get_all_mods_taken_together()
        
        return RENDER.modulesTakenTogether(common_mod.upper(), lst_of_mods)

    
    def POST(self):
        '''
            Handles the loading of new searches
        '''

        data = web.input()
        common_mod = data.code
        if len(common_mod) > 0:
            #if invalid, empty table will be returned
            lst_of_mods = model.get_mod_taken_together_with(common_mod)
        else:
            lst_of_mods = model.get_all_mods_taken_together()

        raise web.seeother('/modulesTakenTogether?code='+common_mod.upper())

        






















            
