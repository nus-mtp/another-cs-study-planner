'''
    This module contains the handler for web requests pertaining to
    the list of oversubscribed modules.
'''


from app import RENDER
import web
from components import model


class OversubModule(object):
    '''
        This class contains the implementations of the GET
        requests.
    '''
    def GET(self):
        '''
            Renders the oversubscribed modules page if users requested
            for the page through the GET method.
        '''
        #table_of_year_of_study_with_count = model.get_num_students_by_yr_study()
        #table_of_focus_area_with_count = model.get_num_students_by_focus_areas()

        return RENDER.oversubscribedModules()
