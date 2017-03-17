'''
test_mod_associated_with_mod.py
Contains test cases for querying modules which are associated with other modules.
'''

from nose.tools import assert_true
from components import model

# HOW TO RUN NOSE TESTS
# 1. Make sure you are in cs-modify main directory
# 2. Make sure the path "C:\Python27\Scripts" is added in your environment variables
# 3. Enter in cmd: "nosetests test/"
# 4. Nose will run all the tests inside the test/ folder

class TestCode(object):
    '''
        This class runs the test cases for querying modules
        associated with other modules
    '''
    def __init__(self):
        pass


    def test_query_module_association_prereq_all_or(self):
        '''
            Tests querying the modules prerequisite as a string, where prereq is all 'or'
        '''
        prereq_string = model.get_prerequisite_as_string('CS2010')
        required_prereq_string = "CG1103 or CS1020E or CS1020"

        assert_true(is_prereq_equal(prereq_string, required_prereq_string))


    def test_query_module_association_prereq_mix_or_and(self):
        '''
            Tests querying the modules prerequisite as a string, where prereq is a
            mixture of 'or' and 'and'
        '''
        prereq_string = model.get_prerequisite_as_string('CS3230')
        required_prereq_string = "(MA1100 or CS1231) and CS2010"

        assert_true(is_prereq_equal(prereq_string, required_prereq_string))

        prereq_string = model.get_prerequisite_as_string('CS4222')
        required_prereq_string = "(ST2334 or ST2131) and (EE3204 or CS2105)"

        assert_true(is_prereq_equal(prereq_string, required_prereq_string))


    def test_query_module_association_prereq_all_and(self):
        '''
            Tests querying the modules prerequisite as a string, where prereq is all 'and'
        '''
        prereq_string = model.get_prerequisite_as_string('CS3215')
        required_prereq_string = "CS2103 and CS2301"

        assert_true(is_prereq_equal(prereq_string, required_prereq_string))


    def test_query_module_association_no_prereq(self):
        '''
            Tests querying the modules prerequisite as a string, where there is no
            prereq
        '''
        prereq_string = model.get_prerequisite_as_string('CS1010')
        required_prereq_string = ""

        assert_true(is_prereq_equal(prereq_string, required_prereq_string))


    def test_query_module_association_one_prereq(self):
        '''
            Tests querying the modules prerequisite as a string, where there is
            only one prereq
        '''
        prereq_string = model.get_prerequisite_as_string('CS1020')
        required_prereq_string = "CS1010"

        assert_true(is_prereq_equal(prereq_string, required_prereq_string))


    def test_query_module_association_no_preclusion(self):
        '''
            Tests querying the modules preclusions as a string, where there is
            no preclusions.
        '''
        preclude_string = model.get_preclusion_as_string('CS2104')
        required_preclude_string = ""

        assert_true(is_preclude_equal(preclude_string, required_preclude_string))


    def test_query_module_association_one_preclusion(self):
        '''
            Tests querying the modules preclusions as a string, where there is
            only one preclusion.
        '''
        preclude_string = model.get_preclusion_as_string('CS4213')
        required_preclude_string = "CS3247"

        assert_true(is_preclude_equal(preclude_string, required_preclude_string))


    def test_query_module_association_many_preclusions(self):
        '''
            Tests querying the modules preclusions as a string, where there are
            more than one preclusions.
        '''
        preclude_string = model.get_preclusion_as_string('CS4350')
        required_preclude_string = "CS4204, CS4203"

        assert_true(is_preclude_equal(preclude_string, required_preclude_string))

        preclude_string = model.get_preclusion_as_string('CS4203')
        required_preclude_string = "CS4350, CS3283, CS3284"

        assert_true(is_preclude_equal(preclude_string, required_preclude_string))


# Static methods start here
STRING_AND = "and"
STRING_OR = "or"
STRING_OPEN_BRACKET = "("
STRING_CLOSE_BRACKET = ")"
STRING_COMMA = ","


def is_preclude_equal(preclude1, preclude2):
    '''
        Returns true if given preclude1 is considered to be the same (or
        equivalent) as given preclude2. Returns false otherwise.

        Both precludes are string of modules separated by commas.
    '''
    return is_equal_after_split_and_remove_spaces_and_sort(STRING_COMMA,
                                                           preclude1, preclude2)


