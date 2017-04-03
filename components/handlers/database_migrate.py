'''
    This module contains the handler for web requests pertaining to
    the database migration page.
'''

from app import RENDER
import web
from components import model, session


class DatabaseMigrate(object):
    '''
        This class is responsible for methods corresponding to the database migration page.
    '''
    def GET(self):
        '''
            This function is called when the database migration page is loaded
            If user is not logged in, they are redirected to the login page.
        '''
        if not session.validate_session():
            raise web.seeother('/login')
        else:
            current_database_ay = model.get_all_fixed_ay_sems()[0][0][0:8]
            next_ay = model.get_next_ay(current_database_ay)
            future_ay = model.get_next_ay(next_ay)

            return RENDER.databaseMigrate(current_database_ay, next_ay, future_ay)


    def POST(self):
        model.migrate_to_next_aysem()
        web.seeother("/")
