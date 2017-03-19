'''
test_functions_in_test_mod_associated_with_mod.py
Contains test cases for testing the equality check functions found in the file
test_mod_associated_with_mod.py
'''

from nose.tools import assert_true, assert_false
import test_mod_associated_with_mod as file_to_test

class TestCode(object):
    '''
        This class runs the test cases for testing the equality check functions found
        in the file test_mod_associated_with_mod.py
    '''
    def __init__(self):
        pass


    def test_functions_in_file_test_mod_associated_with_mod(self):
        '''
            This function tests if equality function in test_mod_associated_with_mod.py
            is working properly or not.
        '''
        assert_true(file_to_test.is_prereq_equal("C and (A or B)", "C and (B or A)"))
        assert_true(file_to_test.is_prereq_equal("A", "A"))
        assert_true(file_to_test.is_prereq_equal("A or B or C", "B or A or C"))
        assert_true(file_to_test.is_prereq_equal("A and B", "B and A"))
        assert_true(file_to_test.is_prereq_equal("C and (A or B)", "(A or B) and C"))
        assert_true(file_to_test.is_prereq_equal("C and (A or B)", "(B or A) and C"))
        assert_false(file_to_test.is_prereq_equal("C and (A or B)", "(B or C) and C"))
        assert_true(file_to_test.is_prereq_equal("(C or D) and (A or B)", "(B or A) and (D or C)"))
        assert_false(file_to_test.is_prereq_equal("C and (A or B)", "(A or B)"))
        assert_false(file_to_test.is_prereq_equal("C and (A or B)", "A or B"))
        assert_false(file_to_test.is_prereq_equal("C", "B"))
        assert_false(file_to_test.is_prereq_equal("C", "B and C"))
        assert_false(file_to_test.is_prereq_equal("C", "B or C"))
        assert_false(file_to_test.is_prereq_equal("C or A", "C and A"))
