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

        list_of_students_take_mod = \
            model.get_list_students_take_module('CS1010', 'AY 16/17 Sem 1')

        required_list = [('D1000002A', 1, 'Database Systems', '-'),
                         ('D1000000A', 1, 'Artificial Intelligence', '-'),
                         ('D1000001A', 1, 'Computer Graphics and Games', '-')
                        ]

        assert_equal(len(list_of_students_take_mod), len(required_list))
        assert_equal(sorted(list_of_students_take_mod), sorted(required_list))


    def test_list_students_take_module_two_focus(self):
        '''
            Tests querying the list of students who plan
            to take a certain mod in a specified semester,
            where these students have exactly 2 focus areas.
        '''

        list_of_students_take_mod = \
            model.get_list_students_take_module('CS4244', 'AY 16/17 Sem 2')

        required_list = [('D4000000A', 4, 'Artificial Intelligence',
                          'Computer Graphics and Games')
                        ]

        assert_equal(len(list_of_students_take_mod), len(required_list))
        assert_equal(sorted(list_of_students_take_mod), sorted(required_list))


    def test_list_students_take_module_empty(self):
        '''
            Tests querying the list of students who plan
            to take a certain mod in a specified semester,
            where these are no students planning to take the module.
        '''

        list_of_students_take_mod = \
            model.get_list_students_take_module('CS2108', 'AY 17/18 Sem 1')

        required_list = []

        assert_equal(len(list_of_students_take_mod), len(required_list))
        assert_equal(sorted(list_of_students_take_mod), sorted(required_list))
