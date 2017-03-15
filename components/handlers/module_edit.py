'''
    This module contains the handler for web requests pertaining to
    the editing of a module.
'''


from app import RENDER
import web
from components import model
from components.handlers.outcome import Outcome
from components.handlers.module_view_in_ay_sem import IndividualModule


class EditModuleInfo(object):
    '''
        This class handles the editing of general module info
        (Module name, description and MCs)
    '''
    def GET(self):
        '''
            Handles the loading of the 'Edit General Module Info' page
        '''
        data = web.input()
        module_code = data.code

        module_info = model.get_module(module_code)
        overlapping_mod_list = model.get_mod_taken_together_with(module_code)
        return RENDER.moduleEdit(module_info, overlapping_mod_list)


    def POST(self, *test_data):
        '''
            Handles the submission of the 'Edit General Module Info' page
        '''
        if test_data:   # for testing purposes
            data = test_data[0]
        else:
            data = web.input()

        module_code = data.code
        module_name = data.name
        module_desc = data.desc
        module_mc = data.mc

        old_module_info = model.get_module(module_code)
        old_module_name = old_module_info[1]
        old_module_desc = old_module_info[2]
        old_module_mc = old_module_info[3]

        outcome = True
        if (module_name != old_module_name or module_desc != old_module_desc or
                int(module_mc) != int(old_module_mc)):
            model.store_original_module_info(module_code, old_module_name,
                                             old_module_desc, old_module_mc)
            outcome = model.update_module(module_code, module_name, module_desc, module_mc)

        if not test_data:
            return Outcome().POST("edit_module", outcome, module_code)


class EditMountingInfo(object):
    '''
        This class handles the editing of specific mounting info
        (Mounting status and quota)
    '''
    def GET(self):
        '''
            Handles the loading of the 'Edit Specific Module Info' page
        '''
        data = web.input()
        module_code = data.code
        ay_sem = data.aySem
        print ay_sem

        module_ay_sem_info_handler = IndividualModule()
        module_ay_sem_info_handler.load_mounting_info(module_code, ay_sem)
        mounting_value = module_ay_sem_info_handler.get_mounting_status()
        quota = module_ay_sem_info_handler.get_quota()
        print mounting_value
        overlapping_list = model.get_mod_taken_together_with(module_code)

        return RENDER.mountingEdit(module_code, ay_sem, mounting_value, quota, overlapping_list)


    def POST(self):
        '''
            Handles the submission of the 'Edit Specific Module Info' page
        '''
        data = web.input()
        module_code = data.code
        ay_sem = data.aySem
        try:
            quota = data.quota
            if quota == "":
                quota = None
        except AttributeError:
            quota = None

        old_mounting_value = data.oldMountingValue
        mounting_status = data.mountingStatus

        if mounting_status == "Mounted":
            outcome = None
            if old_mounting_value == "1":
                outcome = model.update_quota(module_code, ay_sem, quota)
            else:
                outcome = model.add_tenta_mounting(module_code, ay_sem, quota)
        elif mounting_status == "Not Mounted":
            outcome = model.delete_tenta_mounting(module_code, ay_sem)

        return Outcome().POST("edit_mounting", outcome, module_code, ay_sem)
