'''
    This module contains the handler for web requests pertaining to
    fixed module mountings.
'''


from app import RENDER
import web
from components import model, session


class Fixed(object):
    '''
        This class contains the implementations of the GET and POST requests.
        It generates a full mounting plan that states whether each module is
        mounted or not mounted in a semester of the current AY.
    '''
    def __init__(self):
        '''
            Full_mounting_plan is a list of 'subplans'
            Each subplan is a list of 9 attributes
            (code, name, sem 1 mounting, sem 2 mounting,
            sem 1 quota, sem 2 quota, number of students taking in sem 1,
            number of students taking in sem 2, status)
            For fixed mountings, each mounting has 2 possible values (-1 or 1)
            -1 = not mounted; 1 = mounted
        '''
        self.full_mounting_plan = []


    def populate_module_code_and_name(self):
        '''
            Populate full mounting plan with subplans
            Populate each subplan with module code and name
        '''
        del self.full_mounting_plan[:]
        module_infos = model.get_all_modules()
        for info in module_infos:
            code = info[0]
            name = info[1]
            status = info[4]
            subplan = ["", "", -1, -1, None, None, 0, 0, ""]
            subplan[0] = code
            subplan[1] = name
            subplan[8] = status
            self.full_mounting_plan.append(subplan)


    def populate_module_ay_sem_data(self):
        '''
            Populate each subplan with sem 1 and sem 2 mounting values, quotas,
            and numbers of students taking
        '''
        full_mounting_plan = self.full_mounting_plan
        mounted_module_infos = model.get_all_fixed_mounted_modules()

        subplan_index = 0
        curr_subplan = full_mounting_plan[subplan_index]

        for info in mounted_module_infos:
            code = info[0]
            curr_module_code = curr_subplan[0]
            while code != curr_module_code:
                subplan_index += 1
                curr_subplan = full_mounting_plan[subplan_index]
                curr_module_code = curr_subplan[0]
            ay_sem = info[2]
            sem = ay_sem[9:14]
            quota = info[3]
            if sem == "Sem 1":
                curr_subplan[2] = 1
                curr_subplan[4] = quota
            elif sem == "Sem 2":
                curr_subplan[3] = 1
                curr_subplan[5] = quota

        student_stats = model.get_student_stats_for_all_mods()

        subplan_index = 0
        curr_subplan = full_mounting_plan[subplan_index]
        current_ay = model.get_current_ay()

        for stat in student_stats:
            code = stat[1]
            curr_module_code = curr_subplan[0]
            while code != curr_module_code:
                subplan_index += 1
                curr_subplan = full_mounting_plan[subplan_index]
                curr_module_code = curr_subplan[0]
            ay_sem = stat[2]
            number_of_students = stat[0]
            if ay_sem == current_ay+" Sem 1":
                curr_subplan[6] = number_of_students
            elif ay_sem == current_ay+" Sem 2":
                curr_subplan[7] = number_of_students

        self.full_mounting_plan = full_mounting_plan


    def GET(self, to_render=True, logged_in=False):
        '''
            Renders the fixed mounting page if users requested
            for the page through the GET method.
        '''
        if not session.validate_session() and not logged_in:
            raise web.seeother('/login')

        self.populate_module_code_and_name()
        self.populate_module_ay_sem_data()
        current_ay = model.get_current_ay()

        full_mounting_plan = self.full_mounting_plan
        # New modules will not be displayed in fixed mounting
        full_mounting_plan = [subplan for subplan in full_mounting_plan 
                              if subplan[8].rstrip() == "Active"]
        full_mounting_plan = model.replace_empty_quota_with_symbols(full_mounting_plan)
        if to_render:
            return RENDER.moduleMountingFixed(current_ay, full_mounting_plan)
        else:
            self.full_mounting_plan = full_mounting_plan


    def POST(self):
        '''
            Directs users to the page for fixed module mountings.

            This method is invoked when users click on the button
            to navigate to the fixed module mountings, that is
            present in other valid pages.
        '''
        raise web.seeother('/moduleMountingFixed')
