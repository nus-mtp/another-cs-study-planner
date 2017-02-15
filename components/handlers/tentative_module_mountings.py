'''
    This module contains the handler for web requests pertaining to
    tentative module mountings.
'''


import web


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
        mountedModuleInfos = model.getAllTentativeMountedModules()
        return render.moduleMountingTentative(mountedModuleInfos)


    def POST(self):
        '''
            Directs users to the page for tentative module mountings.

            This method is invoked when users click on the button
            to navigate to the tentative module mountings, that is
            present in other valid pages.
        '''
        raise web.seeother('/moduleMountingTentative')
