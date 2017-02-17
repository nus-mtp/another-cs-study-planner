'''
    This module contains the handler for web requests pertaining to
    tentative module mountings.
'''


from app import RENDER
import web
from components import model


class Tentative(object):
    '''
        This class contains the implementations of the GET and POST
        requests.
    '''
    def __init__(self):
        '''
            Full_mounting_plan is a list of 'subplans'
            Each subplan is a list of 4 attributes (code, name, sem 1 mounting, sem 2 mounting)
            Sem 1 & sem 2 mounting have 3 possible values (-1, 0, 1)
            -1 = not mounted; 0 = unmounted; 1 = mounted
        '''
        self.full_mounting_plan = []


    def populate_module_code_and_name(self):
        '''
            Populate full mounting plan with subplans
            Populate each subplan with module code and name
        '''
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
        mounted_module_infos = model.get_all_tenta_mounted_modules_of_selected_ay(selected_ay)
        subplan_index = 0
        curr_subplan = self.full_mounting_plan[subplan_index]

        for info in mounted_module_infos:
            code = info[0]
            curr_module_code = curr_subplan[0]
            while code != curr_module_code:
                subplan_index += 1
                curr_subplan = self.full_mounting_plan[subplan_index]
                curr_module_code = curr_subplan[0]
            ay_sem = info[2]
            sem = ay_sem[9:14]
            if sem == "Sem 1":
                curr_subplan[2] = 1
            elif sem == "Sem 2":
                curr_subplan[3] = 1


    def GET(self):
        '''
            Renders the tentative mounting page if users requested
            for the page through the GET method.
        '''
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
