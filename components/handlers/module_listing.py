'''
    This module contains the handler for web requests pertaining to
    full modules listing.
'''


from app import RENDER
import web
from components import model, session, check_string
from components.handlers.outcome import Outcome


class Modules(object):
    '''
        This class handles the 'Add Module' form and the displaying of list of modules
    '''
    URL_THIS_PAGE = '/modules'


    def GET(self):
        '''
            This function is called when the '/modules' page (moduleListing.html) is loaded
            If user is not logged in, they are redirected to the login page.
        '''
        if not session.validate_session():
            raise web.seeother('/login')
        else:
            module_infos = model.get_all_modules()
            return RENDER.moduleListing(module_infos)
