'''
    This module contains the handler for web requests pertaining to
    tentative module mountings.
'''


from app import RENDER
import web
from components import model


class Tentative(object):
    '''
        This class contains the implementations of the GET and POST
        requests.
    '''
    def GET(self):
        '''
            Renders the tentative mounting page if users requested
            for the page through the GET method.
        '''
        mountedModuleInfos = model.get_all_tenta_mounted_modules()
        return RENDER.moduleMountingTentative(mountedModuleInfos)


    def POST(self):
        '''
            Directs users to the page for tentative module mountings.

            This method is invoked when users click on the button
            to navigate to the tentative module mountings, that is
            present in other valid pages.
        '''
        raise web.seeother('/moduleMountingTentative')
