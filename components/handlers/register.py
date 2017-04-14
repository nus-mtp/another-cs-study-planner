'''
    This module handles account registration.
'''

import hashlib
import uuid
import web
from app import RENDER
from components import model
from components.handlers.outcome import Outcome


## For login test
class Register(object):
    '''
        Class handles registration (put user in database)
    '''
    def GET(self):
        '''
            This function is called when /register is accessed.
        '''
        web.header('X-Frame-Options', 'SAMEORIGIN')
        web.header('X-Content-Type-Options', 'nosniff')
        web.header('X-XSS-Protection', '1')
        return RENDER.register()


    def POST(self):
        '''
            This function is called when the register button is clicked.

            1) If username is taken, an alert will indicate that username
               is taken.
            2) If all validations pass, the account is inserted into the database.

            Blank inputs are blocked by front-end. For full extent of validation
            we also perform validation here should the front-end happen to be
            bypassed in some manner.
        '''
        web.header('X-Frame-Options', 'SAMEORIGIN')
        web.header('X-Content-Type-Options', 'nosniff')
        web.header('X-XSS-Protection', '1')
        credentials = web.input()

        try:
            input_id = credentials.id
            input_password = credentials.password
        except AttributeError:
            raise web.seeother('/register')

        # User ID and password should not be more than 20 characters long,
        # and should not contain special characters
        if not model.is_alpha_numeric(input_id) or \
        not model.is_alpha_numeric(input_password):
            outcome = False
        # If user ID already exists, alert user that the ID is taken.
        elif model.is_userid_taken(credentials.id):
            outcome = "taken"
        # Else, the new account is valid, and add it to the database.
        else:
            salt = uuid.uuid4().hex
            hashed_password = hashlib.sha512(credentials.password
                                             + salt).hexdigest()
            model.add_admin(credentials.id, salt, hashed_password)
            outcome = True

        return Outcome().POST("create_user", outcome, None)
