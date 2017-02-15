'''
    This module contains the handler for web requests pertaining to
    queries. (this is a dummy file)
'''


from app import RENDER
import web
from components import model


class DummyQuery(object):
    '''
        This class contains the implementations of the GET and POST
        requests.
    '''
    def GET(self):
        '''
            Renders the dummy query page if users requested
            for the page through the GET method.
        '''
        table_of_year_of_study_with_count = model.get_num_students_by_yr_study()
        table_of_focus_area_with_count = model.get_num_students_by_focus_areas()

        return RENDER.dummyQuery(table_of_year_of_study_with_count, 
            table_of_focus_area_with_count)
