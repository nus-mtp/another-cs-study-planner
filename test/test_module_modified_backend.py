'''
    test_modified_modules_backend.py
    Contains test cases related to the backend functions of modified modules.
'''
from nose.tools import assert_equal, assert_true, assert_false
from components import model
from components.handlers.modified_modules import Modified


class TestCode(object):
    '''
        This class runs the test cases related to modified modules.
    '''
    def __init__(self):
        self.current_ay = model.get_current_ay()
        self.next_ay = self.get_next_ay(self.current_ay)
        self.next_next_ay = self.get_next_ay(self.next_ay)
        self.modified_modules_handler = Modified()


    def get_next_ay(self, ay):
        '''
            Return the AY that comes after the given AY
        '''
        ay = ay.split(' ')[1].split('/')
        return 'AY ' + str(int(ay[0])+1) + '/' + str(int(ay[1])+1)


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

        model.add_module('BB2001', 'Dummy Module 1',
                         "This module is unmounted from sem 1", 1, 'Active')
        model.add_module('BB2002', 'Dummy Module 2',
                         "This module is remounted in sem 2", 2, 'Active')
        model.add_module('BB2003', 'Dummy Module 3',
                         "This module is changed from mounted in sem 1 to sem 2", 3, 'Active')

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

        model.add_fixed_mounting('BB2001', self.current_ay+' Sem 1', 10)
        model.add_fixed_mounting('BB2001', self.current_ay+' Sem 2', 10)
        model.add_fixed_mounting('BB2002', self.current_ay+' Sem 1', 20)
        model.add_fixed_mounting('BB2003', self.current_ay+' Sem 1', 30)

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

        model.add_tenta_mounting('BB2001', self.next_ay+' Sem 2', 10)
        model.add_tenta_mounting('BB2002', self.next_ay+' Sem 1', 20)
        model.add_tenta_mounting('BB2002', self.next_ay+' Sem 2', 20)
        model.add_tenta_mounting('BB2003', self.next_ay+' Sem 2', 30)


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
        model.delete_fixed_mounting('BB2001', self.current_ay+' Sem 1')
        model.delete_fixed_mounting('BB2001', self.current_ay+' Sem 2')
        model.delete_fixed_mounting('BB2002', self.current_ay+' Sem 1')
        model.delete_fixed_mounting('BB2003', self.current_ay+' Sem 1')

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
        model.delete_tenta_mounting('BB2001', self.next_ay+' Sem 2')
        model.delete_tenta_mounting('BB2002', self.next_ay+' Sem 1')
        model.delete_tenta_mounting('BB2002', self.next_ay+' Sem 2')
        model.delete_tenta_mounting('BB2003', self.next_ay+' Sem 2')

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

        modified_modules = self.modified_modules_handler.get_modules_with_modified_quota()
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

        modified_modules = self.modified_modules_handler.get_modules_with_modified_quota()
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
                target_aysem = module[2]
                current_quota = module[3]
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

        modified_modules = self.modified_modules_handler.get_modules_with_modified_quota()
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
                target_aysem = module[2]
                current_quota = module[3]
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

        modified_modules = self.modified_modules_handler.get_modules_with_modified_quota()
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
                target_aysem = module[2]
                current_quota = module[3]
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

        modified_modules = self.modified_modules_handler.get_modules_with_modified_quota()
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
                target_aysem = module[2]
                current_quota = module[3]
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

        modified_modules = self.modified_modules_handler.get_modules_with_modified_quota()
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
                target_aysem = module[2]
                current_quota = module[3]
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
                target_aysem = module[2]
                current_quota = module[3]
                modified_quota = module[4]
                break

        assert_true(is_in_modified_modules)
        assert_equal(test_current_aysem, current_aysem)
        assert_equal(test_current_quota, current_quota)
        assert_equal(test_target_aysem, target_aysem)
        assert_equal(test_modified_quota, modified_quota)


    def test_mounting_not_modified(self):
        '''
            Test that a module whose mounting is NOT modified
            will not appear in the list of modified modules
        '''
        test_module_code = 'BB1001'

        modified_modules = self.modified_modules_handler.get_modules_with_modified_mounting()
        is_in_modified_modules = False

        for module in modified_modules:
            code = module[0]
            if code == test_module_code:
                is_in_modified_modules = True
                break

        assert_false(is_in_modified_modules)


    def test_unmounted_module(self):
        '''
            Test that a module whose is unmounted
            will appear in the list of modified modules
        '''
        test_module_code = 'BB2001'
        test_current_aysem = self.current_ay+" Sem 1"
        test_target_aysem = self.next_ay+" Sem 1"
        test_mounting_change = "Unmounted"

        modified_modules = self.modified_modules_handler.get_modules_with_modified_mounting()
        is_in_modified_modules = False
        current_aysem = None
        target_aysem = None
        mounting_change = None

        for module in modified_modules:
            code = module[0]
            if code == test_module_code:
                is_in_modified_modules = True
                current_aysem = module[1]
                target_aysem = module[2]
                mounting_change = module[3]
                break

        assert_true(is_in_modified_modules)
        assert_equal(test_current_aysem, current_aysem)
        assert_equal(test_target_aysem, target_aysem)
        assert_equal(test_mounting_change, mounting_change)


    def test_remounted_module(self):
        '''
            Test that a module whose is remounted
            will appear in the list of modified modules
        '''
        test_module_code = 'BB2002'
        test_current_aysem = self.current_ay+" Sem 2"
        test_target_aysem = self.next_ay+" Sem 2"
        test_mounting_change = "Mounted"

        modified_modules = self.modified_modules_handler.get_modules_with_modified_mounting()
        is_in_modified_modules = False
        current_aysem = None
        target_aysem = None
        mounting_change = None

        for module in modified_modules:
            code = module[0]
            if code == test_module_code:
                is_in_modified_modules = True
                current_aysem = module[1]
                target_aysem = module[2]
                mounting_change = module[3]
                break

        assert_true(is_in_modified_modules)
        assert_equal(test_current_aysem, current_aysem)
        assert_equal(test_target_aysem, target_aysem)
        assert_equal(test_mounting_change, mounting_change)


    def test_multiple_mounting_changes(self):
        '''
            Test that a module whose mounting is modified for multiple AY-Sems
            will appear as multiple entries in the modified module table
        '''
        test_module_code = 'BB2003'
        test_current_aysem = self.current_ay+" Sem 1"
        test_target_aysem = self.next_ay+" Sem 1"
        test_mounting_change = "Unmounted"

        modified_modules = self.modified_modules_handler.get_modules_with_modified_mounting()
        is_in_modified_modules = False
        current_aysem = None
        target_aysem = None
        mounting_change = None

        current_index = 0
        for module in modified_modules:
            code = module[0]
            if code == test_module_code:
                is_in_modified_modules = True
                current_aysem = module[1]
                target_aysem = module[2]
                mounting_change = module[3]
                break
            current_index += 1

        assert_true(is_in_modified_modules)
        assert_equal(test_current_aysem, current_aysem)
        assert_equal(test_target_aysem, target_aysem)
        assert_equal(test_mounting_change, mounting_change)

        test_current_aysem = self.current_ay+" Sem 2"
        test_target_aysem = self.next_ay+" Sem 2"
        test_mounting_change = "Mounted"

        is_in_modified_modules = False
        for module in modified_modules[current_index+1:]:
            code = module[0]
            if code == test_module_code:
                is_in_modified_modules = True
                current_aysem = module[1]
                target_aysem = module[2]
                mounting_change = module[3]
                break
            current_index += 1

        assert_true(is_in_modified_modules)
        assert_equal(test_current_aysem, current_aysem)
        assert_equal(test_target_aysem, target_aysem)
        assert_equal(test_mounting_change, mounting_change)


    def test_mounting_modified_in_multiple_ays(self):
        '''
            Test that the modified module table can display modules
            whose mounting is modified for multiple future AYs
        '''
        test_module_code = 'BB1001'   # not mounted in next next AY
        test_current_aysem = self.current_ay+" Sem 1"
        test_target_aysem = self.next_next_ay+" Sem 1"
        test_mounting_change = "Unmounted"

        # Set modified module to check for modifications in next two AYs
        self.modified_modules_handler.number_of_future_ays = 2

        modified_modules = self.modified_modules_handler.get_modules_with_modified_mounting()
        is_in_modified_modules = False
        current_aysem = None
        target_aysem = None
        mounting_change = None

        for module in modified_modules:
            code = module[0]
            if code == test_module_code:
                is_in_modified_modules = True
                current_aysem = module[1]
                target_aysem = module[2]
                mounting_change = module[3]
                break

        self.modified_modules_handler.number_of_future_ays = 1

        assert_true(is_in_modified_modules)
        assert_equal(test_current_aysem, current_aysem)
        assert_equal(test_target_aysem, target_aysem)
        assert_equal(test_mounting_change, mounting_change)

