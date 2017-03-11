'''
    Temporary page for 404 errors
'''

from app import RENDER

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
