'''
    This module contains the handler for web requests pertaining to the
    'Edit All Mountings and Quotas' page
'''


from app import RENDER
import web
from components import model, session
from components.handlers.tentative_module_mountings import Tentative
from components.handlers.outcome import Outcome


class EditAll(object):
    '''
        This class contains the implementations of the GET and POST requests.
        for the 'Edit All Mountings and Quotas' page
    '''
    def GET(self):
        '''
            Renders the 'Edit All Mountings and Quotas' page if users requested
            for the page through the GET method.
        '''
        web.header('X-Frame-Options', 'SAMEORIGIN')
        web.header('X-Content-Type-Options', 'nosniff')
        web.header('X-XSS-Protection', '1')
        if not session.validate_session():
            raise web.seeother('/login')

        # Currently, tentative mounting will be shown for the next AY
        selected_ay = model.get_next_ay(model.get_current_ay())

        tenta_mounting_handler = Tentative()
        tenta_mounting_handler.populate_module_code_and_name()
        tenta_mounting_handler.populate_module_ay_sem_data(selected_ay)
        full_mounting_plan = tenta_mounting_handler.full_mounting_plan
        full_mounting_plan = model.replace_empty_quota_with_symbols(full_mounting_plan)

        return RENDER.editAll(selected_ay, full_mounting_plan)


    def POST(self, *test_data):
        '''
            Handles the editing operations for all mountings and quotas
        '''
        if test_data:
            input_data = test_data[0]
        else:
            input_data = web.input()
        all_modules = model.get_all_modules()
        target_ay = model.get_next_ay(model.get_current_ay())

        for module in all_modules:
            module_code = module[0]
            try:
                is_module_edited = input_data[module_code+"_isEdited"]
            except KeyError:
                is_module_edited = "False"

            if is_module_edited == "True":
                try:
                    sem1_mounting = input_data[module_code+"_Sem1Mounting"]
                    sem1_mounting = True
                except KeyError:
                    sem1_mounting = False
                try:
                    sem2_mounting = input_data[module_code+"_Sem2Mounting"]
                    sem2_mounting = True
                except KeyError:
                    sem2_mounting = False

                try:
                    sem1_quota = input_data[module_code+"_Sem1Quota"]
                    if sem1_quota == "":  # quota = '?'
                        sem1_quota = None
                except KeyError:  # quota = '-'
                    sem1_quota = None
                if sem1_quota is not None:
                    try:
                        sem1_quota = int(sem1_quota)
                        if sem1_quota < 0 or sem1_quota > 999:
                            if test_data:
                                return False
                            else:
                                return Outcome().POST("edit_all_mountings_and_quotas", False, None)
                    except ValueError:  # quota is not an integer
                        if test_data:
                            return False
                        else:
                            return Outcome().POST("edit_all_mountings_and_quotas", False, None)

                try:
                    sem2_quota = input_data[module_code+"_Sem2Quota"]
                    if sem2_quota == "":  # quota = '?'
                        sem2_quota = None
                except KeyError:  # quota = '-'
                    sem2_quota = None
                if sem2_quota is not None:
                    try:
                        sem2_quota = int(sem2_quota)
                        if sem2_quota < 0 or sem2_quota > 999:
                            if test_data:
                                return False
                            else:
                                return Outcome().POST("edit_all_mountings_and_quotas", False, None)
                    except ValueError:  # quota is not an integer
                        if test_data:
                            return False
                        else:
                            return Outcome().POST("edit_all_mountings_and_quotas", False, None)

                target_aysem = target_ay+" Sem 1"
                outcome = None
                if sem1_mounting is True:
                    old_mounting = model.get_mounting_of_target_tenta_ay_sem(module_code,
                                                                             target_aysem)
                    if old_mounting is True:
                        outcome = model.update_quota(module_code,
                                                     target_aysem, sem1_quota)
                    else:
                        outcome = model.add_tenta_mounting(module_code,
                                                           target_aysem, sem1_quota)
                else:
                    outcome = model.delete_tenta_mounting(module_code, target_aysem)
                if outcome is False:
                    return Outcome().POST("edit_all_mountings_and_quotas", False, None)

                target_aysem = target_ay+" Sem 2"
                outcome = None
                if sem2_mounting is True:
                    old_mounting = model.get_mounting_of_target_tenta_ay_sem(module_code,
                                                                             target_aysem)
                    if old_mounting is True:
                        outcome = model.update_quota(module_code,
                                                     target_aysem, sem2_quota)
                    else:
                        outcome = model.add_tenta_mounting(module_code,
                                                           target_aysem, sem2_quota)
                else:
                    outcome = model.delete_tenta_mounting(module_code, target_aysem)
                if outcome is False:
                    return Outcome().POST("edit_all_mountings_and_quotas", False, None)

        if not test_data:
            return Outcome().POST("edit_all_mountings_and_quotas", True, None)
