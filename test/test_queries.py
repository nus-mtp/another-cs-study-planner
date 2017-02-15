'''
test_queries.py
Contains test cases for database query related functions.
'''
from nose.tools import assert_equal
from components import model

# HOW TO RUN NOSE TESTS
# 1. Make sure you are in cs-modify main directory
# 2. Make sure the path "C:\Python27\Scripts" is added in your environment variables
# 3. Enter in cmd: "nosetests test/"
# 4. Nose will run all the tests inside the test/ folder

class TestCode(object):
    '''
        This class runs the test cases for database query related functions.
    '''
    def __init__(self):
        self.num_column_for_each_year = 2

    def test_query_num_students_in_year_of_study(self):
        '''
            Tests querying number of students at each year of study
        '''
        num_in_year = [4, 3, 3, 3]

        table_of_year_of_study_with_count = \
            model.get_num_students_by_yr_study()

        num_of_rows_expected = 4
        for x in range(1, num_of_rows_expected):
            current_row = table_of_year_of_study_with_count[x]
            assert_equal(self.num_column_for_each_year, len(current_row))
            current_year = current_row[0]
            current_number_of_student = current_row[1]
            assert_equal(num_in_year[current_year - 1], current_number_of_student)
