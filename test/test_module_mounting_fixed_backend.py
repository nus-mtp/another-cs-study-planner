'''
test_database.py
Contains test cases for database related functions.
'''
from nose.tools import assert_equal, assert_true
from components.handlers.fixed_module_mountings import Fixed as fixed_module_mountings


class TestCode(object):
    '''
    This class runs the test cases for database related functions.
    '''
    def __init__(self):
        self.fixed_module_mountings = fixed_module_mountings()
        self.fixed_module_mountings.populate_module_code_and_name()
        self.fixed_module_mountings.populate_mounting_values()
        assert_true(len(self.fixed_module_mountings.full_mounting_plan) > 0)


    def test_mounted_in_both_sems(self):
        '''
            Tests that a module that is mounted in both sems
            will have the mounting values '1' and '1'
        '''
        full_mounting_plan = self.fixed_module_mountings.full_mounting_plan
        test_module_code = "CS1010"
        test_module_sem_1 = -2
        test_module_sem_2 = -2
        has_test_module = False

        for subplan in full_mounting_plan:
            if subplan[0] == test_module_code:
                has_test_module = True
                test_module_sem_1 = subplan[2]
                test_module_sem_2 = subplan[3]
                break

        assert_true(has_test_module)
        assert_equal(test_module_sem_1, 1)
        assert_equal(test_module_sem_2, 1)


    def test_mounted_in_sem_1_only(self):
        '''
            Tests that a module that is mounted in sem 1 only
            will have the mounting values '1' and '-1'
        '''
        full_mounting_plan = self.fixed_module_mountings.full_mounting_plan
        test_module_code = "CG1001"
        test_module_sem_1 = -2
        test_module_sem_2 = -2
        has_test_module = False

        for subplan in full_mounting_plan:
            if subplan[0] == test_module_code:
                has_test_module = True
                test_module_sem_1 = subplan[2]
                test_module_sem_2 = subplan[3]
                break

        assert_true(has_test_module)
        assert_equal(test_module_sem_1, 1)
        assert_equal(test_module_sem_2, -1)


    def test_mounted_in_sem_2_only(self):
        '''
            Tests that a module that is mounted in sem 2 only
            will have the mounting values '-1' and '1'
        '''
        full_mounting_plan = self.fixed_module_mountings.full_mounting_plan
        test_module_code = "CS3247"
        test_module_sem_1 = -2
        test_module_sem_2 = -2
        has_test_module = False

        for subplan in full_mounting_plan:
            if subplan[0] == test_module_code:
                has_test_module = True
                test_module_sem_1 = subplan[2]
                test_module_sem_2 = subplan[3]
                break

        assert_true(has_test_module)
        assert_equal(test_module_sem_1, -1)
        assert_equal(test_module_sem_2, 1)

    def test_not_mounted(self):
        '''
            Tests that a module that is not mounted in any sem
            will have the mounting values '-1' and '-1'
        '''
        full_mounting_plan = self.fixed_module_mountings.full_mounting_plan
        test_module_code = "CS4344"
        test_module_sem_1 = -2
        test_module_sem_2 = -2
        has_test_module = False

        for subplan in full_mounting_plan:
            if subplan[0] == test_module_code:
                has_test_module = True
                test_module_sem_1 = subplan[2]
                test_module_sem_2 = subplan[3]
                break

        assert_true(has_test_module)
        assert_equal(test_module_sem_1, -1)
        assert_equal(test_module_sem_2, -1)
