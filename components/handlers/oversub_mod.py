'''
    This module contains the handler for web requests pertaining to
    the list of oversubscribed modules.
'''


from app import RENDER
import web
from components import model, session
from components.handlers.fixed_module_mountings import Fixed
from components.handlers.tentative_module_mountings import Tentative


class OversubModule(object):
    '''
        This class contains the implementations of the GET
        requests.
    '''
    def GET(self):
        '''
            Renders the oversubscribed modules page if users requested
            for the page through the GET method.
        '''
        if not session.validate_session():
            raise web.seeother('/login')

        #list_of_oversub_mod = model.get_oversub_mod()
        list_of_oversub_mod = []

        fixed_mounting_handler = Fixed()
        fixed_mounting_handler.GET(to_render=False)
        full_mounting_plan = fixed_mounting_handler.full_mounting_plan

        current_ay = model.get_current_ay()
        for subplan in full_mounting_plan:
            module_code = subplan[0]
            module_name = subplan[1]
            sem1_quota = subplan[4]
            sem2_quota = subplan[5]
            sem1_num_students = subplan[6]
            sem2_num_students = subplan[7]

            if ((sem1_quota != '?' and sem1_quota != '-') and sem1_num_students > sem1_quota) \
                or ((sem1_quota == '?' or sem1_quota == '-') and sem1_num_students > 0):
                if sem1_quota == '?' or sem1_quota == '-':
                    oversub_amount = sem1_num_students
                else:
                    oversub_amount = sem1_num_students - sem1_quota
                list_of_oversub_mod.append((module_code, module_name, current_ay+" Sem 1", 
                                            sem1_quota, sem1_num_students, oversub_amount))
            if ((sem2_quota != '?' and sem2_quota != '-') and sem2_num_students > sem2_quota) \
                or ((sem2_quota == '?' or sem2_quota == '-') and sem2_num_students > 0):
                if sem2_quota == '?' or sem2_quota == '-':
                    oversub_amount = sem2_num_students
                else:
                    oversub_amount = sem2_num_students - sem2_quota
                list_of_oversub_mod.append((module_code, module_name, current_ay+" Sem 2", 
                                            sem2_quota, sem2_num_students, oversub_amount))

        tenta_mounting_handler = Tentative()
        tenta_mounting_handler.GET(to_render=False)
        full_mounting_plan = tenta_mounting_handler.full_mounting_plan

        next_ay = model.get_next_ay(current_ay)
        for subplan in full_mounting_plan:
            module_code = subplan[0]
            module_name = subplan[1]
            sem1_quota = subplan[4]
            sem2_quota = subplan[5]
            sem1_num_students = subplan[6]
            sem2_num_students = subplan[7]
            if ((sem1_quota != '?' and sem1_quota != '-') and sem1_num_students > sem1_quota) \
                or ((sem1_quota == '?' or sem1_quota == '-') and sem1_num_students > 0):
                if sem1_quota == '?' or sem1_quota == '-':
                    oversub_amount = sem1_num_students
                else:
                    oversub_amount = sem1_num_students - sem1_quota
                list_of_oversub_mod.append((module_code, module_name, next_ay+" Sem 1", 
                                            sem1_quota, sem1_num_students, oversub_amount))
            if ((sem2_quota != '?' and sem2_quota != '-') and sem2_num_students > sem2_quota) \
                or ((sem2_quota == '?' or sem2_quota == '-') and sem2_num_students > 0):
                if sem2_quota == '?' or sem2_quota == '-':
                    oversub_amount = sem2_num_students
                else:
                    oversub_amount = sem2_num_students - sem2_quota
                list_of_oversub_mod.append((module_code, module_name, next_ay+" Sem 2", 
                                            sem2_quota, sem2_num_students, oversub_amount))

        return RENDER.oversubscribedModules(list_of_oversub_mod)
