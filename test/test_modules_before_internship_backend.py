'''
test_modules_before_internship.py
Contains test cases for modules taken before internship query related functions.
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
        This class runs the test cases for modules taken before internship
        query related functions.
    '''
    def __init__(self):
        self.INTERN_MOD = 'CP3200'
        self.INTERN_SEM = 'AY 17/18 Sem 1'

    def test_query_module_before_internship_empty(self):
        '''
            Tests querying the list of modules taken before internship,
            in AY/Sem which no one is doing internship in.
        '''
        list_of_modules_before_internship = model.get_mod_before_intern('AY 16/17 Sem 1')
        # List is empty as we do not have data before 16/17 Sem 1
        required_list = []

        assert_equal(len(list_of_modules_before_internship), len(required_list))
        assert_equal(sorted(list_of_modules_before_internship), sorted(required_list))


    def test_query_module_before_internship(self):
        '''
            Tests querying the list of modules taken before internship,
            in AY/Sem with people doing internship in.
        '''
        # Add some modules and dummy students
        required_dummy = ('AAA1111', 'Dummy for Intern', 1)
        model.add_student('dummyYr1A', 1)
        model.add_module('AAA1111', 'Dummy for Intern', 'Description', 4, 'Active')
        model.add_student_plan('dummyYr1A', True, 'AAA1111', 'AY 16/17 Sem 2')
        model.add_student_plan('dummyYr1A', True, self.INTERN_MOD, self.INTERN_SEM)

        # Get list of modules taken before internship
        list_of_modules_before_internship = model.get_mod_before_intern(self.INTERN_SEM)

        assert required_dummy in list_of_modules_before_internship

        # Clean up database
        model.delete_all_plans_of_student('dummyYr1A')
        model.delete_module('AAA1111')
        model.delete_student('dummyYr1A')

        # Test that required dummy no longer in list
        list_of_modules_before_internship = model.get_mod_before_intern(self.INTERN_SEM)

        assert required_dummy not in list_of_modules_before_internship


    def test_query_module_before_internship_with_mod_after_internship(self):
        '''
            Tests querying the list of modules taken before internship,
            in AY/Sem with people doing internship in, and
            with some modules taken after or during aysem of internship
        '''
        # Get list of modules before internship
        list_of_modules_before_internship = model.get_mod_before_intern(self.INTERN_SEM)

        # Add some dummy students and plans. They should not affect the list
        model.add_student('dummyYr1A', 1)
        model.add_module('AAA1111', 'Dummy with Intern', 'Description', 4, 'Active')
        model.add_module('AAA1112', 'Dummy after Intern', 'Description', 4, 'Active')
        model.add_student_plan('dummyYr1A', True, 'AAA1111', self.INTERN_SEM)
        model.add_student_plan('dummyYr1A', True, self.INTERN_MOD, self.INTERN_SEM)
        model.add_student_plan('dummyYr1A', True, 'AAA1112', 'AY 17/18 Sem 2')

        # Get new list of modules before internship. It should remain unchanged.
        new_list_of_modules_before_internship = model.get_mod_before_intern(self.INTERN_SEM)

        assert_equal(len(list_of_modules_before_internship),
                     len(new_list_of_modules_before_internship))
        assert_equal(sorted(list_of_modules_before_internship),
                     sorted(new_list_of_modules_before_internship))

        # Clean up database
        model.delete_all_plans_of_student('dummyYr1A')
        model.delete_module('AAA1111')
        model.delete_module('AAA1112')
        model.delete_student('dummyYr1A')
