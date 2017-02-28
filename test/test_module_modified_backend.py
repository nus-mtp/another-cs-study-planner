'''
    test_modified_modules_backend.py
    Contains test cases related to the backend functions of modified modules.
'''
from nose.tools import assert_equal, assert_true, assert_false
from components import model


class TestCode(object):
    '''
        This class runs the test cases related to modified modules.
    '''
    def __init__(self):
        self.current_ay = "AY 16/17"
        self.next_ay = "AY 17/18"


    def setUp(self):
        '''
            Add dummy modules and mountings into database
        '''
        # Dummy modules
        model.add_module('BB1001', 'Dummy Module 1',
                         "This module's quota is NOT modified", 1, 'Active')
        model.add_module('BB1002', 'Dummy Module 2',
                         "This module's quota for sem 1 is modified", 2, 'Active')
        model.add_module('BB1003', 'Dummy Module 3',
                         "This module's quota for sem 2 is modified", 3, 'Active')
        model.add_module('BB1004', 'Dummy Module 4',
                         "This module's quota for sem 1 has become specified", 4, 'Active')
        model.add_module('BB1005', 'Dummy Module 5',
                         "This module's quota for sem 2 has become unspecified", 5, 'Active')
        model.add_module('BB1006', 'Dummy Module 6',
                         "This module's quota for both sem 1 & 2 have been modified", 6, 'Active')

        # Dummy fixed mountings
        model.add_fixed_mounting('BB1001', self.current_ay+' Sem 1', 10)
        model.add_fixed_mounting('BB1001', self.current_ay+' Sem 2', 10)
        model.add_fixed_mounting('BB1002', self.current_ay+' Sem 1', 20)
        model.add_fixed_mounting('BB1002', self.current_ay+' Sem 2', 20)
        model.add_fixed_mounting('BB1003', self.current_ay+' Sem 1', 30)
        model.add_fixed_mounting('BB1003', self.current_ay+' Sem 2', 30)
        model.add_fixed_mounting('BB1004', self.current_ay+' Sem 1', None)
        model.add_fixed_mounting('BB1004', self.current_ay+' Sem 2', None)
        model.add_fixed_mounting('BB1005', self.current_ay+' Sem 1', 50)
        model.add_fixed_mounting('BB1005', self.current_ay+' Sem 2', 50)
        model.add_fixed_mounting('BB1006', self.current_ay+' Sem 1', 60)
        model.add_fixed_mounting('BB1006', self.current_ay+' Sem 2', 60)

        # Dummy tentative mountings
        model.add_tenta_mounting('BB1001', self.next_ay+' Sem 1', 10)
        model.add_tenta_mounting('BB1001', self.next_ay+' Sem 2', 10)
        model.add_tenta_mounting('BB1002', self.next_ay+' Sem 1', 999)
        model.add_tenta_mounting('BB1002', self.next_ay+' Sem 2', 20)
        model.add_tenta_mounting('BB1003', self.next_ay+' Sem 1', 30)
        model.add_tenta_mounting('BB1003', self.next_ay+' Sem 2', 999)
        model.add_tenta_mounting('BB1004', self.next_ay+' Sem 1', 999)
        model.add_tenta_mounting('BB1004', self.next_ay+' Sem 2', None)
        model.add_tenta_mounting('BB1005', self.next_ay+' Sem 1', 50)
        model.add_tenta_mounting('BB1005', self.next_ay+' Sem 2', None)
        model.add_tenta_mounting('BB1006', self.next_ay+' Sem 1', 999)
        model.add_tenta_mounting('BB1006', self.next_ay+' Sem 2', None)


    def tearDown(self):
        '''
            Clean up the database after all test cases are ran
        '''
        model.delete_fixed_mounting('BB1001', self.current_ay+' Sem 1')
        model.delete_fixed_mounting('BB1001', self.current_ay+' Sem 2')
        model.delete_fixed_mounting('BB1002', self.current_ay+' Sem 1')
        model.delete_fixed_mounting('BB1002', self.current_ay+' Sem 2')
        model.delete_fixed_mounting('BB1003', self.current_ay+' Sem 1')
        model.delete_fixed_mounting('BB1003', self.current_ay+' Sem 2')
        model.delete_fixed_mounting('BB1004', self.current_ay+' Sem 1')
        model.delete_fixed_mounting('BB1004', self.current_ay+' Sem 2')
        model.delete_fixed_mounting('BB1005', self.current_ay+' Sem 1')
        model.delete_fixed_mounting('BB1005', self.current_ay+' Sem 2')
        model.delete_fixed_mounting('BB1006', self.current_ay+' Sem 1')
        model.delete_fixed_mounting('BB1006', self.current_ay+' Sem 2')
        model.delete_tenta_mounting('BB1001', self.next_ay+' Sem 1')
        model.delete_tenta_mounting('BB1001', self.next_ay+' Sem 2')
        model.delete_tenta_mounting('BB1002', self.next_ay+' Sem 1')
        model.delete_tenta_mounting('BB1002', self.next_ay+' Sem 2')
        model.delete_tenta_mounting('BB1003', self.next_ay+' Sem 1')
        model.delete_tenta_mounting('BB1003', self.next_ay+' Sem 2')
        model.delete_tenta_mounting('BB1004', self.next_ay+' Sem 1')
        model.delete_tenta_mounting('BB1004', self.next_ay+' Sem 2')
        model.delete_tenta_mounting('BB1005', self.next_ay+' Sem 1')
        model.delete_tenta_mounting('BB1005', self.next_ay+' Sem 2')
        model.delete_tenta_mounting('BB1006', self.next_ay+' Sem 1')
        model.delete_tenta_mounting('BB1006', self.next_ay+' Sem 2')
        model.delete_module('BB1001')
        model.delete_module('BB1002')
        model.delete_module('BB1003')
        model.delete_module('BB1004')
        model.delete_module('BB1005')
        model.delete_module('BB1006')


    def test_quota_not_modified(self):
        '''
            Test that a module whose quota is NOT modified
            will not appear in the list of modified modules
        '''
        test_module_code = 'BB1001'

        modified_modules = model.get_modules_with_modified_quota()
        is_in_modified_modules = False

        for module in modified_modules:
            code = module[0]
            if code == test_module_code:
                is_in_modified_modules = True
                break

        assert_false(is_in_modified_modules)


    def test_quota_modified_sem_1(self):
        '''
            Test that a module whose quota for sem 1 is modified
            will appear in the list of modified modules
        '''
        test_module_code = 'BB1002'
        test_current_aysem = self.current_ay+" Sem 1"
        test_current_quota = 20
        test_target_aysem = self.next_ay+" Sem 1"
        test_modified_quota = 999

        modified_modules = model.get_modules_with_modified_quota()
        is_in_modified_modules = False
        current_aysem = None
        current_quota = -1
        target_aysem = None
        modified_quota = -1

        for module in modified_modules:
            code = module[0]
            if code == test_module_code:
                is_in_modified_modules = True
                current_aysem = module[1]
                current_quota = module[2]
                target_aysem = module[3]
                modified_quota = module[4]
                break

        assert_true(is_in_modified_modules)
        assert_equal(test_current_aysem, current_aysem)
        assert_equal(test_current_quota, current_quota)
        assert_equal(test_target_aysem, target_aysem)
        assert_equal(test_modified_quota, modified_quota)


    def test_quota_modified_sem_2(self):
        '''
            Test that a module whose quota for sem 2 is modified
            will appear in the list of modified modules
        '''
        test_module_code = 'BB1003'
        test_current_aysem = self.current_ay+" Sem 2"
        test_current_quota = 30
        test_target_aysem = self.next_ay+" Sem 2"
        test_modified_quota = 999

        modified_modules = model.get_modules_with_modified_quota()
        is_in_modified_modules = False
        current_aysem = None
        current_quota = -1
        target_aysem = None
        modified_quota = -1

        for module in modified_modules:
            code = module[0]
            if code == test_module_code:
                is_in_modified_modules = True
                current_aysem = module[1]
                current_quota = module[2]
                target_aysem = module[3]
                modified_quota = module[4]
                break

        assert_true(is_in_modified_modules)
        assert_equal(test_current_aysem, current_aysem)
        assert_equal(test_current_quota, current_quota)
        assert_equal(test_target_aysem, target_aysem)
        assert_equal(test_modified_quota, modified_quota)


    def test_quota_specified(self):
        '''
            Test that a module whose quota for a sem became specified
            will appear in the list of modified modules
        '''
        test_module_code = 'BB1004'
        test_current_aysem = self.current_ay+" Sem 1"
        test_current_quota = None
        test_target_aysem = self.next_ay+" Sem 1"
        test_modified_quota = 999

        modified_modules = model.get_modules_with_modified_quota()
        is_in_modified_modules = False
        current_aysem = None
        current_quota = -1
        target_aysem = None
        modified_quota = -1

        for module in modified_modules:
            code = module[0]
            if code == test_module_code:
                is_in_modified_modules = True
                current_aysem = module[1]
                current_quota = module[2]
                target_aysem = module[3]
                modified_quota = module[4]
                break

        assert_true(is_in_modified_modules)
        assert_equal(test_current_aysem, current_aysem)
        assert_equal(test_current_quota, current_quota)
        assert_equal(test_target_aysem, target_aysem)
        assert_equal(test_modified_quota, modified_quota)


    def test_quota_unspecified(self):
        '''
            Test that a module whose quota for a sem became UNspecified
            will appear in the list of modified modules
        '''
        test_module_code = 'BB1005'
        test_current_aysem = self.current_ay+" Sem 2"
        test_current_quota = 50
        test_target_aysem = self.next_ay+" Sem 2"
        test_modified_quota = None

        modified_modules = model.get_modules_with_modified_quota()
        is_in_modified_modules = False
        current_aysem = None
        current_quota = -1
        target_aysem = None
        modified_quota = -1

        for module in modified_modules:
            code = module[0]
            if code == test_module_code:
                is_in_modified_modules = True
                current_aysem = module[1]
                current_quota = module[2]
                target_aysem = module[3]
                modified_quota = module[4]
                break

        assert_true(is_in_modified_modules)
        assert_equal(test_current_aysem, current_aysem)
        assert_equal(test_current_quota, current_quota)
        assert_equal(test_target_aysem, target_aysem)
        assert_equal(test_modified_quota, modified_quota)


    def test_quota_modified_both_sems(self):
        '''
            Test that a module whose quota for both sems have been modified
            will appear in the list of modified modules as two entries
        '''
        # Test if entry for sem 1 exists
        test_module_code = 'BB1006'
        test_current_aysem = self.current_ay+" Sem 1"
        test_current_quota = 60
        test_target_aysem = self.next_ay+" Sem 1"
        test_modified_quota = 999

        modified_modules = model.get_modules_with_modified_quota()
        is_in_modified_modules = False
        current_aysem = None
        current_quota = -1
        target_aysem = None
        modified_quota = -1

        current_index = 0
        for module in modified_modules:
            code = module[0]
            if code == test_module_code:
                is_in_modified_modules = True
                current_aysem = module[1]
                current_quota = module[2]
                target_aysem = module[3]
                modified_quota = module[4]
                break
            current_index += 1

        assert_true(is_in_modified_modules)
        assert_equal(test_current_aysem, current_aysem)
        assert_equal(test_current_quota, current_quota)
        assert_equal(test_target_aysem, target_aysem)
        assert_equal(test_modified_quota, modified_quota)

        # Test if entry for sem 2 exists
        test_current_aysem = self.current_ay+" Sem 2"
        test_current_quota = 60
        test_target_aysem = self.next_ay+" Sem 2"
        test_modified_quota = None

        is_in_modified_modules = False
        for module in modified_modules[current_index+1:]:
            code = module[0]
            if code == test_module_code:
                is_in_modified_modules = True
                current_aysem = module[1]
                current_quota = module[2]
                target_aysem = module[3]
                modified_quota = module[4]
                break

        assert_true(is_in_modified_modules)
        assert_equal(test_current_aysem, current_aysem)
        assert_equal(test_current_quota, current_quota)
        assert_equal(test_target_aysem, target_aysem)
        assert_equal(test_modified_quota, modified_quota)
