'''
    This module contains the handler for web requests pertaining to
    showing the number of students who have taken module A
    prior to taking module B
'''


from app import RENDER
import web
from components import model, session
from components.handlers.outcome import Outcome


class TakePriorTo(object):
    '''
        This class contains the implementations of the GET
        requests.
    '''
    def __init__(self):
        '''
            Define the number of future AYs that will be included
            By right, this value should be set by the superadmin
        '''
        self.number_of_future_ays = 1


    def get_next_ay(self, ay):
        '''
            Return the AY that comes after the given AY
        '''
        ay = ay.split(' ')[1].split('/')
        return 'AY ' + str(int(ay[0])+1) + '/' + str(int(ay[1])+1)


    def GET(self):
        '''
            Retrieve and display the pairs of modules that have
            at least 1 student who has taken module A
            prior to taking module B
        '''
        if not session.validate_session():
            raise web.seeother('/login')

        module_pairs = model.get_modA_taken_prior_to_modB()

        # Get a list of all AY-Sems (for users to select)
        current_ay = model.get_current_ay()
        all_ay_sems = [current_ay+" Sem 1", current_ay+" Sem 2"]
        target_ay = current_ay
        for i in range(self.number_of_future_ays):
            future_ay = self.get_next_ay(target_ay)
            all_ay_sems.append(future_ay+" Sem 1")
            all_ay_sems.append(future_ay+" Sem 2")

        return RENDER.modulesTakenPriorToOthers(module_pairs, all_ay_sems, None, None,
                                                None, None, None, None)


    def POST(self, *test_data):
        '''
            Retrieve and display the total number of students who have taken module A
            prior to taking module B (in a target AY-Sem)

            Also shows the student count for each AY-Sem that module A is taken in
        '''
        is_testing = (len(test_data) > 0)
        if is_testing:
            module_A = test_data[0]
            module_B = test_data[1]
            target_ay_sem = test_data[2]
        else:
            data = web.input()
            try:
                module_A = data.moduleA
                module_B = data.moduleB
                target_ay_sem = data.aySem
            except AttributeError:
                raise web.seeother("/moduleTakenPriorToOthers")

        # Check if module codes entered are valid
        module_data = model.get_module(module_A.upper())
        if module_data is None:
            return Outcome().POST("get_module", False, module_A)
        module_data = model.get_module(module_B.upper())
        if module_data is None:
            return Outcome().POST("get_module", False, module_B)

        student_counts = model.get_number_of_students_who_took_modA_prior_to_modB(module_A.upper(),
                                                                                  module_B.upper(),
                                                                                  target_ay_sem)
        students_in_module_B = model.get_number_of_students_taking_module(module_B.upper(),
                                                                          target_ay_sem)

        student_prior_count = 0
        for count in student_counts:
            count = count[1]
            student_prior_count += count

        if is_testing:
            return [student_counts, student_prior_count, students_in_module_B]
        else:
            return RENDER.modulesTakenPriorToOthers(None, None, student_counts,
                                                    student_prior_count, module_A.upper(),
                                                    module_B.upper(), target_ay_sem,
                                                    students_in_module_B)
