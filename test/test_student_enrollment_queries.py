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

        # Add a dummy student
        model.add_student('dummyYr3A', 3)

        # Get current amount of students in each year
        table_of_year_of_study_with_count = \
            model.get_num_students_by_yr_study()

        assert_equal(self.is_table_sorted_by_first_elem(
            table_of_year_of_study_with_count), True)

        # Add more students
        model.add_student('dummyYr1A', 1)
        model.add_student('dummyYr1B', 1)
        model.add_student('dummyYr2A', 2)
        model.delete_student('dummyYr3A')

        expected_difference = [2, 1, -1, 0, 0, 0]

        # Get new amount of students in each year
        new_table_of_year_of_study_with_count = \
            model.get_num_students_by_yr_study()

        # Check if new number of students was gotten
        for row_index in range(len(table_of_year_of_study_with_count)):
            old_year_of_study = table_of_year_of_study_with_count[row_index]
            new_year_of_study = new_table_of_year_of_study_with_count[row_index]

            assert_equal(self.num_column_for_each_year, len(new_year_of_study))

            current_year = new_year_of_study[0]
            current_number_of_student = new_year_of_study[1]
            old_number_of_student = old_year_of_study[1]
            assert_equal(old_number_of_student + expected_difference[current_year - 1],
                         current_number_of_student)

        # Clean up database
        model.delete_student('dummyYr1A')
        model.delete_student('dummyYr1B')
        model.delete_student('dummyYr2A')

    def test_additional_query_num_students_in_year_of_study(self):
        '''
            Additional tests to ensure querying number of students at each year of study
            works for year 5 students as well.
        '''
        # Add a dummy student
        model.add_student('dummyYr3A', 3)

        # Get current amount of students in each year
        table_of_year_of_study_with_count = \
            model.get_num_students_by_yr_study()

        assert_equal(self.is_table_sorted_by_first_elem(
            table_of_year_of_study_with_count), True)

        # Add more students
        model.add_student('dummyYr1A', 1)
        model.add_student('dummyYr1B', 1)
        model.add_student('dummyYr2A', 2)
        model.add_student('dummyYr5A', 5)
        model.delete_student('dummyYr3A')

        expected_difference = [2, 1, -1, 0, 1, 0]

        # Get new amount of students in each year
        new_table_of_year_of_study_with_count = \
            model.get_num_students_by_yr_study()

        # Check if new number of students was gotten
        for row_index in range(len(table_of_year_of_study_with_count)):
            old_year_of_study = table_of_year_of_study_with_count[row_index]
            new_year_of_study = new_table_of_year_of_study_with_count[row_index]

            assert_equal(self.num_column_for_each_year, len(new_year_of_study))

            current_year = new_year_of_study[0]
            current_number_of_student = new_year_of_study[1]
            old_number_of_student = old_year_of_study[1]
            assert_equal(old_number_of_student + expected_difference[current_year - 1],
                         current_number_of_student)

        # Clean up database
        model.delete_student('dummyYr1A')
        model.delete_student('dummyYr1B')
        model.delete_student('dummyYr2A')
        model.delete_student('dummyYr5A')


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
        model.add_student('dummyYr5A', 5)
        model.add_student_focus_area('dummyYr5A', None, None)

        expected_difference = {
            'Have Not Indicated': -1,
            'Algorithms & Theory': 0,
            'Artificial Intelligence': 1,
            'Computer Graphics and Games': 0,
            'Computer Security': 0,
            'Database Systems': 0,
            'Multimedia Information Retrieval': 0,
            'Networking and Distributed Systems': 0,
            'Parallel Computing': 0,
            'Programming Languages': 0,
            'Software Engineering': 0,
            'Interactive Media': 0,
            'Visual Computing': 0
        }
        num_of_focus_area = len(expected_difference)

        old_table_of_focus_area_with_count = \
            model.get_num_students_by_focus_areas()

        # Remove the first row which contains "Have not indicated",
        # then test if the remaining is sorted by focus area
        have_not_indicated_row = old_table_of_focus_area_with_count.pop(0)
        assert_equal(
            self.is_table_sorted_by_first_elem(old_table_of_focus_area_with_count),
            True)
        old_table_of_focus_area_with_count.insert(0, have_not_indicated_row)

        assert_equal(len(old_table_of_focus_area_with_count), num_of_focus_area)

        model.add_student('dummyYr1A', 1)
        model.add_student_focus_area('dummyYr1A', 'Artificial Intelligence', None)
        model.delete_student_focus_area('dummyYr5A')
        model.delete_student('dummyYr5A')

        new_table_of_focus_area_with_count = \
            model.get_num_students_by_focus_areas()

        #Check that get by focus area has gotten the updated values
        for index_row in range(0, num_of_focus_area):
            old_focus_row = old_table_of_focus_area_with_count[index_row]
            new_focus_row = new_table_of_focus_area_with_count[index_row]
            assert_equal(self.num_column_for_each_focus, len(old_focus_row))
            old_focus_area = old_focus_row[0]
            old_number_of_student = old_focus_row[1]
            new_number_of_student = new_focus_row[1]
            assert_equal(expected_difference.get(old_focus_area) + old_number_of_student,
                         new_number_of_student)

        # Clean up database
        model.delete_student_focus_area('dummyYr1A')
        model.delete_student('dummyYr1A')

    def test_query_num_students_in_year_of_study_for_target_module(self):
        '''
            Tests querying number of students for each year of study for a target module
        '''
        test_module_code = "CS1010"
        test_ay_sem_1 = "AY 16/17 Sem 1"

        # Add some students and plans
        model.add_student('dummyYr1A', 1)
        model.add_student('dummyYr1B', 1)
        model.add_student('dummyYr2A', 2)
        model.add_student_plan('dummyYr2A', True, 'CS1010', test_ay_sem_1)

        # Get current count of students taking CS1010
        self.module_view_in_ay_sem_handler.load_focus_areas()
        self.module_view_in_ay_sem_handler.load_student_enrollments(test_module_code, test_ay_sem_1)
        student_year_counts = self.module_view_in_ay_sem_handler.student_year_counts

        # Add and remove some plans
        model.add_student_plan('dummyYr1A', True, 'CS1010', test_ay_sem_1)
        model.add_student_plan('dummyYr1B', True, 'CS1010', test_ay_sem_1)
        model.delete_student_plan('dummyYr2A', 'CS1010', test_ay_sem_1)

        # Get new count of students taking CS1010
        self.module_view_in_ay_sem_handler.load_focus_areas()
        self.module_view_in_ay_sem_handler.load_student_enrollments(test_module_code, test_ay_sem_1)
        new_student_year_counts = self.module_view_in_ay_sem_handler.student_year_counts

        # Check if difference is as expected
        assert_equal(new_student_year_counts[0] - student_year_counts[0], 2)
        assert_equal(new_student_year_counts[1] - student_year_counts[1], -1)
        assert_equal(new_student_year_counts[2] - student_year_counts[2], 0)
        assert_equal(new_student_year_counts[3] - student_year_counts[3], 0)
        assert_equal(new_student_year_counts[4] - student_year_counts[4], 0)
        assert_equal(new_student_year_counts[5] - student_year_counts[5], 0)

        # Clean up database
        model.delete_all_plans_of_student('dummyYr1A')
        model.delete_all_plans_of_student('dummyYr1B')
        model.delete_all_plans_of_student('dummyYr2A')
        model.delete_student('dummyYr1A')
        model.delete_student('dummyYr1B')
        model.delete_student('dummyYr2A')

    def test_query_num_students_in_focus_area_for_target_module(self):
        '''
            Tests querying number of students for each focus area for a target module
        '''
        test_module_code = "CS1010"
        test_ay_sem_1 = "AY 16/17 Sem 1"

        # Add some students with focus areas and plans
        model.add_student('dummyYr1A', 1)
        model.add_student('dummyYr1B', 1)
        model.add_student('dummyYr2A', 2)
        model.add_student_focus_area('dummyYr1A', 'Artificial Intelligence', None)
        model.add_student_focus_area('dummyYr1B', 'Database Systems', 'Algorithms & Theory')
        model.add_student_focus_area('dummyYr2A', 'Algorithms & Theory', None)
        model.add_student_plan('dummyYr1A', True, 'CS1010', test_ay_sem_1)

        # Get current focus count of students taking CS1010
        self.module_view_in_ay_sem_handler.load_focus_areas()
        self.module_view_in_ay_sem_handler.load_student_enrollments(test_module_code, test_ay_sem_1)
        focus_area_counts = self.module_view_in_ay_sem_handler.focus_area_counts

        # Add and remove some plans
        model.add_student_plan('dummyYr1B', True, 'CS1010', test_ay_sem_1)
        model.add_student_plan('dummyYr2A', True, 'CS1010', test_ay_sem_1)
        model.delete_student_plan('dummyYr1A', 'CS1010', test_ay_sem_1)

        # Get new count of students taking CS1010
        self.module_view_in_ay_sem_handler.load_focus_areas()
        self.module_view_in_ay_sem_handler.load_student_enrollments(test_module_code, test_ay_sem_1)
        new_focus_area_counts = self.module_view_in_ay_sem_handler.focus_area_counts

        # Check if difference is as expected
        assert_equal(new_focus_area_counts["Nil"] - focus_area_counts["Nil"], 0)
        assert_equal(new_focus_area_counts["AT"] - focus_area_counts["AT"], 2)
        assert_equal(new_focus_area_counts["AI"] - focus_area_counts["AI"], -1)
        assert_equal(new_focus_area_counts["CGaG"] - focus_area_counts["CGaG"], 0)
        assert_equal(new_focus_area_counts["CS"] - focus_area_counts["CS"], 0)
        assert_equal(new_focus_area_counts["DS"] - focus_area_counts["DS"], 1)
        assert_equal(new_focus_area_counts["MIR"] - focus_area_counts["MIR"], 0)
        assert_equal(new_focus_area_counts["NaDS"] - focus_area_counts["NaDS"], 0)
        assert_equal(new_focus_area_counts["PC"] - focus_area_counts["PC"], 0)
        assert_equal(new_focus_area_counts["PL"] - focus_area_counts["PL"], 0)
        assert_equal(new_focus_area_counts["SE"] - focus_area_counts["SE"], 0)

        # Clean up database
        model.delete_all_plans_of_student('dummyYr1A')
        model.delete_all_plans_of_student('dummyYr1B')
        model.delete_all_plans_of_student('dummyYr2A')
        model.delete_student_focus_area('dummyYr1A')
        model.delete_student_focus_area('dummyYr1B')
        model.delete_student_focus_area('dummyYr2A')
        model.delete_student('dummyYr1A')
        model.delete_student('dummyYr1B')
        model.delete_student('dummyYr2A')
