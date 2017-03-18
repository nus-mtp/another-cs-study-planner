'''
    This module contains the handler for web requests pertaining to
    a module's mounting for a particular AY/Sem
'''


from app import RENDER
import web
from components import model, session


class IndividualModule(object):
    '''
        This class handles the display of a single module mounting
    '''
    def __init__(self):
        '''
            Define the AY-Sems that are in the system
            By right, these settings hould be set by the superadmin
        '''
        self.number_of_future_ays = 1
        self.current_ay = model.get_current_ay()
        self.list_of_ay_sems = [self.current_ay+" Sem 1", self.current_ay+" Sem 2"]

        ay = self.current_ay
        for i in range(self.number_of_future_ays):
            ay = model.get_next_ay(ay)
            self.list_of_ay_sems.append(ay+" Sem 1")
            self.list_of_ay_sems.append(ay+" Sem 2")

        self.mounting_status = -1
        self.quota = None
        self.is_current_ay = False


    def load_mounting_info(self, module_code, target_ay_sem):
        '''
            Load the mounting status and quota of the target module and AY/Sem
        '''
        fixed_mounting_status = -1
        fixed_quota = None
        is_current_ay = False

        # Get mounting status in current AY
        target_ay = target_ay_sem[0:8]
        current_ay = model.get_current_ay()
        if target_ay == current_ay:
            is_current_ay = True
            fixed_quota = model.get_quota_of_target_fixed_ay_sem(module_code, target_ay_sem)
        else:
            target_sem = target_ay_sem[9:14]
            fixed_quota = model.get_quota_of_target_fixed_ay_sem(module_code,
                                                                 current_ay+" "+target_sem)
        if fixed_quota is False:
            fixed_quota = '-'
        else:
            fixed_mounting_status = 1

        if is_current_ay:
            self.mounting_status = fixed_mounting_status
            self.quota = fixed_quota
        else:
            # Get mounting status in target (future) AY
            tenta_quota = model.get_quota_of_target_tenta_ay_sem(module_code, target_ay_sem)
            tenta_mounting_status = -1
            if tenta_quota is False:
                tenta_quota = '-'
                if fixed_mounting_status == 1:
                    tenta_mounting_status = 0
                else:
                    tenta_mounting_status = -1
            else:
                tenta_mounting_status = 1
            self.mounting_status = tenta_mounting_status
            self.quota = tenta_quota

        self.is_current_ay = is_current_ay


    def get_overlapping_mods(self, code):
        '''
            Get modules that over lap with this module
        '''
        return model.get_mod_taken_together_with(code)


    def get_mounting_status(self):
        '''
            Return the mounting status of the module in the target AY-Sem
        '''
        return self.mounting_status


    def get_quota(self):
        '''
            Return the quota of the module in the target AY-Sem
        '''
        return self.quota


    def GET(self):
        '''
            Retrieve and render all the info of a module mounting
        '''
        if not session.validate_session():
            raise web.seeother('/login')

        input_data = web.input()
        module_code = input_data.code
        module_info = model.get_module(module_code)
        if module_info is None:
            error_message = module_code + " does not exist in the system."
            return RENDER.notfound(error_message)
        target_ay_sem = input_data.targetAY
        if target_ay_sem not in self.list_of_ay_sems:
            return RENDER.notfound(target_ay_sem + " is not in the system's list of AY-Semesters.")

        self.load_mounting_info(module_code, target_ay_sem)
        is_future_ay = not self.is_current_ay

        overlapping_mod_list = model.get_mod_taken_together_with(module_code)
        prereq_string = model.get_prerequisite_as_string(module_code)
        preclude_string = model.get_preclusion_as_string(module_code)
        is_starred = model.is_module_starred(module_code, web.cookies().get('user'))

        return RENDER.individualModuleInfo(module_info, is_future_ay,
                                           target_ay_sem, self.mounting_status,
                                           self.quota, overlapping_mod_list,
                                           is_starred, prereq_string, preclude_string)


    def POST(self):
        ''' Redirect '''
        raise web.seeother('/')
