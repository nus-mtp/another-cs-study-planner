'''
    This module contains the handler for web requests pertaining to
    showing the number of students who have taken module A
    prior to taking module B
'''


from app import RENDER
import web
from components import model, session


class TakePriorTo(object):
    '''
        This class contains the implementations of the GET
        requests.
    '''
    def GET(self, *test_data):
        '''
            Retrieve and display the pairs of modules that have
            at least 1 student who has taken module A
            prior to taking module B
        '''
        is_testing = (len(test_data) > 0)
        if is_testing:
            module_A = test_data[0]
            module_B = test_data[1]
            target_ay_sem = test_data[2]
        else:
            if not session.validate_session():
                raise web.seeother('/login')
            input_data = model.validate_input(web.input(), ["moduleA", "moduleB", "aysem"],
                                              aysem_specific=False, attr_required=False)

            target_ay_sem = None
            try:
                target_ay_sem = input_data.aysem
                module_A = input_data.moduleA
                module_B = input_data.moduleB            
            except AttributeError:
                module_pairs = None
                if target_ay_sem is not None:
                    module_pairs = model.get_modA_taken_prior_to_modB(target_ay_sem)

                # Get a list of all AY-Sems (for users to select)
                all_ay_sems = model.get_all_ay_sems()

                return RENDER.modulesTakenPriorToOthers("all_pairs", module_pairs, all_ay_sems, None, None,
                                                        None, None, target_ay_sem, None)


        student_counts = \
                         model.get_number_of_students_who_took_modA_prior_to_modB(module_A.upper(),
                                                                                  module_B.upper(),
                                                                                  target_ay_sem)
        module_B_students = \
                            model.get_number_of_students_taking_module_in_ay_sem(module_B.upper(),
                                                                                 target_ay_sem)

        student_prior_count = 0
        for count in student_counts:
            count = count[1]
            student_prior_count += count

        if is_testing:
            return [student_counts, student_prior_count, module_B_students]
        else:
            return RENDER.modulesTakenPriorToOthers("specific_pair", None, None, student_counts,
                                                    student_prior_count, module_A.upper(),
                                                    module_B.upper(), target_ay_sem,
                                                    module_B_students)
