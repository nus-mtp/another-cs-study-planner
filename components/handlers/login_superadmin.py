'''
    This module handles super admin log in
'''
import hashlib
from app import RENDER, SESSION
import web
from components import model

class LoginSuperAdmin(object):
    '''
        Class handles super admin log in
    '''

    def __init__(self):
        '''
            initilaze super admin
        '''

    def GET(self):
        '''
            gets super admin login page
        '''

class verifyLogin(object):
    '''
        used when login button is clicked
    '''

    def POST(self):
        '''
            called when login button is clicked.
        '''
