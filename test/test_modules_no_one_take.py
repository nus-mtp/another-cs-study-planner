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

        list_aysem_to_test = ['AY 16/17 Sem 1', 'AY 16/17 Sem 2', 'AY 17/18 Sem 1',
                              'AY 17/18 Sem 2']

        list_of_modules_taken_together = model.get_all_mods_taken_together()

        for aysem in list_aysem_to_test:
            list_of_modules_no_one_take = model.get_mods_no_one_take(aysem)

            # Mods that are taken together should be complement of
            # mods which are not taken together
            for row in list_of_modules_taken_together:
                first_mod_code = row[0]
                second_mod_code = row[1]
                current_aysem = row[2]
                if current_aysem != aysem:
                    continue

                first_mod_name = model.get_module_name(first_mod_code)
                second_mod_name = model.get_module_name(second_mod_code)

                module_pair = (first_mod_code, first_mod_name, second_mod_code,
                               second_mod_name)

                assert_false(module_pair in list_of_modules_no_one_take)

                alternate_module_pair = (second_mod_code, second_mod_name, first_mod_code,
                                         first_mod_name)

                assert_false(alternate_module_pair in list_of_modules_no_one_take)
