'''
    This module contains the handler for web requests pertaining to
    a module's information overview.
'''


from app import RENDER, SESSION
import web
from components import model


class ViewMod(object):
    '''
        This class handles the display of a single module
    '''
    def __init__(self):
        '''
            The mounting plan of a module contains its info for EVERY AY/Sem
            Each row in the mounting plan has 4 attributes:
            0: AY/Sem, 1: Mounting value, 2: Quota, 3: No. of students taking/planning to take
        '''
        self.fixed_mounting_plan = None
        self.tenta_mounting_plan = None


    def load_fixed_mounting_plan(self, module_code):
        '''
            Loads the fixed mounting plan of the single module
        '''
        fixed_mounting_and_quota = model.get_fixed_mounting_and_quota(module_code)
        fixed_ay_sems = model.get_all_fixed_ay_sems()
        fixed_mounting_plan = []

        for ay_sem in fixed_ay_sems:
            # AY/Sem is marked as 'not mounted' by default
            ay_sem = ay_sem[0]
            ay_sem_plan = [ay_sem, -1, "-"]

            # Mark AY/Sems that module is mounted in
            for mounting in fixed_mounting_and_quota:
                mounted_ay_sem = mounting[0]
                quota = mounting[1]
                if ay_sem == mounted_ay_sem:
                    ay_sem_plan[1] = 1
                    ay_sem_plan[2] = quota
                    break
            fixed_mounting_plan.append(ay_sem_plan)

        self.fixed_mounting_plan = fixed_mounting_plan


    def load_tenta_mounting_plan(self, module_code):
        '''
            Loads the tentative mounting plan of the single module
        '''
        tenta_mounting_and_quota = model.get_tenta_mounting_and_quota(module_code)
        tenta_ay_sems = model.get_all_tenta_ay_sems()
        tenta_mounting_plan = []

        for ay_sem in tenta_ay_sems:
            # AY/Sem is marked as 'not mounted' by default
            ay_sem = ay_sem[0]
            ay_sem_plan = [ay_sem, -1, "-"]

            # Mark AY/Sems that module is mounted in
            for mounting in tenta_mounting_and_quota:
                mounted_ay_sem = mounting[0]
                quota = mounting[1]
                if ay_sem == mounted_ay_sem:
                    ay_sem_plan[1] = 1
                    ay_sem_plan[2] = quota
                    break

            # Mark AY/Sems that module is unmounted from
            # (i.e. mounted in fixed AY, but will no longer be mounted in tentative AY)
            fixed_sem_1_mounting_value = self.fixed_mounting_plan[0][1]
            fixed_sem_2_mounting_value = self.fixed_mounting_plan[1][1]
            tenta_mounting_value = ay_sem_plan[1]
            if ay_sem[9:14] == "Sem 1":
                if fixed_sem_1_mounting_value == 1 and tenta_mounting_value == -1:
                    ay_sem_plan[1] = 0
            elif ay_sem[9:14] == "Sem 2":
                if fixed_sem_2_mounting_value == 1 and tenta_mounting_value == -1:
                    ay_sem_plan[1] = 0
            tenta_mounting_plan.append(ay_sem_plan)

        self.tenta_mounting_plan = tenta_mounting_plan

    def get_overlapping_mods(self,code):
        '''
            Get modules that over lap with this module
        '''
        return model.get_mod_taken_together_with(code)

    def GET(self):
        '''
            Retrieve and render all the info of a module
        '''
        if SESSION['id'] != web.ACCOUNT_LOGIN_SUCCESSFUL:
            raise web.seeother('/login')
        input_data = web.input()
        module_code = input_data.code
        module_info = model.get_module(module_code)
        self.load_fixed_mounting_plan(module_code)
        self.load_tenta_mounting_plan(module_code)
        number_of_student_planning = model.get_number_students_planning(module_code)
        system_message = SESSION['editModMsg']
        overlapping_modules_list = self.get_overlapping_mods(module_code)
        SESSION['editModMsg'] = None

        #get html of overlapping modules template

        return RENDER.viewModule(module_info, self.fixed_mounting_plan,
                                 self.tenta_mounting_plan, number_of_student_planning,
                                 system_message, overlapping_modules_list)


    def POST(self):
        ''' Redirect '''
        raise web.seeother('/viewModule')
