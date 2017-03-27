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
    all_ay_sems = model.get_all_ay_sems()

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

        input_data = model.validate_input(web.input(), ["aysem"],
                                          aysem_specific=False, attr_required=False)
        try:
            # Search request by user
            ay_sem_of_interest = input_data.aysem
            lower_range_class_size = input_data.lowerClassSize
            higher_range_class_size = input_data.higherClassSize
        except AttributeError:
            # Loading the page without sufficient data (first time load page)
            current_aysem = model.get_current_ay_sem()
            return RENDER.moduleSpecificSize(self.all_ay_sems, None, current_aysem, None, None)

        if not self.is_valid_range(lower_range_class_size, higher_range_class_size):
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
        input_data = model.validate_input(web.input(), ["aysem"])
        try:
            ay_sem_of_interest = input_data.aysem
            lower_range_class_size = input_data.lowerClassSize
            higher_range_class_size = input_data.higherClassSize
        except AttributeError:
            error = RENDER.notfound('Please do not tamper with our html forms. Thank you! ;)')
            raise web.notfound(error)

        webpage_to_redirect = "/moduleSpecificSize?aysem=" + ay_sem_of_interest + \
                              "&lowerClassSize=" + lower_range_class_size + \
                              "&higherClassSize=" + higher_range_class_size

        raise web.seeother(webpage_to_redirect)