def is_prereq_equal(prereq1, prereq2):
    '''
        Returns true if given prereq1 is considered to be the same (or
        equivalent) as given prereq2. Returns false otherwise.

        For example, (A or B) and C is considered to be equivalent to the following:
        C and (A or B)
        C and (B or A)
        (A or B) and C
        (B or A) and C
    '''
    list_of_ands_in_prereq1 = prereq1.split(STRING_AND)
    list_of_ands_in_prereq2 = prereq2.split(STRING_AND)

    if len(list_of_ands_in_prereq1) != len(list_of_ands_in_prereq2):
        return False

    is_preq_accounted_for = [False] * len(list_of_ands_in_prereq2)

    for prereq_component1 in list_of_ands_in_prereq1:
        is_current_component_in_component2 = False

        for index in range(len(list_of_ands_in_prereq2)):
            prereq_component2 = list_of_ands_in_prereq2[index]
            if is_prereq_component_equal(prereq_component1, prereq_component2):
                is_preq_accounted_for[index] = True
                is_current_component_in_component2 = True
                break

        if not is_current_component_in_component2:
            return False

    # Check every prereq component 2 is accounted for.
    for i in range(len(list_of_ands_in_prereq2)):
        if not is_preq_accounted_for[i]:
            return False

    return True


def is_prereq_component_equal(prereq_component1, prereq_component2):
    '''
        Returns true if prereq_component1 is considered to be equivalent to
        prereq_component2. prereq_component consists of module code or module
        codes separated by commas, and enclosed by brackets. There is no
        'AND' in the prereq_component. Returns false otherwise
    '''
    if STRING_OPEN_BRACKET in prereq_component1 and \
        STRING_OPEN_BRACKET in prereq_component2:
        # Both components contain brackets
        component1_without_brackets = remove_brackets(prereq_component1)
        component2_without_brackets = remove_brackets(prereq_component2)

        is_equal = is_equal_after_split_and_remove_spaces_and_sort(
            STRING_OR, component1_without_brackets,
            component2_without_brackets)

        return is_equal
    else:
        # If no brackets are present in either component
        if STRING_OR in prereq_component1 and \
            STRING_OR in prereq_component2:
            is_equal = is_equal_after_split_and_remove_spaces_and_sort(
                STRING_OR, prereq_component1, prereq_component2)

            return is_equal
        elif STRING_AND in prereq_component1 and \
            STRING_AND in prereq_component2:
            is_equal = is_equal_after_split_and_remove_spaces_and_sort(
                STRING_AND, prereq_component1, prereq_component2)

            return is_equal
        else:
            # Both components should be atomic and compared for equality,
            # if one of them is not atomic, they are just not equal
            prereq_component1 = remove_spaces(prereq_component1)
            prereq_component2 = remove_spaces(prereq_component2)
            return prereq_component1 == prereq_component2


def remove_brackets(string_to_remove_brackets):
    '''
        Removes all '(' and ')' brackets from given string.
    '''
    string_to_remove_brackets = \
        string_to_remove_brackets.replace(STRING_OPEN_BRACKET, "")
    string_to_remove_brackets =  \
        string_to_remove_brackets.replace(STRING_CLOSE_BRACKET, "")
    return string_to_remove_brackets


def remove_spaces(string_to_remove_spaces):
    '''
        Trims all spaces from given string
    '''
    string_to_remove_spaces = string_to_remove_spaces.strip(" ")
    return string_to_remove_spaces


def is_equal_after_split_and_remove_spaces_and_sort(split_by, list_1, list_2):
    '''
        Splits both lists by given split_by parameter, and checks if both lists
        contains the same elements (ignore spaces and order of elements)
        Returns true if they are the same and false otherwise.
    '''
    list_1 = list_1.split(split_by)
    list_2 = list_2.split(split_by)

    list_1 = [remove_spaces(component) for component in list_1]
    list_2 = [remove_spaces(component) for component in list_2]

    list_1.sort()
    list_2.sort()

    return list_1 == list_2
