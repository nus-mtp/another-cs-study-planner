'''
    This module contains the handler for web requests pertaining to
    tentative module mountings.
'''


from app import RENDER, SESSION
import web
from components import model
from components.handlers.fixed_module_mountings import Fixed


class Tentative(object):
    '''
        This class contains the implementations of the GET and POST requests.
        It generates a full mounting plan that states whether each module is
        mounted or not mounted in a semester of the selected future AY.
    '''
    def __init__(self):
        '''
            Full_mounting_plan is a list of 'subplans'
            Each subplan is a list of 4 attributes (code, name, sem 1 mounting, sem 2 mounting)
            For tentative mountings, each mounting has 3 possible values (-1 or 0 or 1)
            -1 = not mounted; 0 = unmounted; 1 = mounted
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
            subplan = ["", "", -1, -1]
            subplan[0] = code
            subplan[1] = name
            self.full_mounting_plan.append(subplan)


    def populate_mounting_values(self, selected_ay):
        '''
            Populate each subplan with sem 1 and sem 2 mounting values
        '''
        tenta_full_mounting_plan = self.full_mounting_plan
        mounted_module_infos = model.get_all_tenta_mounted_modules_of_selected_ay(selected_ay)
        subplan_index = 0
        curr_subplan = tenta_full_mounting_plan[subplan_index]

        # Mark module that are mounted
        for info in mounted_module_infos:
            code = info[0]
            curr_module_code = curr_subplan[0]
            while code != curr_module_code:
                subplan_index += 1
                curr_subplan = tenta_full_mounting_plan[subplan_index]
                curr_module_code = curr_subplan[0]
            ay_sem = info[2]
            sem = ay_sem[9:14]
            if sem == "Sem 1":
                curr_subplan[2] = 1
            elif sem == "Sem 2":
                curr_subplan[3] = 1

        # Generate full mounting plan for fixed mountings
        fixed_mounting_handler = Fixed()
        fixed_mounting_handler.populate_module_code_and_name()
        fixed_mounting_handler.populate_mounting_values()
        fixed_full_mounting_plan = fixed_mounting_handler.full_mounting_plan

        # Mark module that are unmounted
        # (i.e. mounted in current AY, but will no longer be mounted in future AY)
        for i in range(len(fixed_full_mounting_plan)):
            fixed_subplan = fixed_full_mounting_plan[i]
            tenta_subplan = tenta_full_mounting_plan[i]
            fixed_sem_1_mounting = fixed_subplan[2]
            tenta_sem_1_mounting = tenta_subplan[2]
            fixed_sem_2_mounting = fixed_subplan[3]
            tenta_sem_2_mounting = tenta_subplan[3]
            if fixed_sem_1_mounting == 1 and tenta_sem_1_mounting == -1:
                tenta_full_mounting_plan[i][2] = 0
            if fixed_sem_2_mounting == 1 and tenta_sem_2_mounting == -1:
                tenta_full_mounting_plan[i][3] = 0

        self.full_mounting_plan = tenta_full_mounting_plan


    def GET(self):
        '''
            Renders the tentative mounting page if users requested
            for the page through the GET method.
        '''
        if SESSION['id'] != web.ACCOUNT_LOGIN_SUCCESSFUL:
            raise web.seeother('/login')

        #input_data = web.input()
        #selected_ay = input_data.ay        # User will select the AY that he wants to see
        selected_ay = "AY 17/18"        # Hardcoded for now

        self.populate_module_code_and_name()
        self.populate_mounting_values(selected_ay)

        return RENDER.moduleMountingTentative(selected_ay, self.full_mounting_plan)


    def POST(self):
        '''
            Directs users to the page for tentative module mountings.

            This method is invoked when users click on the button
            to navigate to the tentative module mountings, that is
            present in other valid pages.
        '''
        raise web.seeother('/moduleMountingTentative')
