'''
    This module contains the handler for web requests pertaining to
    the database migration page.
'''

from app import RENDER
import web
from components import model, session
from components.handlers.outcome import Outcome


class DatabaseMigrate(object):
    '''
        This class is responsible for methods corresponding to the database migration page.
    '''
    def GET(self):
        '''
            This function is called when the database migration page is loaded
            If user is not logged in, they are redirected to the login page.
        '''
        web.header('X-Frame-Options', 'SAMEORIGIN')
        web.header('X-Content-Type-Options', 'nosniff')
        web.header('X-XSS-Protection', '1')
        if not session.validate_session():
            raise web.seeother('/login')
        else:
            current_ay_with_current_date = model.get_current_ay_sem()[0:8]
            current_database_ay = model.get_current_ay()

            if current_ay_with_current_date == current_database_ay:
                # pass # [NOTE] uncomment out this line for debugging purposes
                raise web.seeother("/") # [NOTE] comment out this line for debugging purposes

            next_ay = model.get_next_ay(current_database_ay)
            future_ay = model.get_next_ay(next_ay)

            return RENDER.databaseMigrate(current_database_ay, next_ay, future_ay)


    def POST(self):
        '''
            Performs the database migration, should the user acknowledges
            the implication involved, and presses the 'Proceed' button in
            the web page.
        '''
        web.header('X-Frame-Options', 'SAMEORIGIN')
        web.header('X-Content-Type-Options', 'nosniff')
        web.header('X-XSS-Protection', '1')
        hasSucceeded = model.migrate_to_next_aysem()

        return Outcome().POST("migrate-database", hasSucceeded, None)
