'''
    helper.py
    Contains functions that process and/or manipulate data that are OUTSIDE the database
'''

## Prevent model.py from being imported twice
from sys import modules
try:
    from components import model
except ImportError:
    model = modules['components.model']

import web
from app import RENDER

INDEX_FIRST_ELEM = 0
INDEX_SECOND_ELEM = 1
LENGTH_EMPTY = 0

# Currently, the system only has data for AY 16/17 and AY 17/18
NUMBER_OF_AY_IN_SYSTEM = 2


######################################################################################
# Functions that are realted to AY and semester information
######################################################################################

def get_next_ay(ay):
    '''
        Return the AY that comes after the given AY
    '''
    ay = ay.split(' ')[1].split('/')
    return 'AY ' + str(int(ay[0])+1) + '/' + str(int(ay[1])+1)


def get_number_of_ay_in_system():
    '''
        Return the number of AY in the system
    '''
    return NUMBER_OF_AY_IN_SYSTEM


def get_all_ay_sems(ay_count=NUMBER_OF_AY_IN_SYSTEM):
    '''
        Returns all the AY-Sems in the system
    '''
    current_ay = model.get_current_ay()
    ay_sems_in_system = [current_ay+" Sem 1", current_ay+" Sem 2"]
    target_ay = current_ay
    for i in range(ay_count-1):
        target_ay = get_next_ay(target_ay)
        ay_sems_in_system.append(target_ay+" Sem 1")
        ay_sems_in_system.append(target_ay+" Sem 2")
    return ay_sems_in_system


def get_all_future_ay_sems(ay_count=NUMBER_OF_AY_IN_SYSTEM):
    '''
        Returns all the FUTURE AY-Sems in the system
    '''
    future_ay_sems_in_system = []
    target_ay = model.get_current_ay()
    for i in range(ay_count-1):
        target_ay = get_next_ay(target_ay)
        future_ay_sems_in_system.append(target_ay+" Sem 1")
        future_ay_sems_in_system.append(target_ay+" Sem 2")
    return future_ay_sems_in_system


def is_aysem_in_list(given_aysem, given_list):
    '''
        Returns true if given_aysem is found inside given_list.
        Example:
        given_list is a list of [('AY 16/17 Sem 1',), ('AY 16/17 Sem 2',)] structure.
    '''
    for aysem_tuple in given_list:
        retrieved_aysem = aysem_tuple[0]
        if given_aysem == retrieved_aysem:
            return True

    return False


def is_aysem_in_system(ay_sem):
    '''
        Returns the AY-Sem if given AY-Sem is found inside the system, otherwise return False
    '''
    ay_sems_in_system = get_all_ay_sems()

    valid_aysem = False
    for i in range(len(ay_sems_in_system)):
        if ay_sem.upper() == ay_sems_in_system[i].upper():
            valid_aysem = ay_sems_in_system[i]
            break
    return valid_aysem


def is_aysem_in_system_and_is_future(ay_sem):
    '''
        Returns the aysem if given aysem is found inside the system AND is a future AY-Sem,
        otherwise return False
    '''
    future_ay_sems_in_system = get_all_future_ay_sems()

    valid_future_aysem = False
    for i in range(len(future_ay_sems_in_system)):
        if ay_sem.upper() == future_ay_sems_in_system[i].upper():
            valid_future_aysem = future_ay_sems_in_system[i]
            break
    return valid_future_aysem


######################################################################################
# Functions that are related to mounting and/or quota information
######################################################################################

def get_quota_in_aysem(ay_sem, aysem_quota_merged_list):
    '''
        This is a helper function.
        Retrieves the correct quota from ay_sem listed inside
        aysem_quota_merged_list parameter.
    '''
    for aysem_quota_pair in aysem_quota_merged_list:
        aysem_in_pair = aysem_quota_pair[0]
        if ay_sem == aysem_in_pair:
            quota_in_pair = aysem_quota_pair[1]

            return quota_in_pair

    return None # quota not found in list


######################################################################################
# Functions that are related to general student enrollment information
######################################################################################

