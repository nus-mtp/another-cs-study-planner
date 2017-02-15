'''
    This module contains the handler for web requests pertaining to
    fixed module mountings.
'''


from app import RENDER
import web
from components import model


class Fixed(object):
    '''
        This class contains the implementations of the GET and POST
        requests.
    '''
    def GET(self):
        '''
            Renders the fixed mounting page if users requested
            for the page through the GET method.
        '''
        mountedModuleInfos = model.get_all_fixed_mounted_modules()
        return RENDER.moduleMountingFixed(mountedModuleInfos)


    def POST(self):
        '''
            Directs users to the page for fixed module mountings.

            This method is invoked when users click on the button
            to navigate to the fixed module mountings, that is
            present in other valid pages.
        '''
        raise web.seeother('/moduleMountingFixed')
