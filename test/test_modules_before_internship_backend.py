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
        self.TEST_MOD_1 = 'CS6101'
        self.TEST_MOD_2 = 'CP3200'
        self.TEST_MOD_3 = 'CS3230'
        self.TEST_MOD_4 = 'CS2105'
        self.isDuringTesting = False # a boolean flag to allow functions to be called by
                                     # other functions only, and not by nosetests


    def test_query_module_before_internship_empty(self):
        '''
            Tests querying the list of modules taken before internship,
            in AY/Sem which no one is doing internship in.
        '''
        list_of_modules_before_internship = model.get_mod_before_intern('AY 16/17 Sem 1')
        required_list = []

        assert_equal(len(list_of_modules_before_internship), len(required_list))
        assert_equal(sorted(list_of_modules_before_internship), sorted(required_list))

        list_of_modules_before_internship = model.get_mod_before_intern('AY 16/17 Sem 2')
        required_list = []

        assert_equal(len(list_of_modules_before_internship), len(required_list))
        assert_equal(sorted(list_of_modules_before_internship), sorted(required_list))


    def test_query_module_before_internship(self):
        '''
            Tests querying the list of modules taken before internship,
            in AY/Sem with people doing internship in.
        '''
        list_of_modules_before_internship = model.get_mod_before_intern('AY 17/18 Sem 1')
        required_list = [('CS1020', 'Data Structures and Algorithms I', 2),
                         ('CS1010', 'Programming Methodology', 2),
                         ('CS1231', 'Discrete Structures', 2),
                         ('CS2105', 'Introduction to Computer Networks', 2),
                         ('CS3230', 'Design and Analysis of Algorithms', 1),
                         ('CS2010', 'Data Structures and Algorithms II', 1),
                         ('CS4221', 'Database Applications Design and Tuning', 1),
                         ('CS4224', 'Distributed Databases', 1)
                        ]

        assert_equal(len(list_of_modules_before_internship), len(required_list))
        assert_equal(sorted(list_of_modules_before_internship), sorted(required_list))

        list_of_modules_before_internship = model.get_mod_before_intern('AY 17/18 Sem 2')
        required_list = [('CS3247', 'Game Development', 1),
                         ('CS4350', 'Game Development Project', 1),
                         ('CS3223', 'Database Systems Implementation', 1),
                         ('CS2102', 'Database Systems', 1)
                        ]

        assert_equal(len(list_of_modules_before_internship), len(required_list))
        assert_equal(sorted(list_of_modules_before_internship), sorted(required_list))


    def test_query_module_before_internship_with_mod_after_internship(self):
        '''
            Tests querying the list of modules taken before internship,
            in AY/Sem with people doing internship in, and
            with some modules taken after or during aysem of internship
        '''
        self.isDuringTesting = True
        self.populate_dummy_data_for_test_mod_before_intern()

        list_of_modules_before_internship = model.get_mod_before_intern('AY 17/18 Sem 1')
        required_list = [('CS1020', 'Data Structures and Algorithms I', 2),
                         ('CS1010', 'Programming Methodology', 2),
                         ('CS1231', 'Discrete Structures', 2),
                         ('CS2105', 'Introduction to Computer Networks', 3),
                         ('CS3230', 'Design and Analysis of Algorithms', 1),
                         ('CS2010', 'Data Structures and Algorithms II', 1),
                         ('CS4221', 'Database Applications Design and Tuning', 1),
                         ('CS4224', 'Distributed Databases', 1)
                        ]

        assert_equal(len(list_of_modules_before_internship), len(required_list))
        assert_equal(sorted(list_of_modules_before_internship), sorted(required_list))

        self.isDuringTesting = True
        self.clean_up_dummy_data_for_test_mod_before_intern()


    def populate_dummy_data_for_test_mod_before_intern(self):
        '''
            Populates some dummy data for more testing
        '''
        if self.isDuringTesting:
            sql_command = "INSERT INTO student VALUES('D9818873B', 1)"
            model.DB_CURSOR.execute(sql_command)
            sql_command = "INSERT INTO studentplans VALUES('D9818873B', " + \
            "false, '" + self.TEST_MOD_1 + "', 'AY 17/18 Sem 1')"
            model.DB_CURSOR.execute(sql_command)
            sql_command = "INSERT INTO studentplans VALUES('D9818873B', " + \
            "false, '" + self.TEST_MOD_2 + "', 'AY 17/18 Sem 1')"
            model.DB_CURSOR.execute(sql_command)
            sql_command = "INSERT INTO studentplans VALUES('D9818873B', " + \
            "false, '" + self.TEST_MOD_3 + "', 'AY 17/18 Sem 2')"
            model.DB_CURSOR.execute(sql_command)
            sql_command = "INSERT INTO studentplans VALUES('D9818873B', " + \
            "false, '" + self.TEST_MOD_4 + "', 'AY 16/17 Sem 1')"
            model.DB_CURSOR.execute(sql_command)

            self.isDuringTesting = False


    def clean_up_dummy_data_for_test_mod_before_intern(self):
        '''
            Clean up dummy data for testing
        '''
        if self.isDuringTesting:
            sql_command = "DELETE FROM studentplans WHERE studentid='D9818873B'"
            model.DB_CURSOR.execute(sql_command)
            sql_command = "DELETE FROM student WHERE nusnetid='D9818873B'"
            model.DB_CURSOR.execute(sql_command)

            self.isDuringTesting = False
