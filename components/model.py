'''
    model.py
    Acts as a facade for database.py and helper.py
'''

from components import database, helper

INDEX_FIRST_ELEM = 0
INDEX_SECOND_ELEM = 1
LENGTH_EMPTY = 0


######################################################################################
# Functions that query general module information
######################################################################################

def get_all_modules():
    return database.get_all_modules()


def get_module(code):
    return database.get_module(code)


def get_module_name(code):
    return database.get_module_name(code)


def is_existing_module(code):
    return database.is_existing_module(code)


def get_original_module_info(code):
    return database.get_original_module_info(code)


def get_new_modules():
    return database.get_new_modules()


######################################################################################
# Functions that add/modify/delete general module information
######################################################################################

def add_module(code, name, description, module_credits, status):
    return database.add_module(code, name, description, module_credits, status)


def update_module(code, name, description, module_credits):
    return database.update_module(code, name, description, module_credits)


def delete_module(code):
    return database.delete_module(code)


def store_original_module_info(code, name, description, module_credits):
    return database.store_original_module_info(code, name, description, module_credits)


def remove_original_module_info(code):
    return database.remove_original_module_info(code)


######################################################################################
# Functions that query mounting and/or quota information
######################################################################################

def get_all_fixed_mounted_modules():
    return database.get_all_fixed_mounted_modules()


def get_all_tenta_mounted_modules():
    return database.get_all_tenta_mounted_modules()


def get_all_tenta_mounted_modules_of_selected_ay(selected_ay):
    return database.get_all_tenta_mounted_modules_of_selected_ay(selected_ay)


def get_fixed_mounting_and_quota(code):
    return database.get_fixed_mounting_and_quota(code)


def get_tenta_mounting_and_quota(code):
    return database.get_tenta_mounting_and_quota(code)


def get_mounting_of_target_fixed_ay_sem(code, ay_sem):
    return database.get_mounting_of_target_fixed_ay_sem(code, ay_sem)


def get_mounting_of_target_tenta_ay_sem(code, ay_sem):
    return database.get_mounting_of_target_tenta_ay_sem(code, ay_sem)


def get_quota_of_target_fixed_ay_sem(code, ay_sem):
    return database.get_quota_of_target_fixed_ay_sem(code, ay_sem)


def get_quota_of_target_tenta_ay_sem(code, ay_sem):
    return database.get_quota_of_target_tenta_ay_sem(code, ay_sem)


def get_mod_specified_class_size(given_aysem, quota_lower, quota_higher):
    return database.get_mod_specified_class_size(given_aysem, quota_lower, quota_higher)


######################################################################################
# Functions that add/modify/delete mounting and/or quota information
######################################################################################

def add_fixed_mounting(code, ay_sem, quota):
    return database.add_fixed_mounting(code, ay_sem, quota)


def delete_fixed_mounting(code, ay_sem):
    return database.delete_fixed_mounting(code, ay_sem)


def delete_all_fixed_mountings(code):
    return database.delete_all_fixed_mountings(code)


def add_tenta_mounting(code, ay_sem, quota):
    return database.add_tenta_mounting(code, ay_sem, quota)


def update_quota(code, ay_sem, quota):
    return database.update_quota(code, ay_sem, quota)


def delete_tenta_mounting(code, ay_sem):
    return database.delete_tenta_mounting(code, ay_sem)


def delete_all_tenta_mountings(code):
    return database.delete_all_tenta_mountings(code)


######################################################################################
# Functions that query AY and semester information
######################################################################################

def get_current_ay():
    return database.get_current_ay()


def get_next_ay(ay):
    return helper.get_next_ay(ay)


def get_number_of_ay_in_system():
    return helper.get_number_of_ay_in_system()


def get_all_fixed_ay_sems():
    return database.get_all_fixed_ay_sems()


def get_all_tenta_ay_sems():
    return database.get_all_tenta_ay_sems()


def get_all_ay_sems():
    return helper.get_all_ay_sems()


def get_all_future_ay_sems():
    return helper.get_all_future_ay_sems()


def is_aysem_in_list(given_aysem, given_list):
    return helper.is_aysem_in_list(given_aysem, given_list)


def is_aysem_in_system(ay_sem):
    return helper.is_aysem_in_system(ay_sem)


def is_aysem_in_system_and_is_future(ay_sem):
    return helper.is_aysem_in_system_and_is_future(ay_sem)


######################################################################################
# Functions that query information related to students demand for a module
######################################################################################

def get_number_students_planning(code):
    return database.get_number_students_planning(code)


def get_number_of_students_taking_module_in_ay_sem(module_code, ay_sem):
    return database.get_number_of_students_taking_module_in_ay_sem(module_code, ay_sem)


def get_list_students_take_module(code, aysem):
    return database.get_list_students_take_module(code, aysem)


def get_oversub_mod():
    return database.get_oversub_mod()


def get_quota_in_aysem(ay_sem, aysem_quota_merged_list):
    return helper.get_quota_in_aysem(ay_sem, aysem_quota_merged_list)


######################################################################################
# Functions that query general student enrollment information
######################################################################################

def get_all_focus_areas():
    return database.get_all_focus_areas()


def get_num_students_by_yr_study():
    return database.get_num_students_by_yr_study()


def append_missing_year_of_study(initial_table):
    return helper.append_missing_year_of_study(initial_table)


def get_num_students_by_focus_area_non_zero():
    return database.get_num_students_by_focus_area_non_zero()


