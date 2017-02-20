'''
    test_module_mounting_fixed_backend.py
    Contains test cases related to the backend functions of fixed module mountings.
'''
from nose.tools import assert_equal, assert_true
from components.handlers.fixed_module_mountings import Fixed
from components import model


class TestCode(object):
    '''
        This class runs the test cases related to fixed module mountings.
    '''
    def __init__(self):
        self.number_of_tests_left = None
        self.fixed_mounting_handler = None
        self.current_ay = None


    def setUp(self):
        '''
            Add dummy modules and mountings into database,
            Then retrieve all fixed module mountings from database
        '''
        self.fixed_mounting_handler = Fixed()
        self.current_ay = self.fixed_mounting_handler.get_current_ay()

        model.add_module('BB1001', 'Dummy Module 1',
                         'This module is mounted in both semesters.', 1, 'Active')
        model.add_module('BB1002', 'Dummy Module 2',
                         'This module is mounted in semester 1 only.', 2, 'Active')
        model.add_module('BB1003', 'Dummy Module 3',
                         'This module is mounted in semester 2 only.', 3, 'Active')
        model.add_module('BB1004', 'Dummy Module 4',
                         'This module is mounted in not mounted in any semester.', 4, 'Active')

        model.add_fixed_mounting('BB1001', self.current_ay+' Sem 1', 10)
        model.add_fixed_mounting('BB1001', self.current_ay+' Sem 2', 20)
        model.add_fixed_mounting('BB1002', self.current_ay+' Sem 1', 30)
        model.add_fixed_mounting('BB1003', self.current_ay+' Sem 2', 40)

        self.fixed_mounting_handler.populate_module_code_and_name()
        self.fixed_mounting_handler.populate_mounting_values()

        assert_true(len(self.fixed_mounting_handler.full_mounting_plan) > 0)


    def tearDown(self):
        '''
            Clean up the database after all test cases are ran
        '''
        model.delete_fixed_mounting('BB1001', self.current_ay+' Sem 1')
        model.delete_fixed_mounting('BB1001', self.current_ay+' Sem 2')
        model.delete_fixed_mounting('BB1002', self.current_ay+' Sem 1')
        model.delete_fixed_mounting('BB1003', self.current_ay+' Sem 2')
        model.delete_module('BB1001')
        model.delete_module('BB1002')
        model.delete_module('BB1003')
        model.delete_module('BB1004')


    def test_mounted_in_both_sems(self):
        '''
            Tests that a module that is mounted in both sems
            will have the mounting values '1' and '1'
        '''
        full_mounting_plan = self.fixed_mounting_handler.full_mounting_plan
        test_module_code = "BB1001"
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
        full_mounting_plan = self.fixed_mounting_handler.full_mounting_plan
        test_module_code = "BB1002"
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
        full_mounting_plan = self.fixed_mounting_handler.full_mounting_plan
        test_module_code = "BB1003"
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
        full_mounting_plan = self.fixed_mounting_handler.full_mounting_plan
        test_module_code = "BB1004"
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


    def test_all_fixed_mountings_in_same_ay(self):
        '''
            Tests that all the fixed module mountings
            are in the same AY (current AY)
        '''
        mounted_module_infos = model.get_all_fixed_mounted_modules()
        current_ay = self.current_ay
        is_same_ay = True
        for info in mounted_module_infos:
            ay = info[2][0:8]
            if ay != current_ay:
                is_same_ay = False
                break
        assert_true(is_same_ay)
