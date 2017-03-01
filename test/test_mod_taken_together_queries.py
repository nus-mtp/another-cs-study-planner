'''
test_mod_taken_together_queries.py
Contains test cases for querying modules taken together in the same semester
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
        This class runs the test cases for querying modules
        taken together in the same semester
    '''
    def __init__(self):
        pass


    def test_query_module_taken_together_specified_mod(self):
        '''
            Tests querying the list of modules taken together
            with specified module in the same semester
        '''

        list_of_mod_taken_together = \
            model.get_mod_taken_together_with('CS1010')

        required_list = [('CS1010', 'CS1231', 'AY 16/17 Sem 1', 3),
                         ('CS1010', 'CS2105', 'AY 16/17 Sem 1', 2),
                         ('CS1010', 'CS2106', 'AY 16/17 Sem 1', 1)]

        assert_equal(len(list_of_mod_taken_together), len(required_list))
        assert_equal(list_of_mod_taken_together, required_list)

        list_of_mod_taken_together = \
            model.get_mod_taken_together_with('CS2105')

        required_list = [('CS2105', 'CS1231', 'AY 16/17 Sem 1', 2),
                         ('CS2105', 'CS1010', 'AY 16/17 Sem 1', 2)]

        assert_equal(len(list_of_mod_taken_together), len(required_list))
        assert_equal(sorted(list_of_mod_taken_together), sorted(required_list))
