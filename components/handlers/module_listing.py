'''
    This module contains the handler for web requests pertaining to
    full modules listing.
'''


from app import RENDER, SESSION
import web
from components import model


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
        if SESSION['id'] != web.ACCOUNT_LOGIN_SUCCESSFUL:
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
        raise web.seeother(self.URL_THIS_PAGE)        # load index.html again

class FlagAsRemoved(object):
    '''
        This class handles the flagging of a module as 'To Be Removed'
    '''
    URL_THIS_PAGE = '/modules'

    def GET(self):
        ''' Redirect '''
        raise web.seeother(self.URL_THIS_PAGE)


    def POST(self, module_code):
        ''' Flag module as removed '''
        model.flag_module_as_removed(module_code)
        raise web.seeother(self.URL_THIS_PAGE)



class DeleteMod(object):
    '''
        This class handles the deletion of module
    '''
    URL_THIS_PAGE = '/modules'

    def GET(self):
        ''' Redirect '''
        raise web.seeother(self.URL_THIS_PAGE)


    def POST(self, module_code):        # module_code is obtained from the end of the URL
        ''' Delete the module '''
        outcome = model.delete_module(module_code)
        if outcome is False:
            SESSION['deleteError'] = module_code
            SESSION['displayErrorMessage'] = True
        raise web.seeother(self.URL_THIS_PAGE)
