'''
test_database.py
Contains test cases for database related functions.
'''
from nose.tools import assert_equal, assert_false, assert_in, assert_true
from components import model


# HOW TO RUN NOSE TESTS
# 1. Make sure you are in cs-modify main directory
# 2. Make sure the path "C:\Python27\Scripts" is added in your environment variables
# 3. Enter in cmd: "nosetests test/"
# 4. Nose will run all the tests inside the test/ folder

class TestCode(object):
    '''
    This class runs the test cases for database related functions.
    '''
    def __init__(self):
        self.test_module_code = "CS2103T"

        self.mounting_table_column_count = 3
        self.test_module_mounted_count = 2
        self.test_module_tenta_mount_ay_s1 = "AY 17/18 Sem 1"
        self.test_module_tenta_mount_ay_s2 = "AY 17/18 Sem 2"
        self.test_module_quota1 = 190
        self.test_module_quota2 = 160


    def test_get_module(self):
        '''
            Tests getting of modules.
        '''
        module_table_column_count = 5
        test_module_name = "Software Engineering"
        test_module_desc = "This module introduces the necessary conceptual and analytical "+\
                            "tools for systematic and rigorous development of software systems."

        test_module_status = "Active"
        test_module_mc = 4

        module_info = model.get_module(self.test_module_code)
        assert_equal(module_table_column_count, len(module_info))
        assert_equal(self.test_module_code, module_info[0])
        assert_equal(test_module_name, module_info[1])
        assert_in(test_module_desc, module_info[2])
        assert_equal(test_module_mc, module_info[3])
        assert_equal(test_module_status, module_info[4].rstrip())


    def test_get_fixed_mount_and_quota(self):
        '''
            Tests getting of fixed mountings and quota.
        '''
        test_module_fixed_mounted_ay_s1 = "AY 16/17 Sem 1"
        test_module_fixed_mounted_ay_s2 = "AY 16/17 Sem 2"

        mountings = model.get_fixed_mounting_and_quota(self.test_module_code)
        assert_equal(self.test_module_mounted_count, len(mountings))
        mounting_and_quota1 = mountings[0]
        assert_equal(test_module_fixed_mounted_ay_s1, mounting_and_quota1[0])
        assert_equal(self.test_module_quota1, mounting_and_quota1[1])

        mounting_and_quota2 = mountings[1]
        assert_equal(test_module_fixed_mounted_ay_s2, mounting_and_quota2[0])
        assert_equal(self.test_module_quota2, mounting_and_quota2[1])


    def test_get_tenta_mount_and_quota(self):
        '''
            Tests getting of tentative mountings and quota.
        '''
        mountings = model.get_tenta_mounting_and_quota(self.test_module_code)
        assert_equal(self.test_module_mounted_count, len(mountings))

        mounting_and_quota1 = mountings[0]
        assert_equal(self.test_module_tenta_mount_ay_s1, mounting_and_quota1[0])
        assert_equal(self.test_module_quota1, mounting_and_quota1[1])

        mounting_and_quota2 = mountings[1]
        assert_equal(self.test_module_tenta_mount_ay_s2, mounting_and_quota2[0])
        assert_equal(self.test_module_quota2, mounting_and_quota2[1])


    def test_add_and_delete_module(self):
        '''
            Tests addition and deletion of modules.
        '''
        model.add_module("AA1111", "Dummy Module", "Dummy Description", 1)
        module_info = model.get_module("AA1111")
        assert_true(module_info is not None)
        assert_equal("New", module_info[4].rstrip())

        model.delete_module("AA1111")
        module_info = model.get_module("AA1111")
        assert_true(module_info is None)


    def test_add_mod_with_repeat_code(self):
        '''
            Tests adding of module with duplicated code. Should fail.
        '''
        model.add_module("AA1111", "Dummy Module", "Dummy Description", 1)

        # Not duplicate code --> success
        outcome = model.add_module("AA2222", "Dummy Module", "Dummy Description", 1)
        assert_true(outcome)

        # Duplicate code --> fail
        outcome = model.add_module("AA1111", "Dummy Module", "Dummy Description", 1)
        assert_false(outcome)

        model.delete_module("AA1111")
        model.delete_module("AA2222")
