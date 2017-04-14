'''
    This module contains the handler for web requests pertaining to
    showing the list of modules taken before internship and
    the number of students who have taken those modules.
'''


from app import RENDER
import web
from components import model, session


class TakePriorInternship(object):
    '''
        This class contains the implementations of the GET
        requests.
    '''
    def __init__(self):
        self.CURRENT_SEM = model.get_current_ay_sem()
        self.AVAILABLE_AY_SEM = model.get_all_ay_sems()


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

        modules_before_internship = model.get_mod_before_intern(ay_sem_of_interest)
        return RENDER.modulesTakenPriorToInternship(modules_before_internship,
                                                    self.AVAILABLE_AY_SEM,
                                                    ay_sem_of_interest)


    def POST(self):
        '''
            Invoked when user wants to search for modules
            before internship with a specified AY-Sem
        '''
        # will have input data as function is called from button
        web.header('X-Frame-Options', 'SAMEORIGIN')
        web.header('X-Content-Type-Options', 'nosniff')
        web.header('X-XSS-Protection', '1')
        input_data = model.validate_input(web.input(), ["aysem"])
        ay_sem = input_data.aysem

        raise web.seeother('/moduleTakenPriorToInternship?aysem=' + ay_sem)