def append_missing_year_of_study(initial_table):
    '''
        Helper function to append missing years of study to the
        given initial table.
        initial_table given in lists of (year, number of students)
        pair.
        e.g. If year 5 is missing from table, appends (5,0) to table
        and returns the table
    '''
    MAX_POSSIBLE_YEAR = 6
    for index in range(0, MAX_POSSIBLE_YEAR):
        year = index + 1
        year_exists_in_table = False

        for year_count_pair in initial_table:
            req_year = year_count_pair[0]
            if req_year == year:
                year_exists_in_table = True
                break

        if not year_exists_in_table:
            initial_table.append((year, 0))

    return initial_table


######################################################################################
# Functions that are related to prerequisite or preclusion information
######################################################################################

def get_prerequisite_as_string(module_code):
    '''
        Returns a string of pre-requisites of specified module_code
    '''
    prerequisites = model.get_prerequisite(module_code)
    prereq_list = convert_to_list(prerequisites)

    # sort list of lists based on index (which is the first elem of each row)
    prereq_list.sort(key=lambda row: row[INDEX_FIRST_ELEM])

    prereq_string = convert_list_of_prereqs_to_string(prereq_list)

    return prereq_string


def get_preclusion_as_string(module_code):
    '''
        Returns a string of preclusions of specified module_code
    '''
    preclusions = model.get_preclusion(module_code)
    preclude_list = convert_to_list(preclusions)
    processed_list = [preclude[INDEX_FIRST_ELEM] for preclude in preclude_list]

    preclude_string = ", ".join(processed_list)

    return preclude_string


def convert_list_of_prereqs_to_string(prereq_list):
    '''
        Converts given list of lists (prereq_list) into string form of prereqs.
        Pre-condition: Given list must have the rows' first index sorted.
        Example: [['0', 'CS1010'], ['0', 'CS1231'], ['1', 'CS2105']] will yield
        the string (CS1010 or CS1231) and CS2105.
        Same index elements have an "OR" relationship, different index elements
        have an "AND" relationship.
    '''
    number_of_prereq = len(prereq_list)
    if number_of_prereq == LENGTH_EMPTY:
        return ""

    required_string = ""
    temp_list_for_or = list()
    previous_index = None
    for prereq_with_index in prereq_list:
        current_index = prereq_with_index[INDEX_FIRST_ELEM]
        current_prereq = prereq_with_index[INDEX_SECOND_ELEM]

        if previous_index is None:
            previous_index = current_index
            temp_list_for_or.append(current_prereq)
        else:
            if previous_index == current_index:
                temp_list_for_or.append(current_prereq)
            else:
                prereq_of_or_string = convert_list_prereq_to_or_string(temp_list_for_or)
                required_string = process_and_relation_prereq(required_string,
                                                              prereq_of_or_string)
                previous_index = current_index
                temp_list_for_or = [current_prereq]

    if len(required_string) == LENGTH_EMPTY:
        # there is no 'and' relation
        prereq_of_or_string = convert_list_prereq_to_or_string(temp_list_for_or,
                                                               False)
        required_string = prereq_of_or_string
    else:
        # there is 'and' relation to process
        prereq_of_or_string = convert_list_prereq_to_or_string(temp_list_for_or)
        required_string = process_and_relation_prereq(required_string,
                                                      prereq_of_or_string)

    return required_string


def convert_list_prereq_to_or_string(temp_list, to_add_brackets=True):
    '''
        Converts all elements in temp_list to a string separated by "or"
    '''
    number_of_prereq = len(temp_list)
    if number_of_prereq == 1:
        return temp_list[INDEX_FIRST_ELEM]
    else:
        # more than 1 prereq
        required_string = " or ".join(temp_list)

        if to_add_brackets:
            required_string_with_brackets = "(" + required_string + ")"

            return required_string_with_brackets
        else:
            return required_string


def process_and_relation_prereq(existing_string, prereq_of_or_string):
    '''
        Appends the prereq_of_or_string into existing_string by building
        "and" relations between existing prereqs in existing_string
        with those in prereq_of_or_string
    '''
    existing_string_length = len(existing_string)

    if existing_string_length == LENGTH_EMPTY:
        return prereq_of_or_string
    else:
        and_string = " and "
        required_string = existing_string + and_string + prereq_of_or_string

        return required_string


