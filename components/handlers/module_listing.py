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


    def POST(self):
        '''
            This function might be called from button links from other pages.
        '''

        # Detects if this function is called from button links from another page.
        referrer_page = web.ctx.env.get('HTTP_REFERER', self.URL_THIS_PAGE)
        parts = referrer_page.split("/")
        referrer_page_shortform = "/" + parts[len(parts) - 1]
        # If referred from another page, direct to this page straight away.
        if referrer_page_shortform != self.URL_THIS_PAGE:
            raise web.seeother(self.URL_THIS_PAGE)

        try:
            data = web.input()
            action = data.action  # if action is not 'delete', will trigger AttributeError
            module_code = data.code

            if not (check_string.check_code(module_code)):
                return Outcome().POST("invalid_input")
            
            outcome = model.delete_module(module_code)
            return Outcome().POST("delete_module", outcome, module_code)

        except AttributeError:
            raise web.seeother(self.URL_THIS_PAGE)
