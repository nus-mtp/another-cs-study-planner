'''
    This module handles session authentication
'''

import web

def validate_session():
    '''
        Check if session is valid by checking if
        a) user is logged in
        b) logged in user is who they claim to be
    '''
    # Check if user logged in successfully
    loginStatus = web.ctx.session._initializer.get('loginStatus')
    if (loginStatus != web.ACCOUNT_LOGIN_SUCCESSFUL):
        return False
    
    # Check if user is the logged in user
    user = web.cookies().get('user')
    if (web.ctx.session._initializer.get('userId') != user):
        return False
    return True
    