'''
    test_modified_modules_backend.py
    Contains test cases related to the backend functions of modified modules.
'''
from nose.tools import assert_equal, assert_not_equal, assert_true, assert_false
from components import model
from components.handlers.modified_modules import Modified
from components.handlers.module_edit import EditModuleInfo
from components.handlers.module_restore import RestoreModule


class TestCode(object):
    '''
        This class runs the test cases related to modified modules.
    '''
    def __init__(self):
        self.current_ay = model.get_current_ay()
        self.next_ay = self.get_next_ay(self.current_ay)
        self.next_next_ay = self.get_next_ay(self.next_ay)
        self.modified_modules_handler = Modified()
        self.module_edit_handler = EditModuleInfo()
        self.module_restore_handler = RestoreModule()


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
                         "This module's quota for both sem 1 & 2 have been modified",
                         6, 'Active')

        model.add_module('BB2001', 'Dummy Module 1',
                         "This module is unmounted from sem 1", 1, 'Active')
        model.add_module('BB2002', 'Dummy Module 2',
                         "This module is remounted in sem 2", 2, 'Active')
        model.add_module('BB2003', 'Dummy Module 3',
                         "This module is changed from mounted in sem 1 to sem 2", 3, 'Active')
        model.add_module('BB2004', 'Dummy Module 4',
                         "This module's mounting is modified but quota is not modified",
                         4, 'Active')

        model.add_module('BB3001', 'Dummy Module 1',
                         "This module's quota is modified and will be restored", 1, 'Active')
        model.add_module('BB3002', 'Dummy Module 2',
                         "This module's quota has been specified and will be restored" +\
                         "to unspecified", 2, 'Active')
        model.add_module('BB3003', 'Dummy Module 3',
                         "This module's has been mounted and will be restored to unmounted",
                         3, 'Active')
        model.add_module('BB3004', 'Dummy Module 4',
                         "This module's has been unmounted and will be restored to mounted",
                         4, 'Active')
        model.add_module('BB3005', 'Dummy Module 5',
                         "This module's name will be restored", 5, 'Active')
        model.add_module('BB3006', 'Dummy Module 6',
                         "This module's name, description and MC will be restored", 6,
                         'Active')

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
        model.add_fixed_mounting('BB2004', self.current_ay+' Sem 1', None)

        model.add_fixed_mounting('BB3001', self.current_ay+' Sem 1', 10)
        model.add_fixed_mounting('BB3002', self.current_ay+' Sem 1', None)
        model.add_fixed_mounting('BB3004', self.current_ay+' Sem 2', 40)

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
        model.add_tenta_mounting('BB2004', self.next_ay+' Sem 1', None)
        model.add_tenta_mounting('BB2004', self.next_ay+' Sem 2', None)

        model.add_tenta_mounting('BB3001', self.next_ay+' Sem 1', 999)
        model.add_tenta_mounting('BB3002', self.next_ay+' Sem 1', 999)
        model.add_tenta_mounting('BB3003', self.next_ay+' Sem 2', 999)

        # Dummy module backup
        model.store_original_module_info('BB3005', 'Original Module Name',
                                         "This module's name will be restored", 5)
        model.store_original_module_info('BB3006', 'Original Module Name',
                                         "Original Module Description", 0)


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
        model.delete_fixed_mounting('BB2004', self.current_ay+' Sem 1')
        model.delete_fixed_mounting('BB3001', self.current_ay+' Sem 1')
        model.delete_fixed_mounting('BB3002', self.current_ay+' Sem 1')
        model.delete_fixed_mounting('BB3004', self.current_ay+' Sem 2')

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
        model.delete_tenta_mounting('BB2004', self.next_ay+' Sem 1')
        model.delete_tenta_mounting('BB2004', self.next_ay+' Sem 2')
        model.delete_tenta_mounting('BB3001', self.next_ay+' Sem 1')
        model.delete_tenta_mounting('BB3002', self.next_ay+' Sem 1')
        model.delete_tenta_mounting('BB3003', self.next_ay+' Sem 2')
        model.delete_tenta_mounting('BB3004', self.next_ay+' Sem 2')

        model.delete_module('BB1001')
        model.delete_module('BB1002')
        model.delete_module('BB1003')
        model.delete_module('BB1004')
        model.delete_module('BB1005')
        model.delete_module('BB1006')
        model.delete_module('BB2001')
        model.delete_module('BB2002')
        model.delete_module('BB2003')
        model.delete_module('BB2004')
        model.delete_module('BB3001')
        model.delete_module('BB3002')
        model.delete_module('BB3003')
        model.delete_module('BB3004')
        model.delete_module('BB3005')
        model.delete_module('BB3006')


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
        test_mounting_change = 0

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
        test_mounting_change = 1

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
        test_mounting_change = 0

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
        test_mounting_change = 1

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
        test_mounting_change = 0

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


    class TestEditModuleData(object):
        '''
            Emulate the data submitted by the web form of the 'Edit Module' page
        '''
        def __init__(self, status, code, name, desc, mc):
            self.status = status
            self.code = code
            self.name = name
            self.desc = desc
            self.mc = mc


    def test_module_edit_but_same_info(self):
        '''
            Test that for Edit Module, if module info is exactly the same as before the edit,
            a backup of the module's original info will NOT be inserted into database
        '''
        test_module_code = 'BB1001'
        test_module_name = "Dummy Module 1"
        test_module_desc = "This module's quota is NOT modified"
        test_module_mc = 1

        test_post_data = self.TestEditModuleData("submit", test_module_code,
                                                 test_module_name, test_module_desc,
                                                 test_module_mc)
        self.module_edit_handler.POST(test_post_data)

        modified_modules = self.modified_modules_handler.get_modules_with_modified_details()
        is_in_modified_modules = False
        for module in modified_modules:
            code = module[0]
            if code == test_module_code:
                is_in_modified_modules = True

        assert_false(is_in_modified_modules)


    def test_module_edit_backup(self):
        '''
            Test that for Edit Module, if module info has been modified after the edit,
            a backup of the module's original info will be inserted into database
        '''
        number_of_modified_modules = len(model.get_modules_with_modified_details())

        # Name has been modified
        test_module_code = 'BB1001'
        test_module_name = "Dummy Module NAME MODIFIED"
        test_module_desc = "This module's quota is NOT modified"
        test_module_mc = 1

        test_post_data = self.TestEditModuleData("submit", test_module_code,
                                                 test_module_name, test_module_desc,
                                                 test_module_mc)
        self.module_edit_handler.POST(test_post_data)

        modified_modules = self.modified_modules_handler.get_modules_with_modified_details()
        assert_not_equal(number_of_modified_modules, len(modified_modules))
        number_of_modified_modules = len(modified_modules)

        is_in_modified_modules = False
        is_name_modified = None
        is_desc_modified = None
        is_mc_modified = None
        for module in modified_modules:
            code = module[0]
            if code == test_module_code:
                is_in_modified_modules = True
                is_name_modified = module[1][0] is not None
                is_desc_modified = module[1][1] is not None
                is_mc_modified = module[1][2] is not None
        assert_true(is_in_modified_modules)
        assert_true(is_name_modified)
        assert_false(is_desc_modified)
        assert_false(is_mc_modified)

        # Description has been modified
        test_module_code = 'BB1002'
        test_module_name = "Dummy Module 2"
        test_module_desc = "This module's description has been MODIFIED"
        test_module_mc = 2

        test_post_data = self.TestEditModuleData("submit", test_module_code,
                                                 test_module_name, test_module_desc,
                                                 test_module_mc)
        self.module_edit_handler.POST(test_post_data)

        modified_modules = self.modified_modules_handler.get_modules_with_modified_details()
        assert_not_equal(number_of_modified_modules, len(modified_modules))
        number_of_modified_modules = len(modified_modules)

        is_in_modified_modules = False
        is_name_modified = None
        is_desc_modified = None
        is_mc_modified = None
        for module in modified_modules:
            code = module[0]
            if code == test_module_code:
                is_in_modified_modules = True
                is_name_modified = module[1][0] is not None
                is_desc_modified = module[1][1] is not None
                is_mc_modified = module[1][2] is not None
        assert_true(is_in_modified_modules)
        assert_false(is_name_modified)
        assert_true(is_desc_modified)
        assert_false(is_mc_modified)

        # MC has been modified
        test_module_code = 'BB1003'
        test_module_name = "Dummy Module 3"
        test_module_desc = "This module's quota for sem 2 is modified"
        test_module_mc = 10

        test_post_data = self.TestEditModuleData("submit", test_module_code,
                                                 test_module_name, test_module_desc,
                                                 test_module_mc)
        self.module_edit_handler.POST(test_post_data)

        modified_modules = self.modified_modules_handler.get_modules_with_modified_details()
        assert_not_equal(number_of_modified_modules, len(modified_modules))
        number_of_modified_modules = len(modified_modules)

        is_in_modified_modules = False
        is_name_modified = None
        is_desc_modified = None
        is_mc_modified = None
        for module in modified_modules:
            code = module[0]
            if code == test_module_code:
                is_in_modified_modules = True
                is_name_modified = module[1][0] is not None
                is_desc_modified = module[1][1] is not None
                is_mc_modified = module[1][2] is not None
        assert_true(is_in_modified_modules)
        assert_false(is_name_modified)
        assert_false(is_desc_modified)
        assert_true(is_mc_modified)


    def test_module_edit_back_to_original(self):
        '''
            Test that if a module's detail is previously modified,
            but is then edited back to original,
            it will disappear from the module backup table
        '''
        number_of_modified_modules = len(model.get_modules_with_modified_details())

        # Details modified
        test_module_code = 'BB2001'
        test_module_name = "Dummy Module NAME MODIFIED"
        test_module_desc = "This module's description has been MODIFIED"
        test_module_mc = 10

        test_post_data = self.TestEditModuleData("submit", test_module_code,
                                                 test_module_name, test_module_desc,
                                                 test_module_mc)
        self.module_edit_handler.POST(test_post_data)

        modified_modules = self.modified_modules_handler.get_modules_with_modified_details()
        # Original info inserted into backup
        assert_not_equal(number_of_modified_modules, len(modified_modules))

        is_in_modified_modules = False
        is_name_modified = None
        is_desc_modified = None
        is_mc_modified = None
        for module in modified_modules:
            code = module[0]
            if code == test_module_code:
                is_in_modified_modules = True
                is_name_modified = module[1][0] is not None
                is_desc_modified = module[1][1] is not None
                is_mc_modified = module[1][2] is not None
        assert_true(is_in_modified_modules)
        assert_true(is_name_modified)
        assert_true(is_desc_modified)
        assert_true(is_mc_modified)

        # Details edited back to original
        test_module_code = 'BB2001'
        test_module_name = 'Dummy Module 1'
        test_module_desc = "This module is unmounted from sem 1"
        test_module_mc = 1

        test_post_data = self.TestEditModuleData("submit", test_module_code,
                                                 test_module_name, test_module_desc,
                                                 test_module_mc)
        self.module_edit_handler.POST(test_post_data)

        modified_modules = self.modified_modules_handler.get_modules_with_modified_details()
        # Original info removed from backup
        assert_equal(number_of_modified_modules, len(modified_modules))

        is_in_modified_modules = False
        for module in modified_modules:
            code = module[0]
            if code == test_module_code:
                is_in_modified_modules = True
        assert_false(is_in_modified_modules)


    def test_module_modify_overview(self):
        '''
            Test if the overview for modified modules (modifyType=all)
            shows the correct boolean for whether a module's
            mounting/quota/module details have been modified.

            Also check that when a module's mounting is modified
            and the quota is specified,
            the module's quota will also be considered as modified
        '''
        modified_modules = self.modified_modules_handler.get_all_modified_modules()

        # Quota is modified
        test_module_code = 'BB1004'
        is_in_modified_modules = False
        is_mounting_modified = None
        is_quota_modified = None
        is_module_details_modified = None
        for module in modified_modules:
            code = module[0]
            if code == test_module_code:
                is_in_modified_modules = True
                is_mounting_modified = module[1]
                is_quota_modified = module[2]
                is_module_details_modified = module[3]
                break
        assert_true(is_in_modified_modules)
        assert_false(is_mounting_modified)
        assert_true(is_quota_modified)
        assert_false(is_module_details_modified)

        # Mounting is modified
        test_module_code = 'BB2002'
        is_in_modified_modules = False
        is_mounting_modified = None
        is_quota_modified = None
        is_module_details_modified = None
        for module in modified_modules:
            code = module[0]
            if code == test_module_code:
                is_in_modified_modules = True
                is_mounting_modified = module[1]
                is_quota_modified = module[2]
                is_module_details_modified = module[3]
                break
        assert_true(is_in_modified_modules)
        assert_true(is_mounting_modified)
        assert_true(is_quota_modified)  # Quota is also considered modified
        assert_false(is_module_details_modified)

        # Mounting and module details are modified
        test_module_code = 'BB2003'
        test_module_name = 'Dummy Module 1'
        test_module_desc = "This module's mounting and module details are modified"
        test_module_mc = 1
        test_post_data = self.TestEditModuleData("submit", test_module_code,
                                                 test_module_name, test_module_desc,
                                                 test_module_mc)
        self.module_edit_handler.POST(test_post_data)

        modified_modules = self.modified_modules_handler.get_all_modified_modules()
        is_in_modified_modules = False
        is_mounting_modified = None
        is_quota_modified = None
        is_module_details_modified = None
        for module in modified_modules:
            code = module[0]
            if code == test_module_code:
                is_in_modified_modules = True
                is_mounting_modified = module[1]
                is_quota_modified = module[2]
                is_module_details_modified = module[3]
                break
        assert_true(is_in_modified_modules)
        assert_true(is_mounting_modified)
        assert_true(is_quota_modified)  # Quota is also considered modified
        assert_true(is_module_details_modified)


    class TestRestoreModuleData(object):
        '''
            Emulate the data submitted by the 'Restore Module' button
            on the 'Modified Modules' pages
        '''
        def __init__(self, restoreType, code, currentAySem, targetAySem, quota, mountingChange):
            self.restoreType = restoreType
            self.code = code
            self.currentAySem = currentAySem
            self.targetAySem = targetAySem
            self.quota = quota
            self.mountingChange = mountingChange


    def test_quota_restore(self):
        '''
            Test if a module's whose quota is modified can be restored
            and if the module will disappear from the table of modules with modified quota
        '''
        # Restore quota to original number
        test_module_code = 'BB3001'
        test_current_quota = 10
        test_target_aysem = self.next_ay+" Sem 1"
        test_modified_quota = 999

        modified_modules = self.modified_modules_handler.get_modules_with_modified_quota()
        is_in_modified_modules = False
        current_quota = -1
        modified_quota = -1

        for module in modified_modules:
            code = module[0]
            if code == test_module_code:
                is_in_modified_modules = True
                current_quota = module[3]
                modified_quota = module[4]
                break

        assert_true(is_in_modified_modules)
        assert_equal(test_current_quota, current_quota)
        assert_equal(test_modified_quota, modified_quota)

        test_post_data = self.TestRestoreModuleData("quota", test_module_code, None,
                                                    test_target_aysem, test_current_quota, None)
        self.module_restore_handler.POST(test_post_data)

        modified_modules = self.modified_modules_handler.get_modules_with_modified_quota()
        is_in_modified_modules = False
        for module in modified_modules:
            code = module[0]
            if code == test_module_code:
                is_in_modified_modules = True
                current_quota = module[3]
                modified_quota = module[4]
                break
        assert_false(is_in_modified_modules)

        restored_quota = model.get_quota_of_target_tenta_ay_sem(test_module_code, test_target_aysem)
        assert_equal(restored_quota, test_current_quota)

        # Restore quota to unspecified
        test_module_code = 'BB3002'
        test_current_quota = None
        test_target_aysem = self.next_ay+" Sem 1"
        test_modified_quota = 999

        modified_modules = self.modified_modules_handler.get_modules_with_modified_quota()
        is_in_modified_modules = False
        current_quota = -1
        modified_quota = -1

        for module in modified_modules:
            code = module[0]
            if code == test_module_code:
                is_in_modified_modules = True
                current_quota = module[3]
                modified_quota = module[4]
                break

        assert_true(is_in_modified_modules)
        assert_equal(test_current_quota, current_quota)
        assert_equal(test_modified_quota, modified_quota)

        test_post_data = self.TestRestoreModuleData("quota", test_module_code, None,
                                                    test_target_aysem, test_current_quota, None)
        self.module_restore_handler.POST(test_post_data)

        modified_modules = self.modified_modules_handler.get_modules_with_modified_quota()
        is_in_modified_modules = False
        for module in modified_modules:
            code = module[0]
            if code == test_module_code:
                is_in_modified_modules = True
                current_quota = module[3]
                modified_quota = module[4]
                break
        assert_false(is_in_modified_modules)

        restored_quota = model.get_quota_of_target_tenta_ay_sem(test_module_code, test_target_aysem)
        assert_equal(restored_quota, test_current_quota)


    def test_mounting_restore(self):
        '''
            Test if a module's whose mounting is modified can be restored
            and if the module will disappear from the table of modules with modified mounting
        '''
        # Restore to unmounted
        test_module_code = 'BB3003'
        test_target_aysem = self.next_ay+" Sem 2"

        modified_modules = self.modified_modules_handler.get_modules_with_modified_mounting()
        is_in_modified_modules = False
        mounting_change = None

        for module in modified_modules:
            code = module[0]
            if code == test_module_code:
                is_in_modified_modules = True
                mounting_change = module[3]
                break

        assert_true(is_in_modified_modules)
        assert_equal(mounting_change, 1)  # Mounted

        test_post_data = self.TestRestoreModuleData("mounting", test_module_code, None,
                                                    test_target_aysem, None, mounting_change)
        self.module_restore_handler.POST(test_post_data)

        modified_modules = self.modified_modules_handler.get_modules_with_modified_mounting()
        is_in_modified_modules = False
        for module in modified_modules:
            code = module[0]
            if code == test_module_code:
                is_in_modified_modules = True
                break
        assert_false(is_in_modified_modules)

        restored_mounting = model.get_mounting_of_target_tenta_ay_sem(test_module_code,
                                                                      test_target_aysem)
        assert_equal(restored_mounting, False)  # Not Mounted

        # Restore to mounted
        test_module_code = 'BB3004'
        test_current_aysem = self.current_ay+" Sem 2"
        test_target_aysem = self.next_ay+" Sem 2"

        modified_modules = self.modified_modules_handler.get_modules_with_modified_mounting()
        is_in_modified_modules = False
        mounting_change = None

        for module in modified_modules:
            code = module[0]
            if code == test_module_code:
                is_in_modified_modules = True
                mounting_change = module[3]
                break

        assert_true(is_in_modified_modules)
        assert_equal(mounting_change, 0)  # Not Mounted

        test_post_data = self.TestRestoreModuleData("mounting", test_module_code,
                                                    test_current_aysem, test_target_aysem,
                                                    None, mounting_change)
        self.module_restore_handler.POST(test_post_data)

        modified_modules = self.modified_modules_handler.get_modules_with_modified_mounting()
        is_in_modified_modules = False
        for module in modified_modules:
            code = module[0]
            if code == test_module_code:
                is_in_modified_modules = True
                break
        assert_false(is_in_modified_modules)

        restored_mounting = model.get_mounting_of_target_tenta_ay_sem(test_module_code,
                                                                      test_target_aysem)
        assert_equal(restored_mounting, True)  # Mounted


    def test_details_restore(self):
        '''
            Test if a module's whose details are modified can be restored
            and if the module will disappear from the table of modules with modified details
        '''
        # Name is modified and will be restored
        test_module_code = 'BB3005'
        test_module_name = 'Dummy Module 5'
        test_module_orig_name = 'Original Module Name'

        module_info = model.get_module(test_module_code)
        module_name = module_info[1]
        assert_equal(module_name, test_module_name)

        modified_modules = self.modified_modules_handler.get_modules_with_modified_details()
        is_in_modified_modules = False
        is_name_modified = None
        is_desc_modified = None
        is_mc_modified = None

        for module in modified_modules:
            code = module[0]
            if code == test_module_code:
                is_in_modified_modules = True
                is_name_modified = module[1][0]
                is_desc_modified = module[1][1]
                is_mc_modified = module[1][2]
                break

        assert_true(is_in_modified_modules)
        assert_true(is_name_modified)
        assert_false(is_desc_modified)
        assert_false(is_mc_modified)

        test_post_data = self.TestRestoreModuleData("moduleDetails", test_module_code,
                                                    None, None, None, None)
        self.module_restore_handler.POST(test_post_data)

        modified_modules = self.modified_modules_handler.get_modules_with_modified_details()
        is_in_modified_modules = False
        for module in modified_modules:
            code = module[0]
            if code == test_module_code:
                is_in_modified_modules = True
                break
        assert_false(is_in_modified_modules)

        module_info = model.get_module(test_module_code)
        module_name = module_info[1]
        assert_equal(module_name, test_module_orig_name)

        # Name, description and MC are modified and will be restored
        test_module_code = 'BB3006'
        test_module_name = 'Dummy Module 6'
        test_module_desc = "This module's name, description and MC will be restored"
        test_module_mc = 6
        test_module_orig_name = 'Original Module Name'
        test_module_orig_desc = 'Original Module Description'
        test_module_orig_mc = 0

        module_info = model.get_module(test_module_code)
        module_name = module_info[1]
        module_desc = module_info[2]
        module_mc = module_info[3]
        assert_equal(module_name, test_module_name)
        assert_equal(module_desc, test_module_desc)
        assert_equal(module_mc, test_module_mc)

        modified_modules = self.modified_modules_handler.get_modules_with_modified_details()
        is_in_modified_modules = False
        is_name_modified = None
        is_desc_modified = None
        is_mc_modified = None

        for module in modified_modules:
            code = module[0]
            if code == test_module_code:
                is_in_modified_modules = True
                is_name_modified = module[1][0]
                is_desc_modified = module[1][1]
                is_mc_modified = module[1][2]
                break

        assert_true(is_in_modified_modules)
        assert_true(is_name_modified)
        assert_true(is_desc_modified)
        assert_true(is_mc_modified)

        test_post_data = self.TestRestoreModuleData("moduleDetails", test_module_code,
                                                    None, None, None, None)
        self.module_restore_handler.POST(test_post_data)

        modified_modules = self.modified_modules_handler.get_modules_with_modified_details()
        is_in_modified_modules = False
        for module in modified_modules:
            code = module[0]
            if code == test_module_code:
                is_in_modified_modules = True
                break
        assert_false(is_in_modified_modules)

        module_info = model.get_module(test_module_code)
        module_name = module_info[1]
        module_desc = module_info[2]
        module_mc = module_info[3]
        assert_equal(module_name, test_module_orig_name)
        assert_equal(module_desc, test_module_orig_desc)
        assert_equal(module_mc, test_module_orig_mc)


    def test_mounting_modified_but_not_quota(self):
        '''
            Test that a module whose mounting is modified, but quota has not been specified,
            will only appear in the mounting modified table, but not the quota modified table
        '''
        # This module will appear in BOTH modified mounting table and modified quota table
        test_module_code = 'BB2002'
        test_current_quota = "Unmounted"

        modified_modules = self.modified_modules_handler.get_modules_with_modified_mounting()
        is_in_modified_modules = False
        for module in modified_modules:
            code = module[0]
            if code == test_module_code:
                is_in_modified_modules = True
                break
        assert_true(is_in_modified_modules)

        modified_modules = self.modified_modules_handler.get_modules_with_modified_quota()
        is_in_modified_modules = False
        for module in modified_modules:
            code = module[0]
            current_quota = module[3]
            if code == test_module_code:
                is_in_modified_modules = True
                break
        assert_true(is_in_modified_modules)
        assert_equal(current_quota, test_current_quota)

        # This module will ONLY appear in modified mounting table
        test_module_code = 'BB2004'

        modified_modules = self.modified_modules_handler.get_modules_with_modified_mounting()
        is_in_modified_modules = False
        for module in modified_modules:
            code = module[0]
            if code == test_module_code:
                is_in_modified_modules = True
                break
        assert_true(is_in_modified_modules)

        modified_modules = self.modified_modules_handler.get_modules_with_modified_quota()
        is_in_modified_modules = False
        for module in modified_modules:
            code = module[0]
            if code == test_module_code:
                is_in_modified_modules = True
                break
        assert_false(is_in_modified_modules)
