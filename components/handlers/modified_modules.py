'''
    This module contains the handler for web requests pertaining to
    retrieiving modules that have been modified.
'''


from app import RENDER, SESSION
import web
from components import model
from components.handlers.fixed_module_mountings import Fixed
from components.handlers.tentative_module_mountings import Tentative


class Modified(object):
    '''
        This class contains the implementations of the GET and POST requests.
        It retrieves a list of modified modules and determine which attributes
        have been modified.
    '''
    def __init__(self):
        '''
            Define the number of future AYs that will be included
        '''
        self.number_of_future_ays = 1


    def get_next_ay(self, ay):
        '''
            Return the AY that comes after the given AY
        '''
        ay = ay.split(' ')[1].split('/')
        return 'AY ' + str(int(ay[0])+1) + '/' + str(int(ay[1])+1)


    def get_modules_with_modified_quota(self):
        '''
            Get all modules whose quota has been modified in a future AY.
            Return the module code, current AY-Sem, target AY-Sem, current quota, 
            modified quota, and quota difference
        '''
        modified_modules = model.get_modules_with_modified_quota()
        modified_modules = [list(module) for module in modified_modules]
        for module in modified_modules:
            current_quota = module[3]
            modified_quota = module[4]
            if current_quota is None:
                quota_difference = modified_quota
            elif modified_quota is None:
                quota_difference = -current_quota
            else:
                quota_difference = modified_quota - current_quota
            module.append(quota_difference)
        return modified_modules


    def get_modules_with_modified_mounting(self):
        '''
            Get all modules whose mounting has been modified in a future AY.
            Return the module code, current AY-Sem, target AY-Sem, current quota, 
            modified quota, and quota difference
        '''
        # Generate fixed mounting plan
        fixed_mounting_handler = Fixed()
        current_ay = model.get_current_ay()
        fixed_mounting_handler.populate_module_code_and_name()
        fixed_mounting_handler.populate_mounting_values()
        fixed_full_mounting_plan = fixed_mounting_handler.full_mounting_plan

        modified_modules = []
        target_ay = current_ay

        # Loop through each future AY
        for i in range(self.number_of_future_ays):
            target_ay = self.get_next_ay(target_ay)

            # Generate tentative mounting plan
            tenta_mounting_handler = Tentative()
            tenta_mounting_handler.populate_module_code_and_name()
            tenta_mounting_handler.populate_mounting_values(target_ay)
            tenta_full_mounting_plan = tenta_mounting_handler.full_mounting_plan

            # Compare the fixed and tentative mounting of each module for each semester
            # to see if there is any difference (if there is, means it's modified)
            for i in range(len(fixed_full_mounting_plan)):
                fixed_subplan = fixed_full_mounting_plan[i]
                tenta_subplan = tenta_full_mounting_plan[i]
                module_code = fixed_subplan[0]

                fixed_ay_sem = fixed_subplan[1]
                fixed_sem_1_mounting = fixed_subplan[2]
                tenta_sem_1_mounting = tenta_subplan[2]
                fixed_sem_2_mounting = fixed_subplan[3]
                tenta_sem_2_mounting = tenta_subplan[3]

                if tenta_sem_1_mounting == 0:
                    modified_modules.append([module_code, current_ay+" Sem 1",
                                               target_ay+" Sem 1", "Unmounted"])
                elif tenta_sem_1_mounting == 1 and fixed_sem_1_mounting == -1:
                    modified_modules.append([module_code, current_ay+" Sem 1",
                                               target_ay+" Sem 1", "Mounted"])

                if tenta_sem_2_mounting == 0:
                    modified_modules.append([module_code, current_ay+" Sem 2",
                                               target_ay+" Sem 2", "Unmounted"])
                elif tenta_sem_2_mounting == 1 and fixed_sem_2_mounting == -1:
                    modified_modules.append([module_code, current_ay+" Sem 2",
                                               target_ay+" Sem 2", "Mounted"])

        return modified_modules


    def GET(self):
        '''
            Renders the modified modules page if users requested
            for the page through the GET method.
        '''
        if SESSION['id'] != web.ACCOUNT_LOGIN_SUCCESSFUL:
            raise web.seeother('/login')

        # User can select the type of modified information they want to see
        # By default, the page will show ALL modified modules
        modify_type = None
        try:
            input_data = web.input()
            modify_type = input_data.modifyType
        except Exception:
            modify_type = "all"

        modified_modules = None
        if modify_type == "mounting":
            modified_modules = self.get_modules_with_modified_mounting()
        elif modify_type == "quota":
            modified_modules = self.get_modules_with_modified_quota()

        return RENDER.moduleModified_stub(modify_type, modified_modules)


    def POST(self):
        '''
            Directs users to the page for tentative module mountings.

            This method is invoked when users click on the button
            to navigate to the tentative module mountings, that is
            present in other valid pages.
        '''
        raise web.seeother('/moduleMountingTentative')
