'''
test_student_enrollment_queries.py
Contains test cases for student enrollment query functions.
'''
from nose.tools import assert_equal
from components import model
from components.handlers.module_view_in_ay_sem import IndividualModule

# HOW TO RUN NOSE TESTS
# 1. Make sure you are in cs-modify main directory
# 2. Make sure the path "C:\Python27\Scripts" is added in your environment variables
# 3. Enter in cmd: "nosetests test/"
# 4. Nose will run all the tests inside the test/ folder

class TestCode(object):
    '''
        This class runs the test cases for student enrollment query functions.
    '''
    def __init__(self):
        self.num_column_for_each_year = 2
        self.num_column_for_each_focus = 2
        self.module_view_in_ay_sem_handler = IndividualModule()



    def test_query_num_students_in_year_of_study(self):
        '''
            Tests querying number of students at each year of study
        '''
        num_in_year = [6, 5, 4, 3, 0, 0]

        table_of_year_of_study_with_count = \
            model.get_num_students_by_yr_study()

        assert_equal(self.is_table_sorted_by_first_elem(
            table_of_year_of_study_with_count), True)

        num_of_rows_expected = 4
        for index_row in range(0, num_of_rows_expected):
            current_row = table_of_year_of_study_with_count[index_row]
            assert_equal(self.num_column_for_each_year, len(current_row))
            current_year = current_row[0]
            current_number_of_student = current_row[1]
            assert_equal(num_in_year[current_year - 1], current_number_of_student)


    def test_additional_query_num_students_in_year_of_study(self):
        '''
            Additional tests to ensure querying number of students at each year of study
            works for year 5 students as well.
        '''
        # Inject year 5 student temporarily
        model.add_student('D9818872A', 5)

        num_in_year = [6, 5, 4, 3, 1, 0]

        table_of_year_of_study_with_count = \
            model.get_num_students_by_yr_study()

        assert_equal(self.is_table_sorted_by_first_elem(
            table_of_year_of_study_with_count), True)

        num_of_rows_expected = 5
        for index_row in range(0, num_of_rows_expected):
            current_row = table_of_year_of_study_with_count[index_row]
            assert_equal(self.num_column_for_each_year, len(current_row))
            current_year = current_row[0]
            current_number_of_student = current_row[1]
            assert_equal(num_in_year[current_year - 1], current_number_of_student)

        # Clean up the database
        model.delete_student('D9818872A')


    def is_table_sorted_by_first_elem(self, table_to_test):
        '''
            Helper function to tests if the rows in table_to_test
            is sorted in ascending order
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
        # Inject year 5 student temporarily with no focus area
        model.add_student('D9818872A', 5)
        model.add_student_focus_area('D9818872A', None, None)

        num_in_focus = {
            'Have Not Indicated': 1,
            'Algorithms & Theory': 0,
            'Artificial Intelligence': 5,
            'Computer Graphics and Games': 5,
            'Computer Security': 0,
            'Database Systems': 5,
            'Multimedia Information Retrieval': 0,
            'Networking and Distributed Systems': 0,
            'Parallel Computing': 0,
            'Programming Languages': 0,
            'Software Engineering': 5,
            'Interactive Media': 0,
            'Visual Computing': 0
        }
        num_of_focus_area = len(num_in_focus)

        table_of_focus_area_with_count = \
            model.get_num_students_by_focus_areas()

        # Remove the first row which contains "Have not indicated",
        # then test if the remaining is sorted by focus area
        have_not_indicated_row = table_of_focus_area_with_count.pop(0)
        assert_equal(
            self.is_table_sorted_by_first_elem(table_of_focus_area_with_count),
            True)
        table_of_focus_area_with_count.insert(0, have_not_indicated_row)

        assert_equal(len(table_of_focus_area_with_count), num_of_focus_area)

        for index_row in range(0, num_of_focus_area):
            current_row = table_of_focus_area_with_count[index_row]
            assert_equal(self.num_column_for_each_focus, len(current_row))
            current_focus_area = current_row[0]
            current_number_of_student = current_row[1]
            assert_equal(num_in_focus.get(current_focus_area),
                         current_number_of_student)

        # Clean up the database
        model.delete_student_focus_area('D9818872A')
        model.delete_student('D9818872A')


    def test_query_num_students_in_year_of_study_for_target_module(self):
        '''
            Tests querying number of students for each year of study for a target module
        '''
        test_module_code = "CS1010"
        test_ay_sem_1 = "AY 16/17 Sem 1"
        test_ay_sem_2 = "AY 16/17 Sem 2"

        self.module_view_in_ay_sem_handler.load_focus_areas()
        self.module_view_in_ay_sem_handler.load_student_enrollments(test_module_code, test_ay_sem_1)
        student_year_counts = self.module_view_in_ay_sem_handler.student_year_counts
        assert_equal(student_year_counts[0], 4)
        assert_equal(student_year_counts[1], 1)
        assert_equal(student_year_counts[2], 0)
        assert_equal(student_year_counts[3], 0)
        assert_equal(student_year_counts[4], 0)
        assert_equal(student_year_counts[5], 0)

        self.module_view_in_ay_sem_handler.load_focus_areas()
        self.module_view_in_ay_sem_handler.load_student_enrollments(test_module_code, test_ay_sem_2)
        student_year_counts = self.module_view_in_ay_sem_handler.student_year_counts
        assert_equal(student_year_counts[0], 1)
        assert_equal(student_year_counts[1], 0)
        assert_equal(student_year_counts[2], 1)
        assert_equal(student_year_counts[3], 0)
        assert_equal(student_year_counts[4], 0)
        assert_equal(student_year_counts[5], 0)


    def test_query_num_students_in_focus_area_for_target_module(self):
        '''
            Tests querying number of students for each focus area for a target module
        '''
        test_module_code = "CS1010"
        test_ay_sem_1 = "AY 16/17 Sem 1"
        test_ay_sem_2 = "AY 16/17 Sem 2"

        self.module_view_in_ay_sem_handler.load_focus_areas()
        self.module_view_in_ay_sem_handler.load_student_enrollments(test_module_code, test_ay_sem_1)
        focus_area_counts = self.module_view_in_ay_sem_handler.focus_area_counts
        assert_equal(focus_area_counts["Nil"], 0)
        assert_equal(focus_area_counts["AT"], 0)
        assert_equal(focus_area_counts["AI"], 1)
        assert_equal(focus_area_counts["CGaG"], 1)
        assert_equal(focus_area_counts["CS"], 0)
        assert_equal(focus_area_counts["DS"], 1)
        assert_equal(focus_area_counts["MIR"], 0)
        assert_equal(focus_area_counts["NaDS"], 0)
        assert_equal(focus_area_counts["PC"], 0)
        assert_equal(focus_area_counts["PL"], 0)
        assert_equal(focus_area_counts["SE"], 2)

        self.module_view_in_ay_sem_handler.load_focus_areas()
        self.module_view_in_ay_sem_handler.load_student_enrollments(test_module_code, test_ay_sem_2)
        focus_area_counts = self.module_view_in_ay_sem_handler.focus_area_counts
        assert_equal(focus_area_counts["Nil"], 1)
        assert_equal(focus_area_counts["AT"], 0)
        assert_equal(focus_area_counts["AI"], 0)
        assert_equal(focus_area_counts["CGaG"], 0)
        assert_equal(focus_area_counts["CS"], 0)
        assert_equal(focus_area_counts["DS"], 0)
        assert_equal(focus_area_counts["MIR"], 0)
        assert_equal(focus_area_counts["NaDS"], 0)
        assert_equal(focus_area_counts["PC"], 0)
        assert_equal(focus_area_counts["PL"], 0)
        assert_equal(focus_area_counts["SE"], 1)
