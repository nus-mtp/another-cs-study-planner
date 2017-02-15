'''
    This module contains the handler for web requests pertaining to
    full modules listing.
'''


from app import RENDER
import web
from components import model


class Modules(object):
    '''
        This class contains the implementations of the GET and POST
        requests.

        [NOTE]: Temporarily implemented to direct users to the home page.
    '''
    def GET(self):
        '''
            Renders the full modules listing page if users requested
            for the page through the GET method.
        '''
        raise web.seeother('/')


    def POST(self):
        '''
            Directs users to the page for full module listing.

            This method is invoked when users click on the button
            to navigate to the full modules listing, that is
            present in other valid pages.
        '''
        raise web.seeother('/')


class FlagAsRemoved(object):
    '''
        This class handles the flagging of a module as 'To Be Removed'
    '''
    def GET(self):
        ''' Redirect '''
        raise web.seeother('/')


    def POST(self, module_code):
        ''' Flag module as removed '''
        model.flag_module_as_removed(module_code)
        raise web.seeother('/')


class FlagAsActive(object):
    '''
        This class handles the flagging of a module as 'Active'
    '''
    def GET(self):
        ''' Redirect '''
        raise web.seeother('/')


    def POST(self, module_code):
        ''' Flag module as active '''
        model.flag_module_as_active(module_code)
        raise web.seeother('/')


class DeleteMod(object):
    '''
        This class handles the deletion of module
    '''
    def GET(self):
        ''' Redirect '''
        raise web.seeother('/')


    def POST(self, module_code):        # module_code is obtained from the end of the URL
        ''' Delete the module '''
        model.delete_module(module_code)
        raise web.seeother('/')
