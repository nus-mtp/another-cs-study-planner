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

    CURRENT_SEM = 'AY 16/17 Sem 1'
    AVAILABLE_AY_SEM = ['AY 16/17 Sem 1', 'AY 16/17 Sem 2', 'AY 17/18 Sem 1', 'AY 17/18 Sem 2']


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