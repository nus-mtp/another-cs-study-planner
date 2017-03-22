'''
    This module contains the handler for web requests pertaining to
    the list of modules not taken together by students.
'''


from app import RENDER
import web
from components import model, session
from components.handlers.outcome import Outcome


class NonOverlappingModules(object):
    '''
        This class contains the implementations of the GET
        requests.
    '''
    def __init__(self):
        self.CURRENT_SEM = model.get_current_ay_sem()
        self.AVAILABLE_AY_SEM = self.getAllAySem()


    def getAllAySem(self):
        '''
            Retrieves a list of all available AY-Semesters.
        '''
        fixed_ay_sems = model.get_all_fixed_ay_sems()
        tenta_ay_sems = model.get_all_tenta_ay_sems()
        fixed_ay_sems_list = [aysem[0] for aysem in fixed_ay_sems]
        tenta_ay_sems_list = [aysem[0] for aysem in tenta_ay_sems]

        return fixed_ay_sems_list + tenta_ay_sems_list


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
        if not session.validate_session():
            raise web.seeother('/login')
        ay_sem_of_interest = None

        #see if the user has already requested a search
        try:
            input_data = web.input()
            ay_sem = input_data.sem
            ay_sem_of_interest = ay_sem
        except AttributeError:
            ay_sem_of_interest = self.CURRENT_SEM
            if not self.validateAYSem(ay_sem_of_interest):
                ay_sem_of_interest = "AY 16/17 Sem 1"

        if self.validateAYSem(ay_sem_of_interest):
            lst_of_independ_mods = model.get_mods_no_one_take(ay_sem_of_interest)

            return RENDER.nonOverlappingModules(lst_of_independ_mods,
                                                self.AVAILABLE_AY_SEM, ay_sem_of_interest)
        else:
            return Outcome().POST("non-overlapping-mods", False, None)


    def POST(self):
        '''
            called from search with ay sem form
        '''
        #will have input data as function is called from button
        input_data = web.input()
        ay_sem = input_data.sem
        raise web.seeother('/nonOverlappingModules?sem=' + ay_sem)
