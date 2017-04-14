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
    def GET(self, *test_data):
        '''
            Renders the oversubscribed modules page if users requested
            for the page through the GET method.
        '''
        web.header('X-Frame-Options', 'SAMEORIGIN')
        web.header('X-Content-Type-Options', 'nosniff')
        web.header('X-XSS-Protection', '1')
        if test_data:
            target_ay_sem = test_data[0]
        else:
            if not session.validate_session():
                raise web.seeother('/login')

            input_data = model.validate_input(web.input(), ["aysem"],
                                              aysem_specific=False, attr_required=False)
            try:
                target_ay_sem = input_data.aysem
            except AttributeError:
                target_ay_sem = model.get_current_ay_sem()

        all_ay_sems = model.get_all_ay_sems()

        #list_of_oversub_mod = model.get_oversub_mod()
        list_of_oversub_mod = []

        current_ay = model.get_current_ay()
        if target_ay_sem[0:8] == current_ay:

            fixed_mounting_handler = Fixed()
            fixed_mounting_handler.GET(to_render=False, logged_in=True)
            full_mounting_plan = fixed_mounting_handler.full_mounting_plan

            if target_ay_sem[9:15] == "Sem 1":
                for subplan in full_mounting_plan:
                    module_code = subplan[0]
                    module_name = subplan[1]
                    sem1_quota = subplan[4]
                    sem1_num_students = subplan[6]
                    if ((sem1_quota != '?' and sem1_quota != '-') \
                        and sem1_num_students > sem1_quota) \
                        or ((sem1_quota == '?' or sem1_quota == '-') and sem1_num_students > 0):
                        if sem1_quota == '?' or sem1_quota == '-':
                            oversub_amount = sem1_num_students
                        else:
                            oversub_amount = sem1_num_students - sem1_quota
                        list_of_oversub_mod.append((module_code, module_name, target_ay_sem,
                                                    sem1_quota, sem1_num_students, oversub_amount))

            else:
                for subplan in full_mounting_plan:
                    module_code = subplan[0]
                    module_name = subplan[1]
                    sem2_quota = subplan[5]
                    sem2_num_students = subplan[7]
                    if ((sem2_quota != '?' and sem2_quota != '-') \
                        and sem2_num_students > sem2_quota) \
                        or ((sem2_quota == '?' or sem2_quota == '-') and sem2_num_students > 0):
                        if sem2_quota == '?' or sem2_quota == '-':
                            oversub_amount = sem2_num_students
                        else:
                            oversub_amount = sem2_num_students - sem2_quota
                        list_of_oversub_mod.append((module_code, module_name, target_ay_sem,
                                                    sem2_quota, sem2_num_students, oversub_amount))

        else:
            tenta_mounting_handler = Tentative()
            tenta_mounting_handler.GET(to_render=False, logged_in=True)
            full_mounting_plan = tenta_mounting_handler.full_mounting_plan

            if target_ay_sem[9:15] == "Sem 1":
                for subplan in full_mounting_plan:
                    module_code = subplan[0]
                    module_name = subplan[1]
                    sem1_quota = subplan[4]
                    sem1_num_students = subplan[6]
                    if ((sem1_quota != '?' and sem1_quota != '-') \
                        and sem1_num_students > sem1_quota) \
                        or ((sem1_quota == '?' or sem1_quota == '-') and sem1_num_students > 0):
                        if sem1_quota == '?' or sem1_quota == '-':
                            oversub_amount = sem1_num_students
                        else:
                            oversub_amount = sem1_num_students - sem1_quota
                        list_of_oversub_mod.append((module_code, module_name, target_ay_sem,
                                                    sem1_quota, sem1_num_students, oversub_amount))

            else:
                for subplan in full_mounting_plan:
                    module_code = subplan[0]
                    module_name = subplan[1]
                    sem2_quota = subplan[5]
                    sem2_num_students = subplan[7]
                    if ((sem2_quota != '?' and sem2_quota != '-') \
                        and sem2_num_students > sem2_quota) \
                        or ((sem2_quota == '?' or sem2_quota == '-') and sem2_num_students > 0):
                        if sem2_quota == '?' or sem2_quota == '-':
                            oversub_amount = sem2_num_students
                        else:
                            oversub_amount = sem2_num_students - sem2_quota
                        list_of_oversub_mod.append((module_code, module_name, target_ay_sem,
                                                    sem2_quota, sem2_num_students, oversub_amount))

        if not test_data:
            return RENDER.oversubscribedModules(list_of_oversub_mod, all_ay_sems, target_ay_sem)
        else:
            return list_of_oversub_mod
