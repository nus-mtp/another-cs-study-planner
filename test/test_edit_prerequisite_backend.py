'''
    test_edit_prerequisite_backend.py
    Contains test cases for functions to edit prerequisites.
'''
from nose.tools import assert_equal, assert_false, assert_true
from components import model


# HOW TO RUN NOSE TESTS
# 1. Make sure you are in cs-modify main directory
# 2. Make sure the path "C:\Python27\Scripts" is added in your environment variables
# 3. Enter in cmd: "nosetests test/"
# 4. Nose will run all the tests inside the test/ folder

class TestCode(object):
    '''
        This class runs the test cases for functions to edit prerequisites.
    '''
    def __init__(self):
        self.test_module_code = "AA1111"
        self.test_module_name = "Dummy Module"
        self.test_module_desc = "Dummy Description"
        self.test_module_mc = 4
        self.test_module_status = "Active"

        self.no_prereq_to_one_prereq_tested = False
        self.no_prereq_to_no_prereq_tested = False
        self.no_prereq_to_multiple_prereq_tested = False
        self.prereq_to_one_prereq_tested = False
        self.prereq_to_no_prereq_tested = False
        self.prereq_to_multiple_prereq_tested = False
        self.edit_prereq_duplicate_tested = False
        self.edit_prereq_non_existent_tested = False

        self.test_prereq_code = "BB1111"
        self.test_prereq_index = 0
        self.test_prereq2_code = "BB1112"
        self.test_prereq2_index = 1
        self.test_prereq3_code = "BB1113"
        self.test_prereq3_index = 1
        self.test_invalid_module_code = "ZZ1597"


    def setUp(self):
        '''
            Populate database and perform testing
        '''
        model.add_module(self.test_module_code, self.test_module_name, self.test_module_desc,
                         self.test_module_mc, self.test_module_status)
        model.add_module(self.test_prereq_code, self.test_module_name, self.test_module_desc,
                         self.test_module_mc, self.test_module_status)
        model.add_module(self.test_prereq2_code, self.test_module_name, self.test_module_desc,
                         self.test_module_mc, self.test_module_status)
        model.add_module(self.test_prereq3_code, self.test_module_name, self.test_module_desc,
                         self.test_module_mc, self.test_module_status)
        self.test_no_prereq_to_one_prereq()
        self.no_prereq_to_one_prereq_tested = True
        self.test_prereq_to_one_prereq()
        self.prereq_to_one_prereq_tested = True
        self.test_no_prereq_to_no_prereq()
        self.no_prereq_to_no_prereq_tested = True
        self.test_prereq_to_no_prereq()
        self.prereq_to_no_prereq_tested = True
        self.test_no_prereq_to_multiple_prereq()
        self.no_prereq_to_multiple_prereq_tested = True
        self.test_prereq_to_multiple_prereq()
        self.prereq_to_multiple_prereq_tested = True
        self.test_edit_prereq_duplicate_modules()
        self.edit_prereq_duplicate_tested = True
        self.test_edit_prereq_non_existent_modules()
        self.edit_prereq_non_existent_tested = True


    def tearDown(self):
        '''
            Clean up the database after all test cases are ran
        '''
        model.delete_module(self.test_module_code)
        model.delete_module(self.test_prereq_code)
        model.delete_module(self.test_prereq2_code)
        model.delete_module(self.test_prereq3_code)


    def test_no_prereq_to_one_prereq(self):
        '''
            Tests editing prerequisite on a module originally with no prereq
            to 1 prereq.
        '''
        if not self.no_prereq_to_one_prereq_tested:
            prereq_units_to_change_to = [[self.test_prereq_code]]
            outcome = model.edit_prerequisite(self.test_module_code, prereq_units_to_change_to)

            assert_true(outcome)

            prereq_info = model.get_prerequisite(self.test_module_code)
            assert_true(prereq_info is not None)
            assert_equal(self.test_prereq_index, prereq_info[0][0])
            assert_equal(self.test_prereq_code, prereq_info[0][1])

            model.delete_all_prerequisite(self.test_module_code)

            prereq_info = model.get_prerequisite(self.test_module_code)
            assert_true(len(prereq_info) == 0)
            return


    def test_prereq_to_one_prereq(self):
        '''
            Tests editing prerequisite on a module to 1 prereq.
        '''
        if not self.prereq_to_one_prereq_tested:
            model.add_prerequisite(self.test_module_code, self.test_prereq_code,
                                   self.test_prereq_index)

            prereq_units_to_change_to = [[self.test_prereq2_code]]
            outcome = model.edit_prerequisite(self.test_module_code, prereq_units_to_change_to)

            assert_true(outcome)

            prereq_info = model.get_prerequisite(self.test_module_code)
            assert_true(prereq_info is not None)
            assert_equal(self.test_prereq_index, prereq_info[0][0])
            assert_equal(self.test_prereq2_code, prereq_info[0][1])

            model.delete_all_prerequisite(self.test_module_code)

            prereq_info = model.get_prerequisite(self.test_module_code)
            assert_true(len(prereq_info) == 0)
            return


    def test_no_prereq_to_no_prereq(self):
        '''
            Tests editing prerequisite on a module originally with no prereq
            to no prereq.
        '''
        if not self.no_prereq_to_no_prereq_tested:
            prereq_units_to_change_to = []
            outcome = model.edit_prerequisite(self.test_module_code, prereq_units_to_change_to)

            assert_true(outcome)

            prereq_info = model.get_prerequisite(self.test_module_code)

            assert_true(prereq_info is not None)
            assert_true(len(prereq_info) == 0)
            return


    def test_prereq_to_no_prereq(self):
        '''
            Tests editing prerequisite on a module to no prereq.
        '''
        if not self.prereq_to_no_prereq_tested:
            model.add_prerequisite(self.test_module_code, self.test_prereq_code,
                                   self.test_prereq_index)

            prereq_units_to_change_to = []
            outcome = model.edit_prerequisite(self.test_module_code, prereq_units_to_change_to)

            assert_true(outcome)

            prereq_info = model.get_prerequisite(self.test_module_code)
            assert_true(prereq_info is not None)
            assert_true(len(prereq_info) == 0)
            return


    def test_no_prereq_to_multiple_prereq(self):
        '''
            Tests editing prerequisite on a module originally with no prereq
            to multiple prereqs.
        '''
        if not self.no_prereq_to_multiple_prereq_tested:
            prereq_units_to_change_to = [[self.test_prereq_code],
                                         [self.test_prereq2_code, self.test_prereq3_code]]

            outcome = model.edit_prerequisite(self.test_module_code, prereq_units_to_change_to)
            assert_true(outcome)

            prereq_info = model.get_prerequisite(self.test_module_code)

            assert_true(prereq_info is not None)
            assert_equal(self.test_prereq_index, prereq_info[0][0])
            assert_equal(self.test_prereq_code, prereq_info[0][1])
            assert_equal(self.test_prereq2_index, prereq_info[1][0])
            assert_equal(self.test_prereq2_code, prereq_info[1][1])
            assert_equal(self.test_prereq3_index, prereq_info[2][0])
            assert_equal(self.test_prereq3_code, prereq_info[2][1])

            model.delete_all_prerequisite(self.test_module_code)

            prereq_info = model.get_prerequisite(self.test_module_code)
            assert_true(len(prereq_info) == 0)
            return


    def test_prereq_to_multiple_prereq(self):
        '''
            Tests editing prerequisite on a module to multiple prereq.
        '''
        if not self.prereq_to_multiple_prereq_tested:
            model.add_prerequisite(self.test_module_code, self.test_prereq_code,
                                   self.test_prereq_index)

            prereq_units_to_change_to = [[self.test_prereq_code],
                                         [self.test_prereq2_code, self.test_prereq3_code]]

            outcome = model.edit_prerequisite(self.test_module_code, prereq_units_to_change_to)
            assert_true(outcome)

            prereq_info = model.get_prerequisite(self.test_module_code)

            assert_true(prereq_info is not None)
            assert_equal(self.test_prereq_index, prereq_info[0][0])
            assert_equal(self.test_prereq_code, prereq_info[0][1])
            assert_equal(self.test_prereq2_index, prereq_info[1][0])
            assert_equal(self.test_prereq2_code, prereq_info[1][1])
            assert_equal(self.test_prereq3_index, prereq_info[2][0])
            assert_equal(self.test_prereq3_code, prereq_info[2][1])

            model.delete_all_prerequisite(self.test_module_code)

            prereq_info = model.get_prerequisite(self.test_module_code)
            assert_true(len(prereq_info) == 0)
            return


    def test_edit_prereq_duplicate_modules(self):
        '''
            Tests editing prerequisite on a module to prereqs with duplicates,
            note: this test case should fail to edit.
        '''
        if not self.edit_prereq_duplicate_tested:
            model.add_prerequisite(self.test_module_code, self.test_prereq_code,
                                   self.test_prereq_index)

            prereq_units_to_change_to = [[self.test_prereq2_code],
                                         [self.test_prereq2_code]]

            outcome = model.edit_prerequisite(self.test_module_code, prereq_units_to_change_to)
            assert_false(outcome)

            prereq_info = model.get_prerequisite(self.test_module_code)

            assert_true(prereq_info is not None)
            assert_equal(self.test_prereq_index, prereq_info[0][0])
            assert_equal(self.test_prereq_code, prereq_info[0][1])

            model.delete_all_prerequisite(self.test_module_code)

            prereq_info = model.get_prerequisite(self.test_module_code)
            assert_true(len(prereq_info) == 0)

            # Test another form

            model.add_prerequisite(self.test_module_code, self.test_prereq_code,
                                   self.test_prereq_index)

            prereq_units_to_change_to = [[self.test_prereq2_code, self.test_prereq2_code]]

            outcome = model.edit_prerequisite(self.test_module_code, prereq_units_to_change_to)
            assert_false(outcome)

            prereq_info = model.get_prerequisite(self.test_module_code)

            assert_true(prereq_info is not None)
            assert_equal(self.test_prereq_index, prereq_info[0][0])
            assert_equal(self.test_prereq_code, prereq_info[0][1])

            model.delete_all_prerequisite(self.test_module_code)

            prereq_info = model.get_prerequisite(self.test_module_code)
            assert_true(len(prereq_info) == 0)
            return


    def test_edit_prereq_non_existent_modules(self):
        '''
            Tests editing prerequisite on a module to prereqs which does
            not exist, note: this test case should fail to edit.
        '''
        if not self.edit_prereq_non_existent_tested:
            model.add_prerequisite(self.test_module_code, self.test_prereq_code,
                                   self.test_prereq_index)

            prereq_units_to_change_to = [[self.test_prereq2_code],
                                         [self.test_invalid_module_code]]

            outcome = model.edit_prerequisite(self.test_module_code, prereq_units_to_change_to)
            assert_false(outcome)

            prereq_info = model.get_prerequisite(self.test_module_code)

            assert_true(prereq_info is not None)
            assert_equal(self.test_prereq_index, prereq_info[0][0])
            assert_equal(self.test_prereq_code, prereq_info[0][1])

            model.delete_all_prerequisite(self.test_module_code)

            prereq_info = model.get_prerequisite(self.test_module_code)
            assert_true(len(prereq_info) == 0)

            # Test another form

            model.add_prerequisite(self.test_module_code, self.test_prereq_code,
                                   self.test_prereq_index)

            prereq_units_to_change_to = [[self.test_invalid_module_code,
                                          self.test_prereq2_code]]

            outcome = model.edit_prerequisite(self.test_module_code, prereq_units_to_change_to)
            assert_false(outcome)

            prereq_info = model.get_prerequisite(self.test_module_code)

            assert_true(prereq_info is not None)
            assert_equal(self.test_prereq_index, prereq_info[0][0])
            assert_equal(self.test_prereq_code, prereq_info[0][1])

            model.delete_all_prerequisite(self.test_module_code)

            prereq_info = model.get_prerequisite(self.test_module_code)
            assert_true(len(prereq_info) == 0)
            return
