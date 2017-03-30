'''
    test_edit_preclusion_backend.py
    Contains test cases for functions to edit preclusions.
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
        This class runs the test cases for functions to edit preclusions.
    '''
    def __init__(self):
        self.test_module_code = "AA1111"
        self.test_module_name = "Dummy Module"
        self.test_module_desc = "Dummy Description"
        self.test_module_mc = 4
        self.test_module_status = "Active"

        self.no_preclude_to_one_preclude_tested = False
        self.no_preclude_to_no_preclude_tested = False
        self.no_preclude_to_multiple_preclude_tested = False
        self.preclude_to_one_preclude_tested = False
        self.preclude_to_no_preclude_tested = False
        self.preclude_to_multiple_preclude_tested = False
        self.edit_preclude_duplicate_tested = False
        self.edit_preclude_non_existent_tested = False

        self.test_preclude_code = "BB1111"
        self.test_preclude2_code = "BB1112"
        self.test_preclude3_code = "BB1113"
        self.test_invalid_module_code = "ZZ1597"


    def setUp(self):
        '''
            Populate database and perform testing
        '''
        model.add_module(self.test_module_code, self.test_module_name, self.test_module_desc,
                         self.test_module_mc, self.test_module_status)
        model.add_module(self.test_preclude_code, self.test_module_name, self.test_module_desc,
                         self.test_module_mc, self.test_module_status)
        model.add_module(self.test_preclude2_code, self.test_module_name, self.test_module_desc,
                         self.test_module_mc, self.test_module_status)
        model.add_module(self.test_preclude3_code, self.test_module_name, self.test_module_desc,
                         self.test_module_mc, self.test_module_status)
        self.test_no_preclude_to_one_preclude()
        self.no_preclude_to_one_preclude_tested = True
        self.test_preclude_to_one_preclude()
        self.preclude_to_one_preclude_tested = True
        self.test_no_preclude_to_no_preclude()
        self.no_preclude_to_no_preclude_tested = True
        self.test_preclude_to_no_preclude()
        self.preclude_to_no_preclude_tested = True
        self.test_no_preclude_to_multiple_preclude()
        self.no_preclude_to_multiple_preclude_tested = True
        self.test_preclude_to_multiple_preclude()
        self.preclude_to_multiple_preclude_tested = True
        self.test_edit_preclude_duplicate_modules()
        self.edit_preclude_duplicate_tested = True
        self.test_edit_preclude_non_existent_modules()
        self.edit_preclude_non_existent_tested = True


    def tearDown(self):
        '''
            Clean up the database after all test cases are ran
        '''
        model.delete_module(self.test_module_code)
        model.delete_module(self.test_preclude_code)
        model.delete_module(self.test_preclude2_code)
        model.delete_module(self.test_preclude3_code)


    def test_no_preclude_to_one_preclude(self):
        '''
            Tests editing preclusion on a module originally with no preclude
            to 1 preclude.
        '''
        if not self.no_preclude_to_one_preclude_tested:
            preclude_units_to_change_to = [self.test_preclude_code]
            outcome = model.edit_preclusion(self.test_module_code, preclude_units_to_change_to)

            assert_true(outcome)

            preclude_info = model.get_preclusion(self.test_module_code)
            assert_true(preclude_info is not None)
            assert_equal(self.test_preclude_code, preclude_info[0][0])

            model.delete_all_preclusions(self.test_module_code)

            preclude_info = model.get_preclusion(self.test_module_code)
            assert_true(len(preclude_info) == 0)
            return


    def test_preclude_to_one_preclude(self):
        '''
            Tests editing preclusion on a module to 1 preclude.
        '''
        if not self.preclude_to_one_preclude_tested:
            model.add_preclusion(self.test_module_code, self.test_preclude_code)

            preclude_units_to_change_to = [self.test_preclude2_code]
            outcome = model.edit_preclusion(self.test_module_code, preclude_units_to_change_to)

            assert_true(outcome)

            preclude_info = model.get_preclusion(self.test_module_code)
            assert_true(preclude_info is not None)
            assert_equal(self.test_preclude2_code, preclude_info[0][0])

            model.delete_all_preclusions(self.test_module_code)

            preclude_info = model.get_preclusion(self.test_module_code)
            assert_true(len(preclude_info) == 0)
            return


    def test_no_preclude_to_no_preclude(self):
        '''
            Tests editing preclusion on a module originally with no preclude
            to no preclude.
        '''
        if not self.no_preclude_to_no_preclude_tested:
            preclude_units_to_change_to = []
            outcome = model.edit_preclusion(self.test_module_code, preclude_units_to_change_to)

            assert_true(outcome)

            preclude_info = model.get_preclusion(self.test_module_code)

            assert_true(preclude_info is not None)
            assert_true(len(preclude_info) == 0)
            return


    def test_preclude_to_no_preclude(self):
        '''
            Tests editing preclusion on a module to no preclude.
        '''
        if not self.preclude_to_no_preclude_tested:
            model.add_preclusion(self.test_module_code, self.test_preclude_code)

            preclude_units_to_change_to = []
            outcome = model.edit_preclusion(self.test_module_code, preclude_units_to_change_to)

            assert_true(outcome)

            preclude_info = model.get_preclusion(self.test_module_code)
            assert_true(preclude_info is not None)
            assert_true(len(preclude_info) == 0)
            return


    def test_no_preclude_to_multiple_preclude(self):
        '''
            Tests editing preclusion on a module originally with no preclude
            to multiple precludes.
        '''
        if not self.no_preclude_to_multiple_preclude_tested:
            preclude_units_to_change_to = [self.test_preclude_code,
                                           self.test_preclude2_code, self.test_preclude3_code]

            outcome = model.edit_preclusion(self.test_module_code, preclude_units_to_change_to)
            assert_true(outcome)

            preclude_info = model.get_preclusion(self.test_module_code)

            assert_true(preclude_info is not None)
            assert_equal(self.test_preclude_code, preclude_info[0][0])
            assert_equal(self.test_preclude2_code, preclude_info[1][0])
            assert_equal(self.test_preclude3_code, preclude_info[2][0])

            model.delete_all_preclusions(self.test_module_code)

            preclude_info = model.get_preclusion(self.test_module_code)
            assert_true(len(preclude_info) == 0)
            return


    def test_preclude_to_multiple_preclude(self):
        '''
            Tests editing preclusion on a module to multiple preclude.
        '''
        if not self.preclude_to_multiple_preclude_tested:
            model.add_preclusion(self.test_module_code, self.test_preclude_code)

            preclude_units_to_change_to = [self.test_preclude_code,
                                           self.test_preclude2_code, self.test_preclude3_code]

            outcome = model.edit_preclusion(self.test_module_code, preclude_units_to_change_to)
            assert_true(outcome)

            preclude_info = model.get_preclusion(self.test_module_code)

            assert_true(preclude_info is not None)
            assert_equal(self.test_preclude_code, preclude_info[0][0])
            assert_equal(self.test_preclude2_code, preclude_info[1][0])
            assert_equal(self.test_preclude3_code, preclude_info[2][0])

            model.delete_all_preclusions(self.test_module_code)

            preclude_info = model.get_preclusion(self.test_module_code)
            assert_true(len(preclude_info) == 0)
            return


    def test_edit_preclude_duplicate_modules(self):
        '''
            Tests editing preclusion on a module to precludes with duplicates,
            note: this test case should fail to edit.
        '''
        if not self.edit_preclude_duplicate_tested:
            model.add_preclusion(self.test_module_code, self.test_preclude_code)

            preclude_units_to_change_to = [self.test_preclude2_code,
                                           self.test_preclude2_code]

            outcome = model.edit_preclusion(self.test_module_code, preclude_units_to_change_to)
            assert_false(outcome)

            preclude_info = model.get_preclusion(self.test_module_code)

            assert_true(preclude_info is not None)
            assert_equal(self.test_preclude_code, preclude_info[0][0])

            model.delete_all_preclusions(self.test_module_code)

            preclude_info = model.get_preclusion(self.test_module_code)
            assert_true(len(preclude_info) == 0)


    def test_edit_preclude_non_existent_modules(self):
        '''
            Tests editing preclusion on a module to precludes which does
            not exist, note: this test case should fail to edit.
        '''
        if not self.edit_preclude_non_existent_tested:
            model.add_preclusion(self.test_module_code, self.test_preclude_code)

            preclude_units_to_change_to = [self.test_preclude2_code,
                                           self.test_invalid_module_code]

            outcome = model.edit_preclusion(self.test_module_code, preclude_units_to_change_to)
            assert_false(outcome)

            preclude_info = model.get_preclusion(self.test_module_code)

            assert_true(preclude_info is not None)
            assert_equal(self.test_preclude_code, preclude_info[0][0])

            model.delete_all_preclusions(self.test_module_code)

            preclude_info = model.get_preclusion(self.test_module_code)
            assert_true(len(preclude_info) == 0)

            # Test another form

            model.add_preclusion(self.test_module_code, self.test_preclude_code)

            preclude_units_to_change_to = [self.test_invalid_module_code,
                                           self.test_preclude2_code]

            outcome = model.edit_preclusion(self.test_module_code, preclude_units_to_change_to)
            assert_false(outcome)

            preclude_info = model.get_preclusion(self.test_module_code)

            assert_true(preclude_info is not None)
            assert_equal(self.test_preclude_code, preclude_info[0][0])

            model.delete_all_preclusions(self.test_module_code)

            preclude_info = model.get_preclusion(self.test_module_code)
            assert_true(len(preclude_info) == 0)
            return
