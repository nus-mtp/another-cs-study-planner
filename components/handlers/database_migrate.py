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
            current_ay_with_current_date = model.get_current_ay_sem()[0:8]
            current_database_ay = model.get_current_ay()

            if current_ay_with_current_date == current_database_ay:
                raise web.seeother("/")

            next_ay = model.get_next_ay(current_database_ay)
            future_ay = model.get_next_ay(next_ay)

            return RENDER.databaseMigrate(current_database_ay, next_ay, future_ay)


    def POST(self):
        '''
            Performs the database migration, should the user acknowledges
            the implication involved, and presses the 'Proceed' button in
            the web page.
        '''
        # TODO: retrieve a Boolean from the migration function to determine
        # if the migration was completed successfully, and use JavaScript to
        # redirect to index page.
        model.migrate_to_next_aysem()
        web.seeother("/")
