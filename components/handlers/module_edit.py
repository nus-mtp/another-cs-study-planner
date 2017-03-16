'''
    This module contains the handler for web requests pertaining to
    the editing of a module.
'''


from app import RENDER
import web
from components import model
from components.handlers.outcome import Outcome


class EditModuleInfo(object):
    '''
        This class handles the editing of module info
        (Module name, description and MCs)
    '''
    def POST(self, *test_data):
        '''
            Handles the loading and submission of the 'edit module' form
        '''
        if test_data:   # for testing purposes
            data = test_data[0]
        else:
            data = web.input()
        form_status = data.status
        module_code = data.code

        if form_status == "load":
            module_info = model.get_module(module_code)
            overlapping_mod_list = model.get_mod_taken_together_with(module_code)
            return RENDER.moduleEdit(module_info, overlapping_mod_list)

        elif form_status == "submit":
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
        This class handles the editing of mounting info
        (Mounting status and quota)
    '''
    def POST(self):
        '''
            Handles the loading and submission of the 'edit mounting' form
        '''
        data = web.input()
        form_status = data.status
        module_code = data.code
        ay_sem = data.aySem
        try:
            quota = data.quota
            if quota == "":
                quota = None
        except AttributeError:
            quota = None

        if form_status == "load":
            mounting_value = data.mountingValue
            overlapping_list = model.get_mod_taken_together_with(module_code)
            prereq_string = model.get_prerequisite_as_string(module_code)
            return RENDER.mountingEdit(module_code, ay_sem, mounting_value, quota, overlapping_list)

        elif form_status == "submit":
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
