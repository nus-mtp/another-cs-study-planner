'''
    This module contains the handler for web requests pertaining to
    the restoration of a module's information to original state
'''


import web
from components import model, check_string
from components.handlers.outcome import Outcome


class RestoreModule(object):
    '''
        This class handles the restoration of module info
    '''
    def POST(self, *test_data):
        '''
            Handles the restoration of module info
        '''
        if test_data:  # for testing purposes
            input_data = test_data[0]
        else:
            input_data = model.validate_input(web.input(), ["code", "restore_type"])

        module_code = input_data.code
        restore_type = input_data.restoreType

        if restore_type.lower() == "quota":
            model.validate_input(input_data, ["aysem"])
            ay_sem = input_data.aysem

            quota = input_data.quota
            if quota == "":
                quota = None

            outcome = model.update_quota(module_code, ay_sem, quota)

            if not test_data:
                return Outcome().POST("restore_module", outcome, module_code)

        elif restore_type.lower() == "mounting":
            model.validate_input(input_data, ["aysem"])
            target_ay_sem = input_data.aysem
            mounting_change = int(input_data.mountingChange)

            outcome = None
            if mounting_change == 1:  # Is mounted, so should revert to unmounted
                outcome = model.delete_tenta_mounting(module_code, target_ay_sem)
            elif mounting_change == 0:  # Is unmounted, so should revert to mounted
                current_ay_sem = input_data.currentAySem
                quota = model.get_quota_of_target_fixed_ay_sem(module_code, current_ay_sem)
                outcome = model.add_tenta_mounting(module_code, target_ay_sem, quota)

            if not test_data:
                return Outcome().POST("restore_module", outcome, module_code)

        elif restore_type.lower() == "moduledetails":
            original_module_details = model.get_original_module_info(module_code)
            model.remove_original_module_info(module_code)
            outcome = model.update_module(module_code, original_module_details[1],
                                          original_module_details[2], original_module_details[3])

            if not test_data:
                return Outcome().POST("restore_module", outcome, module_code)
