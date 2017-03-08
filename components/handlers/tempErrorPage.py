'''
    Temporary page for 404 errors
'''

from app import RENDER
import web
from components import model


## Temporary error class
class Error(object):
    '''
        Class handles 404 errors
    '''
    def GET(self):
        '''
            This function is called when /404 is accessed.
        '''
        return RENDER.error()
