'''
    test_migrate_to_next_ay_sem.py
    Contains test cases related to the migration of
    data across the mounting databases.
'''
from nose.tools import assert_equal, assert_true, assert_false
from components import model


class TestCode(object):
    '''
        This class runs the test cases related to the migration of
        data across the mounting databases.
    '''
    def __init__(self):
        self.initial_past_data = model.get_all_past_mounted_modules()
        self.initial_fixed_data = model.get_all_fixed_mounted_modules()
        self.initial_tenta_data = model.get_all_tenta_mounted_modules()
        self.initial_student_year_data = model.get_num_students_by_yr_study()


    def setUp(self):
        '''
            Migrate the database.
        '''
        model.migrate_to_next_aysem()


    def tearDown(self):
        '''
            Clean up / Reset the database after all test cases are ran
        '''
        model.reset_database()


    def test_fixed_data_migrated_to_past_mounting(self):
        '''
            Tests if fixed data is successfully migrated to past mounting.
        '''
        assert_true(len(self.initial_past_data) == 0)

        current_past_data = model.get_all_past_mounted_modules()
        assert_equal(self.initial_fixed_data, current_past_data)

        current_fixed_data = model.get_all_fixed_mounted_modules()
        for data in self.initial_fixed_data:
            assert_true(data not in current_fixed_data)


    def test_one_ay_tenta_migrated_to_fixed_mounting(self):
        '''
            Tests if 1 AY of data is successfully migrated from tenta mounting
            to fixed mounting.
        '''
        current_fixed_data = model.get_all_fixed_mounted_modules()
        current_tenta_data = model.get_all_tenta_mounted_modules()

        previous_ay = None
        for data in current_fixed_data:
            # Test current fixed data came from initial tentative data, and
            # the data no longer exist in current tentative data
            assert_true(data in self.initial_tenta_data)
            assert_true(data not in current_tenta_data)
            # Test all current fixed data are of the same AY
            ay_sem = data[2]
            ay_without_sem = ay_sem[:-1]

            if previous_ay is None:
                previous_ay = ay_without_sem
            else:
                assert_equal(previous_ay, ay_without_sem)

        # Test that current tentative data does not have AY of
        # those which are supposed to be migrated.
        for data in current_tenta_data:
            ay_sem = data[2]
            ay_without_sem = ay_sem[:-1]
            assert_false(ay_without_sem == previous_ay)


    def test_tentative_mount_not_empty(self):
        '''
            Tests that the tentative mounting table is not empty after migration.
        '''
        current_tenta_data = model.get_all_tenta_mounted_modules()
        assert_true(len(current_tenta_data) != 0)


    def test_module_backup_table_cleared(self):
        '''
            Tests that all the data in the moduleBackup table is cleaned up.
        '''
        module_backup_data = model.get_all_original_module_info()
        assert_true(len(module_backup_data) == 0)


    def test_all_mod_in_fixed_mounting_are_active(self):
        '''
            Tests if all modules in fixed mounting have their statuses
            updated to "Active"
        '''
        current_fixed_data = model.get_all_fixed_mounted_modules()
        for data in current_fixed_data:
            module_code = data[0]
            module_status = model.get_module(module_code)[4]
            assert_equal(module_status.strip(), "Active")


    def test_student_year_incremented_by_one(self):
        '''
            Tests if all the students' year of study is incremented by 1.
        '''
        current_student_year_data = model.get_num_students_by_yr_study()
        for year_number_pair in current_student_year_data:
            year = year_number_pair[0]
            number_of_students = year_number_pair[1]

            if year == 1:
                assert_equal(number_of_students, 0)
            else:
                incremented_year_with_number_pair = (year-1, number_of_students)
                assert_true(incremented_year_with_number_pair in \
                            self.initial_student_year_data)
