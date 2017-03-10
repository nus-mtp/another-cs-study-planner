'''
    This module contains the handler for web requests pertaining to
    showing the number of students who have taken module A
    prior to taking module B
'''


from app import RENDER, SESSION
import web
from components import model


class TakePriorTo(object):
    '''
        This class contains the implementations of the GET
        requests.
    '''
    def GET(self):
        '''
            Retrieve and display the pairs of modules that have
            at least 1 student who has taken module A
            prior to taking module B
        '''
        if SESSION['id'] != web.ACCOUNT_LOGIN_SUCCESSFUL:
            raise web.seeother('/login')

        module_pairs = model.get_modA_taken_prior_to_modB()

        return RENDER.modulesTakenPriorToAnother(module_pairs)