def get_focus_areas_with_no_students_taking():
    return database.get_focus_areas_with_no_students_taking()


def get_number_students_without_focus_area():
    return database.get_number_students_without_focus_area()


def get_num_students_by_focus_areas():
    return database.get_num_students_by_focus_areas()


######################################################################################
# Functions that add/modify/delete student or student plans
######################################################################################

def add_student(student_id, year_of_study):
    return database.add_student(student_id, year_of_study)


def delete_student(student_id):
    return database.delete_student(student_id)


def add_student_plan(student_id, is_taken, module_code, ay_sem):
    return database.add_student_plan(student_id, is_taken, module_code, ay_sem)


def delete_student_plan(student_id, module_code, ay_sem):
    return database.delete_student_plan(student_id, module_code, ay_sem)


def delete_all_plans_of_student(student_id):
    return database.delete_all_plans_of_student(student_id)


def add_student_focus_area(student_id, focus_area_1, focus_area_2):
    return database.add_student_focus_area(student_id, focus_area_1, focus_area_2)


def delete_student_focus_area(student_id):
    return database.delete_student_focus_area(student_id)


######################################################################################
# Functions that retrieve information of modules that are modified
######################################################################################

def get_modules_with_modified_details():
    return database.get_modules_with_modified_details()


def get_modules_with_modified_quota():
    return database.get_modules_with_modified_quota()


######################################################################################
# Functions that query information involving module relations
######################################################################################

def get_mod_taken_together_with(code):
    return database.get_mod_taken_together_with(code)


def get_mod_taken_together_with_mod_and_aysem(code, aysem):
    return database.get_mod_taken_together_with_mod_and_aysem(code, aysem)


def get_all_mods_taken_together():
    return database.get_all_mods_taken_together()


def get_modA_taken_prior_to_modB():
    return database.get_modA_taken_prior_to_modB()


def get_number_of_students_who_took_modA_prior_to_modB(module_A, module_B,
                                                       module_B_ay_sem):
    return database.get_number_of_students_who_took_modA_prior_to_modB(module_A, module_B,
                                                                       module_B_ay_sem)


def get_mod_before_intern(ay_sem):
    return database.get_mod_before_intern(ay_sem)


def get_mods_no_one_take(aysem):
    return database.get_mods_no_one_take(aysem)


######################################################################################
# Functions that query prerequisite or preclusion information
######################################################################################

def get_prerequisite(module_code):
    return database.get_prerequisite(module_code)


def get_prerequisite_as_string(module_code):
    return helper.get_prerequisite_as_string(module_code)


def get_preclusion(module_code):
    return database.get_preclusion(module_code)


def get_preclusion_as_string(module_code):
    return helper.get_preclusion_as_string(module_code)


def convert_list_of_prereqs_to_string(prereq_list):
    return helper.convert_list_of_prereqs_to_string(prereq_list)


def convert_list_prereq_to_or_string(temp_list, to_add_brackets=True):
    return helper.convert_list_prereq_to_or_string(temp_list, to_add_brackets=to_add_brackets)


def process_and_relation_prereq(existing_string, prereq_of_or_string):
    return helper.process_and_relation_prereq(existing_string, prereq_of_or_string)


######################################################################################
# Functions that add/modify/delete prerequisite or preclusion information
######################################################################################

def add_prerequisite(module_code, prereq_code, index):
    return database.add_prerequisite(module_code, prereq_code, index)


def delete_prerequisite(module_code, prereq_code):
    return database.delete_prerequisite(module_code, prereq_code)


def add_preclusion(module_code, preclude_code):
    return database.add_preclusion(module_code, preclude_code)


def delete_preclusion(module_code, prereq_code):
    return database.delete_preclusion(module_code, prereq_code)


######################################################################################
# Functions that are related to starred modules
######################################################################################

def star_module(module_code, staff_id):
    return database.star_module(module_code, staff_id)


def unstar_module(module_code, staff_id):
    return database.unstar_module(module_code, staff_id)


def get_starred_modules(staff_id):
    return database.get_starred_modules(staff_id)


def is_module_starred(module_code, staff_id):
    return database.is_module_starred(module_code, staff_id)


######################################################################################
# Functions that are related to managing user (admin) accounts and the login system
######################################################################################

def add_admin(username, salt, hashed_pass):
    return database.add_admin(username, salt, hashed_pass)


def is_userid_taken(userid):
    return database.is_userid_taken(userid)


def delete_admin(username):
    return database.delete_admin(username)


def validate_admin(username, unhashed_pass):
    return database.validate_admin(username, unhashed_pass)


def add_session(username, session_salt):
    return database.add_session(username, session_salt)


def validate_session(username, session_id):
    return database.validate_session(username, session_id)


def clean_old_sessions(date_to_delete):
    return database.clean_old_sessions(date_to_delete)


######################################################################################
# Function that validates input that are used to query or modify the database
######################################################################################

def validate_input(input_data, input_types, is_future=False,
                   aysem_specific=True, attr_required=True, show_404=True):
    return helper.validate_input(input_data, input_types, is_future=is_future,
                                 aysem_specific=aysem_specific, attr_required=attr_required,
                                 show_404=show_404)


######################################################################################
# General helper functions that are used by other functions
######################################################################################

def convert_to_list(table):
    return helper.convert_to_list(table)


def replace_null_with_dash(table):
    return helper.replace_null_with_dash(table)
