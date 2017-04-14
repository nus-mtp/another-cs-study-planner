'''
    This module contains the handler for web requests pertaining to
    a module's mounting for a particular AY/Sem
'''


from app import RENDER
import web
from components import model, session


class IndividualModule(object):
    '''
        This class handles the display of a single module mounting
    '''
    def __init__(self):
        '''
            Define the AY-Sems that are in the system
            By right, these settings hould be set by the superadmin
        '''
        self.mounting_status = -1
        self.quota = None
        self.is_current_ay = False

        self.focus_areas = None
        self.focus_area_acronyms = None
        self.focus_area_counts = None
        self.student_year_counts = None


    def load_mounting_info(self, module_code, ay_sem):
        '''
            Load the mounting status and quota of the target module and AY/Sem
        '''
        fixed_mounting_status = -1
        fixed_quota = None
        is_current_ay = False

        # Get mounting status and quota in current AY
        target_ay = ay_sem[0:8]
        current_ay = model.get_current_ay()
        if target_ay == current_ay:
            is_current_ay = True
            fixed_mounting_status = model.get_mounting_of_target_fixed_ay_sem(module_code, ay_sem)
            fixed_quota = model.get_quota_of_target_fixed_ay_sem(module_code, ay_sem)
        else:
            target_sem = ay_sem[9:14]
            fixed_mounting_status = model.get_mounting_of_target_fixed_ay_sem(module_code,
                                                                              current_ay+" "
                                                                              +target_sem)
            fixed_quota = model.get_quota_of_target_fixed_ay_sem(module_code,
                                                                 current_ay+" "+target_sem)

        if fixed_quota is False:
            fixed_quota = '-'

        if is_current_ay:
            if fixed_mounting_status is True:
                self.mounting_status = 1
            else:
                self.mounting_status = -1
            self.quota = fixed_quota

        else:
            # Get mounting status and quota in target (future) AY
            tenta_mounting_status = model.get_mounting_of_target_tenta_ay_sem(module_code, ay_sem)
            tenta_quota = model.get_quota_of_target_tenta_ay_sem(module_code, ay_sem)

            if tenta_quota is False:
                tenta_quota = '-'
            self.quota = tenta_quota

            if tenta_mounting_status is True:
                self.mounting_status = 1
            else:
                if fixed_mounting_status is True:
                    self.mounting_status = 0
                else:
                    self.mounting_status = -1

        self.is_current_ay = is_current_ay


    def get_overlapping_mods(self, code):
        '''
            Get modules that over lap with this module
        '''
        return model.get_mod_taken_together_with(code)


    def get_mounting_status(self):
        '''
            Return the mounting status of the module in the target AY-Sem
        '''
        return self.mounting_status


    def get_quota(self):
        '''
            Return the quota of the module in the target AY-Sem
        '''
        return self.quota


    def get_acronym(self, focus_area):
        '''
            Return the acronym of a focus area
        '''
        focus_area_words = focus_area.split(" ")
        focus_area_acronym = ""
        for word in focus_area_words:
            first_letter = word[0]
            if first_letter == "&":
                continue
            focus_area_acronym += first_letter
        return focus_area_acronym


    def load_focus_areas(self):
        '''
            Retrieve the list of focus areas and the list of their acronyms
        '''
        focus_areas = model.get_all_focus_areas()
        focus_areas = sorted([area[0] for area in focus_areas])
        focus_area_counts = {"Nil": 0}
        focus_area_acronyms = ["Nil"]
        for focus_area in focus_areas:
            acronym = self.get_acronym(focus_area)
            focus_area_counts[acronym] = 0
            focus_area_acronyms.append(acronym)
        focus_areas.insert(0, "Have Not Indicated")

        self.focus_areas = focus_areas
        self.focus_area_acronyms = focus_area_acronyms
        self.focus_area_counts = focus_area_counts


    def load_student_enrollments(self, module_code, ay_sem):
        '''
            Retrieve the number of students in each year of study,
            and the number of students in each focus area,
            that are taking this module
        '''
        student_list = model.get_list_students_take_module(module_code, ay_sem)
        student_year_counts = [0] * 6

        for student in student_list:
            # Get number of students in each year that are taking the module
            student_year = student[1]
            student_year_counts[student_year-1] += 1

            # Get number of students in each focus area that are taking the module
            focus_area_1 = student[2]
            focus_area_2 = student[3]
            if focus_area_1 == "-" and focus_area_2 == "-":
                self.focus_area_counts["Nil"] += 1
            else:
                if focus_area_1 != "-":
                    self.focus_area_counts[self.get_acronym(focus_area_1)] += 1
                if focus_area_2 != "-":
                    self.focus_area_counts[self.get_acronym(focus_area_2)] += 1

        self.student_year_counts = student_year_counts


    def GET(self):
        '''
            Retrieve and render all the info of a module mounting
        '''
        web.header('X-Frame-Options', 'SAMEORIGIN')
        web.header('X-Content-Type-Options', 'nosniff')
        web.header('X-XSS-Protection', '1')
        if not session.validate_session():
            raise web.seeother('/login')

        input_data = model.validate_input(web.input(), ["code", "aysem"])
        module_code = input_data.code
        ay_sem = input_data.aysem

        # Get module's name, description, MC and status
        module_info = model.get_module(module_code)

        # Get mounting status, quota and number of students taking
        self.load_mounting_info(module_code, ay_sem)
        student_count = model.get_number_of_students_taking_module_in_ay_sem(module_code,
                                                                             ay_sem)

        # Check if the selected AY-Sem is in the current AY
        # (To determine whether to display the 'Edit Specific Info' button)
        is_future_ay = not self.is_current_ay

        # Check if module is starred
        is_starred = model.is_module_starred(module_code, web.cookies().get('user'))

        # Get the year of study and focus area distriubtions of students taking the module
        # (To be rendered as charts)
        self.load_focus_areas()
        self.load_student_enrollments(module_code, ay_sem)

        all_ay_sems = model.get_all_ay_sems()
        all_future_ay_sems = model.get_all_future_ay_sems()

        return RENDER.individualModuleInfo(module_info, all_ay_sems, all_future_ay_sems,
                                           is_future_ay, ay_sem, self.mounting_status,
                                           self.quota, student_count, is_starred,
                                           self.focus_areas, self.focus_area_acronyms,
                                           self.student_year_counts, self.focus_area_counts)
