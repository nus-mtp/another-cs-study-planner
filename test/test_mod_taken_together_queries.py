'''
test_mod_taken_together_queries.py
Contains test cases for querying modules taken together in the same semester
'''

from nose.tools import assert_equal, assert_true
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


    def test_query_module_taken_together_specified_mod(self):
        '''
            Tests querying the list of modules taken together
            with specified module in the same semester
        '''
        # Add some dummy students and modules
        model.add_student('dummyYr1A', 1)
        model.add_module('AAA1111', 'Dummy 1', 'Description', 4, 'Active')
        model.add_module('AAA1112', 'Dummy 2', 'Description', 4, 'Active')
        model.add_student_plan('dummyYr1A', True, 'AAA1111', 'AY 17/18 Sem 2')
        model.add_student_plan('dummyYr1A', True, 'AAA1112', 'AY 17/18 Sem 2')

        list_of_mod_taken_together = \
            model.get_mod_taken_together_with('AAA1111')

        # Clean up database
        model.delete_all_plans_of_student('dummyYr1A')
        model.delete_module('AAA1111')
        model.delete_module('AAA1112')
        model.delete_student('dummyYr1A')

        assert ('AAA1111', 'Dummy 1', 'AAA1112',
                'Dummy 2', 'AY 17/18 Sem 2', 1) in list_of_mod_taken_together


    def test_query_module_taken_together_sorted(self):
        '''
            Tests querying the list of modules taken together
            with specified module in the same semester
            returns a list sorted by number of students
            in non-ascending order.
        '''

        list_of_mod_taken_together = \
            model.get_mod_taken_together_with('CS1010')

        assert_true(self.is_count_in_non_ascending_order(list_of_mod_taken_together))


    def test_query_module_taken_together_specified_mod_specified_aysem(self):
        '''
            Tests querying the list of modules taken together
            with specified module in the specified semester
        '''

        # Add some dummy students and modules
        model.add_student('dummyYr1A', 1)
        model.add_module('AAA1111', 'Dummy 1', 'Description', 4, 'Active')
        model.add_module('AAA1112', 'Dummy 2', 'Description', 4, 'Active')
        model.add_student_plan('dummyYr1A', True, 'AAA1111', 'AY 17/18 Sem 2')
        model.add_student_plan('dummyYr1A', True, 'AAA1112', 'AY 17/18 Sem 2')

        list_of_mod_taken_together = \
            model.get_mod_taken_together_with_mod_and_aysem('AAA1111', 'AY 17/18 Sem 2')

        required_list = [('AAA1111', 'Dummy 1', 'AAA1112', 'Dummy 2', 1)]

        assert_equal(len(list_of_mod_taken_together), len(required_list))
        assert_equal(sorted(list_of_mod_taken_together), sorted(required_list))
        assert_true(self.is_count_in_non_ascending_order(list_of_mod_taken_together))

        # Clean up database
        model.delete_all_plans_of_student('dummyYr1A')
        model.delete_module('AAA1111')
        model.delete_module('AAA1112')
        model.delete_student('dummyYr1A')


    def test_empty_query_module_taken_together_specified_mod_specified_aysem(self):
        '''
            Tests querying the list of modules taken together
            with specified module in the specified semester
            for non-existent module
        '''
        list_of_mod_taken_together = \
            model.get_mod_taken_together_with_mod_and_aysem('AAA1111', 'AY 17/18 Sem 1')

        required_list = []

        assert_equal(len(list_of_mod_taken_together), len(required_list))
        assert_equal(sorted(list_of_mod_taken_together), sorted(required_list))
        assert_true(self.is_count_in_non_ascending_order(list_of_mod_taken_together))


    def test_query_module_taken_together_entire_list(self):
        '''
            Tests querying the list of modules taken together
            in the same semester
        '''
        # Add some dummy students and modules
        model.add_student('dummyYr1A', 1)
        model.add_module('AAA1111', 'Dummy 1', 'Description', 4, 'Active')
        model.add_module('AAA1112', 'Dummy 2', 'Description', 4, 'Active')
        model.add_module('AAA1113', 'Dummy 3', 'Description', 4, 'Active')
        model.add_student_plan('dummyYr1A', True, 'AAA1111', 'AY 17/18 Sem 1')
        model.add_student_plan('dummyYr1A', True, 'AAA1112', 'AY 17/18 Sem 1')
        model.add_student_plan('dummyYr1A', True, 'AAA1112', 'AY 17/18 Sem 2')
        model.add_student_plan('dummyYr1A', True, 'AAA1113', 'AY 17/18 Sem 2')

        list_of_mod_taken_together = \
            model.get_all_mods_taken_together()

        assert_true(self.is_count_in_non_ascending_order(list_of_mod_taken_together))

        assert ('AAA1111', 'Dummy 1', 'AAA1112',
                'Dummy 2', 'AY 17/18 Sem 1', 1) in list_of_mod_taken_together
        assert ('AAA1112', 'Dummy 2', 'AAA1113',
                'Dummy 3', 'AY 17/18 Sem 2', 1) in list_of_mod_taken_together

        # Clean up database
        model.delete_all_plans_of_student('dummyYr1A')
        model.delete_module('AAA1111')
        model.delete_module('AAA1112')
        model.delete_module('AAA1113')
        model.delete_student('dummyYr1A')


    def is_count_in_non_ascending_order(self, list_of_mods):
        '''
            Returns true if the last item in each row of given list
            are arranged in non-ascending order.
            Returns false otherwise
        '''

        num_of_items = len(list_of_mods)

        # when there is 0 or 1 item in the list, it is always in
        # non-ascending order.
        if num_of_items <= 1:
            return True

        first_row = list_of_mods[0]
        num_of_cols = len(first_row)
        last_param = num_of_cols - 1

        previous_item = first_row[last_param]

        for row_number in range(1, num_of_items):
            current_row = list_of_mods[row_number]
            current_item = current_row[last_param]

            if current_item > previous_item:
                return False
            else:
                previous_item = current_item

        return True
