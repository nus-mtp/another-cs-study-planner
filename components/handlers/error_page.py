'''
    display when failed
'''

from app import RENDER
import web

class ErrorPage(object):
    '''
        shows error page with error message
    '''
    def GET(self):
        '''
            shows error page with error message, if no messages, tells the user
        '''
        data = web.input()
        try:
            error = data.error
            return RENDER.errorPage(error)
        except AttributeError:
            return RENDER.errorPage("AttributeError: no error message supplied.")
