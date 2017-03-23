'''
    This module contains the handler for web requests pertaining to
    showing the list of modules taken before internship and
    the number of students who have taken those modules.
'''


from app import RENDER
import web
from components import model, session
from components.handlers.outcome import Outcome


class TakePriorInternship(object):
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
            Check if entered AY-Sem is correct
        '''
        return aysem in self.AVAILABLE_AY_SEM


    def GET(self):
        '''
            Retrieve and display the list of modules taken before
            internship and the number of students who has taken those
            modules.
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
            modules_before_internship = model.get_mod_before_intern(ay_sem_of_interest)
            return RENDER.modulesTakenPriorToInternship(modules_before_internship,
                                                        self.AVAILABLE_AY_SEM,
                                                        ay_sem_of_interest)
        else:
            return Outcome().POST("mods-before-internship", False, None)


    def POST(self):
        '''
            Invoked when user wants to search for modules
            before internship with a specified AY-Sem
        '''
        # will have input data as function is called from button
        input_data = web.input()
        ay_sem = input_data.sem
        raise web.seeother('/moduleTakenPriorToInternship?sem=' + ay_sem)