######################################################################################
# Function that validates input that are used to query or modify the database
######################################################################################

def validate_input(input_data, input_types, is_future=False,
                   aysem_specific=True, attr_required=True):
    '''
        Validates that the GET input data (in the URL) is valid.

        input_types indicate the list of data types to validate.
        e.g. if GET input contains 'code' and 'aysem', then input_types = ["code", "aysem"]

        An input is considered valid if:
        1) The value was specified and
        2) The value exists in the system
        If any input is invalid, return 404 page.
    '''
    if attr_required is False and len(input_data) == 0:
        return input_data

    for input_type in input_types:
        if input_type == "code":
            try:
                module_code = input_data.code
            except AttributeError:
                error = RENDER.notfound('Module code is not specified')
                raise web.notfound(error)
            module_exist = model.is_existing_module(module_code.upper())
            if not module_exist:
                error = RENDER.notfound('Module code "' + module_code +\
                                        '" does not exist in our system')
                raise web.notfound(error)
            else:
                input_data.code = module_code.upper()

        elif input_type == "aysem":
            try:
                ay_sem = input_data.aysem
            except AttributeError:
                if aysem_specific:
                    error = RENDER.notfound('AY-Semester is not specified')
                    raise web.notfound(error)
                else:
                    continue

            if is_future:
                valid_aysem = is_aysem_in_system_and_is_future(ay_sem)
            else:
                valid_aysem = is_aysem_in_system(ay_sem)

            if not valid_aysem:
                if is_future:
                    error = RENDER.notfound('AY-Semester "' + ay_sem +\
                                            '" does not exist in our system,' +\
                                            ' or is not in a future AY')
                else:
                    error = RENDER.notfound('AY-Semester "' + ay_sem +\
                                            '" does not exist in our system')
                raise web.notfound(error)
            else:
                input_data.aysem = valid_aysem

        elif input_type == "modify_type" or input_type == "restore_type":
            try:
                if input_type == "modify_type":
                    info_type = input_data.modifyType
                else:
                    info_type = input_data.restoreType
            except AttributeError:
                if input_type == "modify_type":
                    error = RENDER.notfound('Modify type is not specified')
                else:
                    error = RENDER.notfound('Restore type is not specified')
                raise web.notfound(error)
            valid_info_type = info_type.upper() == "QUOTA" or \
                              info_type.upper() == "MOUNTING" or \
                              info_type.upper() == "MODULEDETAILS"
            if not valid_info_type:
                if input_type == "modify_type":
                    error = RENDER.notfound('Modify type "' + info_type +\
                                            '" is not recognised by the system')
                else:
                    error = RENDER.notfound('Restore type "' + info_type +\
                                            '" is not recognised by the system')
                raise web.notfound(error)

        elif input_type == "moduleA" or input_type == "moduleB":
            try:
                if input_type == "moduleA":
                    module_code = input_data.moduleA
                else:
                    module_code = input_data.moduleB
            except AttributeError:
                error = RENDER.notfound("Module " + input_type[-1] +\
                                        "'s code is not specified")
                raise web.notfound(error)
            module_exist = model.is_existing_module(module_code.upper())
            if not module_exist:
                error = RENDER.notfound('Module code "' + module_code +\
                                        '" does not exist in our system')
                raise web.notfound(error)
            else:
                input_data.code = module_code.upper()

    return input_data


######################################################################################
# General helper functions that are used by other functions
######################################################################################

def convert_to_list(table):
    '''
        Converts a list of tuples to a list of lists.
    '''
    converted_table = list()

    for row in table:
        conveted_list = list(row)
        converted_table.append(conveted_list)

    return converted_table


def replace_null_with_dash(table):
    '''
        Changes all the NULL values found in the table to '-'
        This function supports a 2D table.
    '''
    table = convert_to_list(table)

    for row in table:
        row_length = len(row)
        for col in range(row_length):
            if row[col] is None:
                row[col] = '-'

    return table