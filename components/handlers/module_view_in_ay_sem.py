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
        self.mounting_status = -1
        self.quota = None
        self.is_current_ay = False


    def get_current_ay(self):
        '''
            All fixed mountings should be from the same AY,
            so just get the AY from the first entry
            Test case will ensure that all entries in fixed mountings have the same AY
        '''
        return model.get_first_fixed_mounting()[0][0:8]


    def load_mounting_info(self, module_code, target_ay_sem):
        '''
            Load the mounting status and quota of the target module and AY/Sem
        '''
        fixed_mounting_status = -1
        fixed_quota = None
        is_current_ay = False

        # Get mounting status in current AY
        target_ay = target_ay_sem[0:8]
        current_ay = self.get_current_ay()
        if target_ay == current_ay:
            is_current_ay = True
            fixed_quota = model.get_quota_of_target_fixed_ay_sem(module_code, target_ay_sem)
        else:
            target_sem = target_ay_sem[9:14]
            fixed_quota = model.get_quota_of_target_fixed_ay_sem(module_code,
                                                                 current_ay+" "+target_sem)
        if len(fixed_quota) == 0:
            fixed_quota = '-'
        else:
            fixed_mounting_status = 1
            fixed_quota = fixed_quota[0][0]

        if is_current_ay:
            self.mounting_status = fixed_mounting_status
            self.quota = fixed_quota
        else:
            # Get mounting status in target (future) AY
            tenta_quota = model.get_quota_of_target_tenta_ay_sem(module_code, target_ay_sem)
            tenta_mounting_status = -1
            if len(tenta_quota) == 0:
                tenta_quota = '-'
                if fixed_mounting_status == 1:
                    tenta_mounting_status = 0
                else:
                    tenta_mounting_status = -1
            else:
                tenta_mounting_status = 1
                tenta_quota = tenta_quota[0][0]
            self.mounting_status = tenta_mounting_status
            self.quota = tenta_quota

        self.is_current_ay = is_current_ay

    def get_overlapping_mods(self, code):
        '''
            Get modules that over lap with this module
        '''
        return model.get_mod_taken_together_with(code)
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
            raise web.seeother('/404')
        target_ay_sem = input_data.targetAY

        self.load_mounting_info(module_code, target_ay_sem)
        is_future_ay = not self.is_current_ay
        overlapping_mod_list = model.get_mod_taken_together_with(module_code)

        system_message = web.ctx.session._initializer['editMountMsg']
        web.ctx.session._initializer['editMountMsg'] = None

        return RENDER.individualModuleInfo(module_info, is_future_ay,
                                           target_ay_sem, self.mounting_status,
                                           self.quota, system_message, overlapping_mod_list)


    def POST(self):
        ''' Redirect '''
        raise web.seeother('/')
