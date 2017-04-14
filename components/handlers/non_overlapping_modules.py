'''
    This module contains the handler for web requests pertaining to
    the list of modules not taken together by students.
'''


from app import RENDER
import web
from components import model, session


class NonOverlappingModules(object):
    '''
        This class contains the implementations of the GET
        requests.
    '''
    def __init__(self):
        self.CURRENT_SEM = model.get_current_ay_sem()
        self.AVAILABLE_AY_SEM = model.get_all_ay_sems()


    def validateAYSem(self, aysem):
        '''
            check if entered aysem is correct
        '''
        return aysem in self.AVAILABLE_AY_SEM


    def GET(self):
        '''
            Renders the non-overlapping modules page if users requested
            for the page through the GET method.
        '''
        web.header('X-Frame-Options', 'SAMEORIGIN')
        web.header('X-Content-Type-Options', 'nosniff')
        web.header('X-XSS-Protection', '1')
        if not session.validate_session():
            raise web.seeother('/login')
        ay_sem_of_interest = None

        #see if the user has already requested a search
        input_data = model.validate_input(web.input(), ["aysem"],
                                          aysem_specific=False, attr_required=False)
        try:
            ay_sem = input_data.aysem
            ay_sem_of_interest = ay_sem
        except AttributeError:
            ay_sem_of_interest = self.CURRENT_SEM
            if not self.validateAYSem(ay_sem_of_interest):
                ay_sem_of_interest = "AY 16/17 Sem 1"

        lst_of_independ_mods = model.get_mods_no_one_take(ay_sem_of_interest)

        return RENDER.nonOverlappingModules(lst_of_independ_mods,
                                            self.AVAILABLE_AY_SEM, ay_sem_of_interest)



    def POST(self):
        '''
            called from search with ay sem form
        '''
        #will have input data as function is called from button
        web.header('X-Frame-Options', 'SAMEORIGIN')
        web.header('X-Content-Type-Options', 'nosniff')
        web.header('X-XSS-Protection', '1')
        input_data = model.validate_input(web.input(), ["aysem"])
        ay_sem = input_data.aysem

        raise web.seeother('/nonOverlappingModules?aysem=' + ay_sem)
