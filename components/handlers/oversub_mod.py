'''
    This module contains the handler for web requests pertaining to
    the list of oversubscribed modules.
'''


from app import RENDER
import web
from components import model


class OversubModule(object):
    '''
        This class contains the implementations of the GET
        requests.
    '''
    def GET(self):
        '''
            Renders the oversubscribed modules page if users requested
            for the page through the GET method.
        '''
        list_of_oversub_mod = model.get_oversub_mod()

        return RENDER.oversubscribedModules(list_of_oversub_mod)