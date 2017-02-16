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
        self.num_column_for_each_focus = 2


    def test_query_num_students_in_year_of_study(self):
        '''
            Tests querying number of students at each year of study
        '''
        num_in_year = [4, 3, 3, 3]

        table_of_year_of_study_with_count = \
            model.get_num_students_by_yr_study()

        num_of_rows_expected = 4
        for index_row in range(1, num_of_rows_expected):
            current_row = table_of_year_of_study_with_count[index_row]
            assert_equal(self.num_column_for_each_year, len(current_row))
            current_year = current_row[0]
            current_number_of_student = current_row[1]
            assert_equal(num_in_year[current_year - 1], current_number_of_student)


    def is_table_sorted_by_first_elem(self, table_to_test):
        '''
            Tests if the rows in table_to_test is sorted in ascending order
            according to the first element in each row.
            Table must contain at least one row.
            Returns true if so, false otherwise.
        '''
        FIRST_ELEMENT_INDEX = 0
        previous_element = table_to_test[0][FIRST_ELEMENT_INDEX]

        for row in range(1, len(table_to_test)):
            current_element = table_to_test[row][FIRST_ELEMENT_INDEX]
            if current_element < previous_element:
                return False
            else:
                previous_element = current_element

        return True


    def test_query_num_students_in_focus_area(self):
        '''
            Tests querying number of students for each focus area
        '''
        num_in_focus = {
            'Algorithms & Theory': 0,
            'Artificial Intelligence': 5,
            'Computer Graphics and Games': 5,
            'Computer Security': 0,
            'Database Systems': 5,
            'Multimedia Information Retrieval': 0,
            'Networking and Distributed Systems': 0,
            'Parallel Computing': 0,
            'Programming Languages': 0,
            'Software Engineering': 0
        }
        num_of_focus_area = len(num_in_focus)

        table_of_focus_area_with_count = \
            model.get_num_students_by_focus_areas()

        assert_equal(
            self.is_table_sorted_by_first_elem(table_of_focus_area_with_count),
            True)
        assert_equal(len(table_of_focus_area_with_count), num_of_focus_area)

        for index_row in range(0, num_of_focus_area):
            current_row = table_of_focus_area_with_count[index_row]
            assert_equal(self.num_column_for_each_focus, len(current_row))
            current_focus_area = current_row[0]
            current_number_of_student = current_row[1]
            assert_equal(num_in_focus.get(current_focus_area),
                         current_number_of_student)
