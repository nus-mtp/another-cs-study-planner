'''
    This module contains the handler for web requests pertaining to
    fixed module mountings.
'''


from app import RENDER
import web
from components import model


class Fixed(object):
    '''
        This class contains the implementations of the GET and POST requests.
        It generates a full mounting plan that states whether each module is
        mounted or not mounted in a semester of the current AY.
    '''
    def __init__(self):
        '''
            Full_mounting_plan is a list of 'subplans'
            Each subplan is a list of 4 attributes (code, name, sem 1 mounting, sem 2 mounting)
            For fixed mountings, each mounting has 2 possible values (-1 or 1)
            -1 = not mounted; 1 = mounted
        '''
        self.full_mounting_plan = []


    def get_current_ay(self):
        '''
            All fixed mountings should be from the same AY,
            so just get the AY from the first entry
            Test case will ensure that all entries in fixed mountings have the same AY
        '''
        return model.get_first_fixed_mounting()[0][0:8]


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


    def populate_mounting_values(self):
        '''
            Populate each subplan with sem 1 and sem 2 mounting values
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
            if sem == "Sem 1":
                curr_subplan[2] = 1
            elif sem == "Sem 2":
                curr_subplan[3] = 1

        self.full_mounting_plan = full_mounting_plan


    def GET(self):
        '''
            Renders the fixed mounting page if users requested
            for the page through the GET method.
        '''
        self.populate_module_code_and_name()
        self.populate_mounting_values()
        current_ay = self.get_current_ay()

        return RENDER.moduleMountingFixed_updated(current_ay, self.full_mounting_plan)


    def POST(self):
        '''
            Directs users to the page for fixed module mountings.

            This method is invoked when users click on the button
            to navigate to the fixed module mountings, that is
            present in other valid pages.
        '''
        raise web.seeother('/moduleMountingFixed')
