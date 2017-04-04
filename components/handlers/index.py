'''
    This module contains the handler for web requests pertaining to
    the home page.
'''

from app import RENDER
import web
from components import model, session


class Index(object):
    '''
        This class is responsible for methods corresponding to the home page.
    '''
    def GET(self):
        '''
            This function is called when the '/' page (index.html) is loaded
            If user is not logged in, they are redirected to the login page.
        '''
        if not session.validate_session():
            raise web.seeother('/login')
        else:
            current_ay_with_current_date = model.get_current_ay_sem()[0:8]
            current_database_ay = model.get_current_ay()

            to_migrate_db = False

            if current_ay_with_current_date != current_database_ay:
                to_migrate_db = True

            # [NOTE] for debugging purposes, comment out this line when done.
            # to_migrate_db = True

            return RENDER.index(need_migration=to_migrate_db)
