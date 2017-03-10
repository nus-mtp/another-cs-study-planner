'''
test_modules_no_one_take.py
Contains test cases for querying list of pair of modules which no student plan to take together
in the same semester
'''

from nose.tools import assert_false
from components import model

# HOW TO RUN NOSE TESTS
# 1. Make sure you are in cs-modify main directory
# 2. Make sure the path "C:\Python27\Scripts" is added in your environment variables
# 3. Enter in cmd: "nosetests test/"
# 4. Nose will run all the tests inside the test/ folder

class TestCode(object):
    '''
        This class runs the test cases for querying list of pair of modules which no
        student plan to take together in the same semester
    '''

    def __init__(self):
        pass


    def test_list_modules_no_one_take(self):
        '''
            Tests querying the list of pair of modules which no
            student plan to take together in the same semester
        '''

        list_of_modules_no_one_take = model.get_mods_no_one_take()
        list_of_modules_taken_together = model.get_all_mods_taken_together()

        # Mods that are taken together should be complement of
        # mods which are not taken together
        for row in list_of_modules_taken_together:
            first_mod = row[0]
            second_mod = row[1]
            aysem = row[2]

            module_pair_aysem = (first_mod, second_mod, aysem)

            assert_false(module_pair_aysem in list_of_modules_no_one_take)

            alternate_module_pair_aysem = (second_mod, first_mod, aysem)

            assert_false(alternate_module_pair_aysem in list_of_modules_no_one_take)
