'''
    test_individual_module_mounting_backend.py
    Contains test cases related to backened functions for displaying an individual module's mounting
'''
from nose.tools import assert_equal, assert_true
from components.handlers.module_overview import ViewMod
from components import model


class TestCode(object):
    '''
        This class runs the test cases related to displaying an individual module's mounting.
    '''
    def __init__(self):
        self.module_overview_handler = None
        self.current_ay = None
        self.next_ay = None


    def get_next_ay(self, ay):
        '''
            Return the AY that comes after the current AY
        '''
        ay = ay.split(' ')[1].split('/')
        return 'AY ' + str(int(ay[0])+1) + '/' + str(int(ay[1])+1)


    def setUp(self):
        '''
            Add dummy modules and mountings into database
        '''
        self.module_overview_handler = ViewMod()
        self.current_ay = model.get_first_fixed_mounting()[0][0:8]
        self.next_ay = self.get_next_ay(self.current_ay)

        # Dummy modules
        model.add_module('BB1001', 'Dummy Module 1',
                         'This module is mounted in both sems in both AYs.', 1, 'Active')
        model.add_module('BB1002', 'Dummy Module 2',
                         'This module is mounted in sem 1 only, in both AYs.', 2, 'Active')
        model.add_module('BB1003', 'Dummy Module 3',
                         'This module is mounted in sem 2 only, in both AYs.', 3, 'Active')
        model.add_module('BB1004', 'Dummy Module 4',
                         'This module is not mounted in any sem, in both AYs.', 4, 'Active')

        # Dummy fixed mountings
        model.add_fixed_mounting('BB1001', self.current_ay+' Sem 1', 10)
        model.add_fixed_mounting('BB1001', self.current_ay+' Sem 2', 20)
        model.add_fixed_mounting('BB1002', self.current_ay+' Sem 1', 30)
        model.add_fixed_mounting('BB1003', self.current_ay+' Sem 2', 40)

        # Dummy tentative mountings
        model.add_tenta_mounting('BB1001', self.next_ay+' Sem 1', 10)
        model.add_tenta_mounting('BB1001', self.next_ay+' Sem 2', 20)
        model.add_tenta_mounting('BB1002', self.next_ay+' Sem 1', 30)
        model.add_tenta_mounting('BB1003', self.next_ay+' Sem 2', 40)


    def tearDown(self):
        '''
            Clean up the database after all test cases are ran
        '''
        model.delete_fixed_mounting('BB1001', self.current_ay+' Sem 1')
        model.delete_fixed_mounting('BB1001', self.current_ay+' Sem 2')
        model.delete_fixed_mounting('BB1002', self.current_ay+' Sem 1')
        model.delete_fixed_mounting('BB1003', self.current_ay+' Sem 2')
        model.delete_tenta_mounting('BB1001', self.next_ay+' Sem 1')
        model.delete_tenta_mounting('BB1001', self.next_ay+' Sem 2')
        model.delete_tenta_mounting('BB1002', self.next_ay+' Sem 1')
        model.delete_tenta_mounting('BB1003', self.next_ay+' Sem 2')
        model.delete_module('BB1001')
        model.delete_module('BB1002')
        model.delete_module('BB1003')
        model.delete_module('BB1004')


    def test_mounted_in_both_sems(self):
        '''
            Tests that a module that is mounted in both sems in both AYs
            will have the mounting values '1' and '1' for both AYs
        '''
        test_module_code = "BB1001"
        self.module_overview_handler.load_fixed_mounting_plan(test_module_code)
        self.module_overview_handler.load_tenta_mounting_plan(test_module_code)
        fixed_mounting_plan = self.module_overview_handler.fixed_mounting_plan
        tenta_mounting_plan = self.module_overview_handler.tenta_mounting_plan
        assert_true(len(fixed_mounting_plan) == 2)
        assert_true(len(tenta_mounting_plan) > 0)

        fixed_sem_1_mounting_value = fixed_mounting_plan[0][1]
        fixed_sem_2_mounting_value = fixed_mounting_plan[1][1]
        fixed_sem_1_quota = fixed_mounting_plan[0][2]
        fixed_sem_2_quota = fixed_mounting_plan[1][2]
        assert_equal(fixed_sem_1_mounting_value, 1)
        assert_equal(fixed_sem_2_mounting_value, 1)
        assert_equal(fixed_sem_1_quota, 10)
        assert_equal(fixed_sem_2_quota, 20)

        tenta_sem_1_mounting_value = tenta_mounting_plan[0][1]
        tenta_sem_2_mounting_value = tenta_mounting_plan[1][1]
        tenta_sem_1_quota = tenta_mounting_plan[0][2]
        tenta_sem_2_quota = tenta_mounting_plan[1][2]
        assert_equal(tenta_sem_1_mounting_value, 1)
        assert_equal(tenta_sem_2_mounting_value, 1)
        assert_equal(tenta_sem_1_quota, 10)
        assert_equal(tenta_sem_2_quota, 20)


    def test_mounted_in_sem_1_only(self):
        '''
            Tests that a module that is mounted in sem 1 only, in both AYs,
            will have the mounting values '1' and '-1' for both AYs
        '''
        test_module_code = "BB1002"
        self.module_overview_handler.load_fixed_mounting_plan(test_module_code)
        self.module_overview_handler.load_tenta_mounting_plan(test_module_code)
        fixed_mounting_plan = self.module_overview_handler.fixed_mounting_plan
        tenta_mounting_plan = self.module_overview_handler.tenta_mounting_plan
        assert_true(len(fixed_mounting_plan) == 2)
        assert_true(len(tenta_mounting_plan) > 0)

        fixed_sem_1_mounting_value = fixed_mounting_plan[0][1]
        fixed_sem_2_mounting_value = fixed_mounting_plan[1][1]
        fixed_sem_1_quota = fixed_mounting_plan[0][2]
        fixed_sem_2_quota = fixed_mounting_plan[1][2]
        assert_equal(fixed_sem_1_mounting_value, 1)
        assert_equal(fixed_sem_2_mounting_value, -1)
        assert_equal(fixed_sem_1_quota, 30)
        assert_equal(fixed_sem_2_quota, '-')

        tenta_sem_1_mounting_value = tenta_mounting_plan[0][1]
        tenta_sem_2_mounting_value = tenta_mounting_plan[1][1]
        tenta_sem_1_quota = tenta_mounting_plan[0][2]
        tenta_sem_2_quota = tenta_mounting_plan[1][2]
        assert_equal(tenta_sem_1_mounting_value, 1)
        assert_equal(tenta_sem_2_mounting_value, -1)
        assert_equal(tenta_sem_1_quota, 30)
        assert_equal(tenta_sem_2_quota, '-')


    def test_mounted_in_sem_2_only(self):
        '''
            Tests that a module that is mounted in sem 2 only, in both AYs,
            will have the mounting values '-1' and '1' for both AYs
        '''
        test_module_code = "BB1003"
        self.module_overview_handler.load_fixed_mounting_plan(test_module_code)
        self.module_overview_handler.load_tenta_mounting_plan(test_module_code)
        fixed_mounting_plan = self.module_overview_handler.fixed_mounting_plan
        tenta_mounting_plan = self.module_overview_handler.tenta_mounting_plan
        assert_true(len(fixed_mounting_plan) == 2)
        assert_true(len(tenta_mounting_plan) > 0)

        fixed_sem_1_mounting_value = fixed_mounting_plan[0][1]
        fixed_sem_2_mounting_value = fixed_mounting_plan[1][1]
        fixed_sem_1_quota = fixed_mounting_plan[0][2]
        fixed_sem_2_quota = fixed_mounting_plan[1][2]
        assert_equal(fixed_sem_1_mounting_value, -1)
        assert_equal(fixed_sem_2_mounting_value, 1)
        assert_equal(fixed_sem_1_quota, '-')
        assert_equal(fixed_sem_2_quota, 40)

        tenta_sem_1_mounting_value = tenta_mounting_plan[0][1]
        tenta_sem_2_mounting_value = tenta_mounting_plan[1][1]
        tenta_sem_1_quota = tenta_mounting_plan[0][2]
        tenta_sem_2_quota = tenta_mounting_plan[1][2]
        assert_equal(tenta_sem_1_mounting_value, -1)
        assert_equal(tenta_sem_2_mounting_value, 1)
        assert_equal(tenta_sem_1_quota, '-')
        assert_equal(tenta_sem_2_quota, 40)


    def test_not_mounted(self):
        '''
            Tests that a module that is not mounted in any sem, in both AYs,
            will have the mounting values '-1' and '-1' for both AYs
        '''
        test_module_code = "BB1004"
        self.module_overview_handler.load_fixed_mounting_plan(test_module_code)
        self.module_overview_handler.load_tenta_mounting_plan(test_module_code)
        fixed_mounting_plan = self.module_overview_handler.fixed_mounting_plan
        tenta_mounting_plan = self.module_overview_handler.tenta_mounting_plan
        assert_true(len(fixed_mounting_plan) == 2)
        assert_true(len(tenta_mounting_plan) > 0)

        fixed_sem_1_mounting_value = fixed_mounting_plan[0][1]
        fixed_sem_2_mounting_value = fixed_mounting_plan[1][1]
        fixed_sem_1_quota = fixed_mounting_plan[0][2]
        fixed_sem_2_quota = fixed_mounting_plan[1][2]
        assert_equal(fixed_sem_1_mounting_value, -1)
        assert_equal(fixed_sem_2_mounting_value, -1)
        assert_equal(fixed_sem_1_quota, '-')
        assert_equal(fixed_sem_2_quota, '-')

        tenta_sem_1_mounting_value = tenta_mounting_plan[0][1]
        tenta_sem_2_mounting_value = tenta_mounting_plan[1][1]
        tenta_sem_1_quota = tenta_mounting_plan[0][2]
        tenta_sem_2_quota = tenta_mounting_plan[1][2]
        assert_equal(tenta_sem_1_mounting_value, -1)
        assert_equal(tenta_sem_2_mounting_value, -1)
        assert_equal(tenta_sem_1_quota, '-')
        assert_equal(tenta_sem_2_quota, '-')


    def test_unmounted_from_sem_1(self):
        '''
            Tests that a module that is unmounted from sem 1
            will have the tentative-mounting value of '0' for sem 1
        '''
        test_module_code = "BB1002"
        model.delete_tenta_mounting(test_module_code, self.next_ay+' Sem 1')

        self.module_overview_handler.load_fixed_mounting_plan(test_module_code)
        self.module_overview_handler.load_tenta_mounting_plan(test_module_code)
        tenta_mounting_plan = self.module_overview_handler.tenta_mounting_plan
        assert_true(len(tenta_mounting_plan) > 0)

        tenta_sem_1_mounting_value = tenta_mounting_plan[0][1]
        tenta_sem_1_quota = tenta_mounting_plan[0][2]
        assert_equal(tenta_sem_1_mounting_value, 0)
        assert_equal(tenta_sem_1_quota, '-')

        model.add_tenta_mounting(test_module_code, self.next_ay+' Sem 1', 30)


    def test_unmounted_from_sem_2(self):
        '''
            Tests that a module that is unmounted from sem 2
            will have the tentative-mounting value of '0' for sem 2
        '''
        test_module_code = "BB1003"
        model.delete_tenta_mounting(test_module_code, self.next_ay+' Sem 2')

        self.module_overview_handler.load_fixed_mounting_plan(test_module_code)
        self.module_overview_handler.load_tenta_mounting_plan(test_module_code)
        tenta_mounting_plan = self.module_overview_handler.tenta_mounting_plan
        assert_true(len(tenta_mounting_plan) > 0)

        tenta_sem_2_mounting_value = tenta_mounting_plan[1][1]
        tenta_sem_2_quota = tenta_mounting_plan[1][2]
        assert_equal(tenta_sem_2_mounting_value, 0)
        assert_equal(tenta_sem_2_quota, '-')

        model.add_tenta_mounting(test_module_code, self.next_ay+' Sem 2', 40)


    def test_unmounted_from_both_sems(self):
        '''
            Tests that a module that is unmounted from both sems
            will have the tentative-mounting values '0' and '0'
        '''
        test_module_code = "BB1001"
        model.delete_tenta_mounting(test_module_code, self.next_ay+' Sem 1')
        model.delete_tenta_mounting(test_module_code, self.next_ay+' Sem 2')

        self.module_overview_handler.load_fixed_mounting_plan(test_module_code)
        self.module_overview_handler.load_tenta_mounting_plan(test_module_code)
        tenta_mounting_plan = self.module_overview_handler.tenta_mounting_plan
        assert_true(len(tenta_mounting_plan) > 0)

        tenta_sem_1_mounting_value = tenta_mounting_plan[0][1]
        tenta_sem_1_quota = tenta_mounting_plan[0][2]
        tenta_sem_2_mounting_value = tenta_mounting_plan[1][1]
        tenta_sem_2_quota = tenta_mounting_plan[1][2]
        assert_equal(tenta_sem_1_mounting_value, 0)
        assert_equal(tenta_sem_1_quota, '-')
        assert_equal(tenta_sem_2_mounting_value, 0)
        assert_equal(tenta_sem_2_quota, '-')

        model.add_tenta_mounting(test_module_code, self.next_ay+' Sem 1', 10)
        model.add_tenta_mounting(test_module_code, self.next_ay+' Sem 2', 20)
