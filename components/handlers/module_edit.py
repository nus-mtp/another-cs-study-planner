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
        if module_info is None:
            return RENDER.notfound("Module " + module_code + " does not exist in the system.")

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
        module_info = model.get_module(module_code)
        if module_info is None:
            outcome = False
        elif (module_name != old_module_name or module_desc != old_module_desc or
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
    def __init__(self):
        '''
            Define the AY-Sems that are in the system
            By right, these settings hould be set by the superadmin
        '''
        self.number_of_future_ays = 1
        self.current_ay = model.get_current_ay()
        self.list_of_future_ay_sems = []

        ay = self.current_ay
        for i in range(self.number_of_future_ays):
            ay = model.get_next_ay(ay)
            self.list_of_future_ay_sems.append(ay+" Sem 1")
            self.list_of_future_ay_sems.append(ay+" Sem 2")


    def GET(self):
        '''
            Handles the loading of the 'Edit Specific Module Info' page
        '''
        data = web.input()
        module_code = data.code
        ay_sem = data.aySem

        module_info = model.get_module(module_code)
        if module_info is None:
            return RENDER.notfound("Module " + module_code + " does not exist in the system.")
        if ay_sem not in self.list_of_future_ay_sems:
            return RENDER.notfound(ay_sem + " is not in the system's list of future AY-Semesters.")

        module_ay_sem_info_handler = IndividualModule()
        module_ay_sem_info_handler.load_mounting_info(module_code, ay_sem)
        mounting_value = module_ay_sem_info_handler.get_mounting_status()
        quota = module_ay_sem_info_handler.get_quota()
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


        module_info = model.get_module(module_code)
        if module_info is None:
            outcome = False
        elif ay_sem not in self.list_of_future_ay_sems:
            outcome = False
        else:
            if mounting_status == "Mounted":
                outcome = None
                if old_mounting_value == "1":
                    outcome = model.update_quota(module_code, ay_sem, quota)
                else:
                    outcome = model.add_tenta_mounting(module_code, ay_sem, quota)
            elif mounting_status == "Not Mounted":
                outcome = model.delete_tenta_mounting(module_code, ay_sem)

        return Outcome().POST("edit_mounting", outcome, module_code, ay_sem)
