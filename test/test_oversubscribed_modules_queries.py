'''
test_oversubscribed_modules_queries.py
Contains test cases for oversubscribed modules query related functions.
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
        This class runs the test cases for oversubscribed modules
        query related functions.
    '''
    def __init__(self):
        pass


    def test_query_oversubscribed_modules(self):
        '''
            Tests querying the list of oversubscribed modules.

            Note to developers: Please check that you have repopulated
            your database if this test fails.
        '''
        # To simulate an oversubscribed module, add a module with 0 quota,
        # then add a student who wants to take the module.
        model.add_student('D9818873B', 1)
        model.add_module('AAA1111', 'Test Module', 'Description', 4, 'Active')
        model.add_student_plan('D9818873B', False, 'AAA1111', 'AY 17/18 Sem 1')

        list_of_oversub_mod = model.get_oversub_mod()
        oversubscribed_module = ('AAA1111', 'Test Module',
                          'AY 17/18 Sem 1', '?', 1)

        # Clean up the database
        model.delete_all_plans_of_student('D9818873B')
        model.delete_module("AAA1111")
        model.delete_student('D9818873B')

        # Test for presence of oversubscribed module
        assert oversubscribed_module in list_of_oversub_mod
