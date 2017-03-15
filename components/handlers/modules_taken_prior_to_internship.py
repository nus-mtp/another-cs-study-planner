'''
    This module contains the handler for web requests pertaining to
    showing the list of modules taken before internship and
    the number of students who have taken those modules.
'''


from app import RENDER
import web
from components import model, session


class TakePriorInternship(object):
    '''
        This class contains the implementations of the GET
        requests.
    '''
    def __init__(self):
        pass


    def GET(self):
        '''
            Retrieve and display the list of modules taken before
            internship and the number of students who has taken those
            modules.
        '''
        if not session.validate_session():
            raise web.seeother('/login')

        module_list_with_count = model.get_mod_before_intern("AY 17/18 Sem 1") # dummy value

        return RENDER.modulesTakenPriorToInternship(module_list_with_count)
