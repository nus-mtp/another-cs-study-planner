'''
    This module contains the handler for web requests pertaining to
    the list of modules not taken together by students.
'''


from app import RENDER, SESSION
import web
from components import model


class NonOverlappingModules(object):
    '''
        This class contains the implementations of the GET
        requests.
    '''
    def GET(self):
        '''
            Renders the non-overlapping modules page if users requested
            for the page through the GET method.
        '''
        if SESSION['id'] != web.ACCOUNT_LOGIN_SUCCESSFUL:
            raise web.seeother('/login')

        #TODO: Change hardcoded parameter passed in below.
        list_of_mod_no_one_take = model.get_mods_no_one_take('AY 16/17 Sem 1')

        return RENDER.nonOverlappingModules(list_of_mod_no_one_take)
