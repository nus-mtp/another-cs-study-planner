'''
test_list_students_take_mod.py
Contains test cases for querying list of students who plan to take a certain mod
in a specified semester
'''

from nose.tools import assert_equal
from components import model

# HOW TO RUN NOSE TESTS
# 1. Make sure you are in cs-modify main directory
# 2. Make sure the path "C:\Python27\Scripts" is added in your environment variables
# 3. Enter in cmd: "nosetests test/"
# 4. Nose will run all the tests inside the test/ folder

class TestCode(object):
    '''
        This class runs the test cases for querying list of students who plan
        to take a certain mod in a specified semester
    '''
    def __init__(self):
        pass


    def test_list_students_take_module_one_focus(self):
        '''
            Tests querying the list of students who plan
            to take a certain mod in a specified semester,
            where these students only have one focus area.
        '''
        # Add some modules and dummy students
        model.add_student('dummyYr1A', 1)
        model.add_student_focus_area('dummyYr1A', 'Database Systems', None)
        model.add_student_plan('dummyYr1A', True, 'CS1010', 'AY 16/17 Sem 1')

        list_of_students_take_mod = \
            model.get_list_students_take_module('CS1010', 'AY 16/17 Sem 1')

        required_entry = ['dummyYr1A', 1, 'Database Systems', '-']

        # Clean up database
        model.delete_all_plans_of_student('dummyYr1A')
        model.delete_student('dummyYr1A')
        model.delete_student_focus_area('dummyYr1A')

        assert required_entry in list_of_students_take_mod


    def test_list_students_take_module_two_focus(self):
        '''
            Tests querying the list of students who plan
            to take a certain mod in a specified semester,
            where these students have exactly 2 focus areas.
        '''

        # Add some modules and dummy students
        model.add_student('dummyYr1A', 1)
        model.add_student_focus_area('dummyYr1A', 'Database Systems', 'Computer Graphics and Games')
        model.add_student_plan('dummyYr1A', True, 'CS1010', 'AY 16/17 Sem 1')

        list_of_students_take_mod = \
            model.get_list_students_take_module('CS1010', 'AY 16/17 Sem 1')

        required_entry = ['dummyYr1A', 1, 'Database Systems', 'Computer Graphics and Games']

        # Clean up database
        model.delete_all_plans_of_student('dummyYr1A')
        model.delete_student('dummyYr1A')
        model.delete_student_focus_area('dummyYr1A')

        assert required_entry in list_of_students_take_mod


    def test_list_students_take_module_empty(self):
        '''
            Tests querying the list of students who plan
            to take a certain mod in a specified semester,
            where these are no students planning to take the module.
        '''
        model.add_module('AAA1111', 'Dummy Module', 'Description', 4, 'Active')
        
        list_of_students_take_mod = \
            model.get_list_students_take_module('AAA1111', 'AY 17/18 Sem 1')

        required_list = []

        # Clean up database
        model.delete_module('AAA1111')

        assert_equal(len(list_of_students_take_mod), len(required_list))
        assert_equal(sorted(list_of_students_take_mod), sorted(required_list))
