'''
    test_module_mounting_tentative_backend.py
    Contains test cases related to the backend functions of tentative module mountings.
'''
from nose.tools import assert_equal, assert_true, assert_false
from components.handlers.fixed_module_mountings import Fixed
from components.handlers.tentative_module_mountings import Tentative
from components import model


class TestCode(object):
    '''
        This class runs the test cases related to tentative module mountings.
    '''
    def __init__(self):
        self.number_of_tests_left = None
        self.fixed_mounting_handler = None
        self.tentative_mounting_handler = None
        self.current_ay = None
        self.next_ay = None
        self.selected_tentative_mountings = None


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
        self.fixed_mounting_handler = Fixed()
        self.current_ay = self.fixed_mounting_handler.get_current_ay()

        self.tentative_mounting_handler = Tentative()
        self.next_ay = self.get_next_ay(self.current_ay)
        self.selected_tentative_mountings = model.get_all_tenta_mounted_modules_of_selected_ay(self.next_ay)

        # Dummy modules
        model.add_module('BB1001', 'Dummy Module 1', 
                         'This module is mounted in both sems in both AYs.', 1, 'Active')
        model.add_module('BB1002', 'Dummy Module 2', 
                         'This module is mounted in sem 1 only, in both AYs.', 2, 'Active')
        model.add_module('BB1003', 'Dummy Module 3', 
                         'This module is mounted in sem 2 only, in both AYs.', 3, 'Active')
        model.add_module('BB1004', 'Dummy Module 4', 
                         'This module is not mounted in any sem, in both AYs.', 4, 'Active')
        model.add_module('BB9999', 'Dummy Module X', 
                         'This module is mounted 20 years in the future!', 0, 'Active')

        # Dummy fixed mountings
        model.add_fixed_mounting('BB1001', self.current_ay+' Sem 1', 10)
        model.add_fixed_mounting('BB1001', self.current_ay+' Sem 2', 20)
        model.add_fixed_mounting('BB1002', self.current_ay+' Sem 1', 30)
        model.add_fixed_mounting('BB1003', self.current_ay+' Sem 2', 40)

        self.load_fixed_full_mounting_plan()

        # Dummy tentative mountings
        model.add_tenta_mounting('BB1001', self.next_ay+' Sem 1', 10)    
        model.add_tenta_mounting('BB1001', self.next_ay+' Sem 2', 20) 
        model.add_tenta_mounting('BB1002', self.next_ay+' Sem 1', 30) 
        model.add_tenta_mounting('BB1003', self.next_ay+' Sem 2', 40)
        model.add_tenta_mounting('BB9999', 'AY 36/37 Sem 1', 999)  

        self.load_tenta_full_mounting_plan()


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
        model.delete_tenta_mounting('BB9999', 'AY 36/37 Sem 1')
        model.delete_module('BB1001')
        model.delete_module('BB1002')
        model.delete_module('BB1003')
        model.delete_module('BB1004')


    def load_fixed_full_mounting_plan(self):
        '''
            Retrieve fixed mounting data from database and generate full mounting plan
        '''
        self.fixed_mounting_handler.populate_module_code_and_name()
        self.fixed_mounting_handler.populate_mounting_values()
        assert_true(len(self.fixed_mounting_handler.full_mounting_plan) > 0)


    def load_tenta_full_mounting_plan(self):
        '''
            Retrieve tentative mounting data from database and generate full mounting plan
        '''
        self.tentative_mounting_handler.populate_module_code_and_name()
        self.tentative_mounting_handler.populate_mounting_values(self.next_ay)
        assert_true(len(self.tentative_mounting_handler.full_mounting_plan) > 0) 


    def test_tenta_mountings_of_selected_ay(self):
        '''
            Test that a list of tentative mountings of selected AY
            only contains mountings from the same AY
        '''
        selected_ay = self.next_ay
        mounted_module_infos = self.selected_tentative_mountings
        is_same_ay = True
        for info in mounted_module_infos:
            ay = info[2][0:8]
            if ay != selected_ay:
                is_same_ay = False
                break
        assert_true(is_same_ay)


    def test_tenta_mounting_appear_in_correct_ay(self):
        '''
            Test that a tentative mounting will only appear in
            the tentative mounting list of its AY
        '''
        test_module_code = "BB9999"
        mounted_module_infos = self.selected_tentative_mountings

        # BB9999 should NOT appear in tentative list for next AY
        is_in_list = False
        for info in mounted_module_infos:
            if info[0] == test_module_code:
                is_in_list = True
                break
        assert_false(is_in_list)

        # BB9999 should appear in tentative list for AY 36/37
        mounted_module_infos = model.get_all_tenta_mounted_modules_of_selected_ay("AY 36/37")
        is_in_list = False
        for info in mounted_module_infos:
            if info[0] == test_module_code:
                is_in_list = True
                break
        assert_true(is_in_list)


    def test_mounted_in_both_sems(self):
        '''
            Tests that a module that is mounted in both sems in both AYs
            will have the tentative-mounting values '1' and '1'
        '''
        full_mounting_plan = self.tentative_mounting_handler.full_mounting_plan
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
            Tests that a module that is mounted in sem 1 only, in both AYs,
            will have the tentative-mounting values '1' and '-1'
        '''
        full_mounting_plan = self.tentative_mounting_handler.full_mounting_plan
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
            Tests that a module that is mounted in sem 2 only, in both AYs,
            will have the tentative-mounting values '-1' and '1'
        '''
        full_mounting_plan = self.tentative_mounting_handler.full_mounting_plan
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
            Tests that a module that is not mounted in any sem, in both AYs,
            will have the tentative-mounting values '-1' and '-1'
        '''
        full_mounting_plan = self.tentative_mounting_handler.full_mounting_plan
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


    def test_unmounted_from_sem_1(self):
        '''
            Tests that a module that is unmounted from sem 1
            will have the tentative-mounting value of '0' for sem 1
        '''
        model.delete_tenta_mounting('BB1001', self.next_ay+' Sem 1')
        model.delete_tenta_mounting('BB1002', self.next_ay+' Sem 1')
        self.load_tenta_full_mounting_plan()
        full_mounting_plan = self.tentative_mounting_handler.full_mounting_plan

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
        assert_equal(test_module_sem_1, 0)
        assert_equal(test_module_sem_2, 1)

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
        assert_equal(test_module_sem_1, 0)
        assert_equal(test_module_sem_2, -1)

        model.add_tenta_mounting('BB1001', self.next_ay+' Sem 1', 10)    
        model.add_tenta_mounting('BB1002', self.next_ay+' Sem 1', 30) 
        self.load_tenta_full_mounting_plan()


    def test_unmounted_from_sem_2(self):
        '''
            Tests that a module that is unmounted from sem 2
            will have the tentative-mounting value of '0' for sem 2
        '''
        model.delete_tenta_mounting('BB1001', self.next_ay+' Sem 2')
        model.delete_tenta_mounting('BB1003', self.next_ay+' Sem 2')
        self.load_tenta_full_mounting_plan()
        full_mounting_plan = self.tentative_mounting_handler.full_mounting_plan

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
        assert_equal(test_module_sem_2, 0)

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
        assert_equal(test_module_sem_2, 0)

        model.add_tenta_mounting('BB1001', self.next_ay+' Sem 2', 20)    
        model.add_tenta_mounting('BB1003', self.next_ay+' Sem 2', 40) 
        self.load_tenta_full_mounting_plan()


    def test_unmounted_from_both_sems(self):
        '''
            Tests that a module that is unmounted from both sems
            will have the tentative-mounting values '0' and '0'
        '''
        model.delete_tenta_mounting('BB1001', self.next_ay+' Sem 1')
        model.delete_tenta_mounting('BB1001', self.next_ay+' Sem 2')
        self.load_tenta_full_mounting_plan()
        full_mounting_plan = self.tentative_mounting_handler.full_mounting_plan

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
        assert_equal(test_module_sem_1, 0)
        assert_equal(test_module_sem_2, 0)

        model.add_tenta_mounting('BB1001', self.next_ay+' Sem 1', 10)    
        model.add_tenta_mounting('BB1001', self.next_ay+' Sem 2', 20) 
        self.load_tenta_full_mounting_plan()