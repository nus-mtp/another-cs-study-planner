'''
    This module contains the handler for web requests pertaining to
    the list of modules with specific class size
'''


from app import RENDER
import web
from components import model, session
from components.handlers.outcome import Outcome


class ModuleSpecificSize(object):
    '''
        This class contains the implementations of the GET
        requests.
    '''
    def __init__(self):
        fixed_ay_sems = model.get_all_fixed_ay_sems()
        tenta_ay_sems = model.get_all_tenta_ay_sems()
        fixed_ay_sems_list = [aysem[0] for aysem in fixed_ay_sems]
        tenta_ay_sems_list = [aysem[0] for aysem in tenta_ay_sems]
        self.all_ay_sems = fixed_ay_sems_list + tenta_ay_sems_list


    def is_valid_ay_sem(self, aysem):
        '''
            Returns true if given aysem is valid (exists in database),
            returns false otherwise.
        '''
        return aysem in self.all_ay_sems


    def is_a_number(self, given_input):
        '''
            Returns true if given_input is a number (int),
            returns false otherwise.
        '''
        try:
            given_input = int(given_input)
            return True
        except ValueError:
            return False


    def is_valid_range(self, low_range, high_range):
        '''
            Returns true if given low and high ranges are valid.
            i.e. both are numbers (int), low <= high, low >= 0 and high <= 999
            Returns false otherwise.
        '''
        if not self.is_a_number(low_range) or not self.is_a_number(high_range):
            return False

        # Convert from unicode to integer
        low_range = int(low_range)
        high_range = int(high_range)

        return low_range <= high_range and low_range >= 0 and high_range <= 999


    def GET(self):
        '''
            Renders the list of modules with specific class size page if users
            requested for the page through the GET method.
        '''
        if not session.validate_session():
            raise web.seeother('/login')

        input_data = web.input()
        if len(input_data) == 0 or input_data.sem is None or input_data.lowerClassSize is None \
            or input_data.higherClassSize is None:
            # Loading the page without sufficient data (first time load page)
            return RENDER.moduleSpecificSize(self.all_ay_sems, None, None, None, None)
        else:
            # Search request by user
            ay_sem_of_interest = input_data.sem
            lower_range_class_size = input_data.lowerClassSize
            higher_range_class_size = input_data.higherClassSize

        if not self.is_valid_ay_sem(ay_sem_of_interest):
            return Outcome().POST("mods-specific-size-aysem", False, None)
        elif not self.is_valid_range(lower_range_class_size, higher_range_class_size):
            return Outcome().POST("mods-specific-size-range", False, None)
        else:
            # All inputs are valid

            # Convert unicode to int
            lower_range = int(lower_range_class_size)
            higher_range = int(higher_range_class_size)

            list_of_mods = \
                model.get_mod_specified_class_size(ay_sem_of_interest, lower_range,
                                                   higher_range)

            return RENDER.moduleSpecificSize(self.all_ay_sems, list_of_mods,
                                             ay_sem_of_interest, lower_range,
                                             higher_range)


    def POST(self):
        '''
            called from search with form
        '''
        # Input data will have valid inputs as function is called from submit button
        input_data = web.input()
        ay_sem_of_interest = input_data.sem
        lower_range_class_size = input_data.lowerClassSize
        higher_range_class_size = input_data.higherClassSize

        webpage_to_redirect = "/moduleSpecificSize?sem=" + ay_sem_of_interest + \
                              "&lowerClassSize=" + lower_range_class_size + \
                              "&higherClassSize=" + higher_range_class_size

        raise web.seeother(webpage_to_redirect)
