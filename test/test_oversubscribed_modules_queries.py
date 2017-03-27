'''
test_oversubscribed_modules_queries.py
Contains test cases for oversubscribed modules query related functions.
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
        This class runs the test cases for oversubscribed modules
        query related functions.
    '''
    def __init__(self):
        pass


    def test_query_oversubscribed_modules(self):
        '''
            Tests querying the list of oversubscribed modules.

            Note to developers: Please check that you have repopulated
            your database if this test fails.
        '''
        # No modules in future sem are currently oversubscribed, thus we need to
        # inject data to database to test.
        model.add_student('D9818873B', 1)
        model.add_student_plan('D9818873B', False, 'CS6101', 'AY 17/18 Sem 1')

        list_of_oversub_mod = model.get_oversub_mod()
        required_list = [('CS3230', 'Design and Analysis of Algorithms', 'AY 16/17 Sem 2', '?', 3),
                         ('CS4244', 'Knowledge-Based Systems', 'AY 16/17 Sem 2', '?', 1),
                         ('CS3242', '3D Modelling and Animation', 'AY 16/17 Sem 2', '?', 1),
                         ('CS3243', 'Introduction to Artificial Intelligence',
                          'AY 16/17 Sem 2', '?', 1),
                         ('CS3247', 'Game Development', 'AY 16/17 Sem 2', '?', 1),
                         ('CS4221', 'Database Applications Design and Tuning',
                          'AY 16/17 Sem 2', '?', 1),
                         ('CS3223', 'Database Systems Implementation', 'AY 16/17 Sem 2', '?', 1),
                         ('CS6101', 'Exploration of Computer Science Research',
                          'AY 17/18 Sem 1', 0, 1),
                         ('CP3200', 'Internship', 'AY 17/18 Sem 1', '?', 3),
                         ('CP3200', 'Internship', 'AY 17/18 Sem 2', '?', 1),
                         ('CP3880', 'Advanced Technology Attachment Programme',
                          'AY 17/18 Sem 1', '?', 1),
                         ('CP3880', 'Advanced Technology Attachment Programme',
                          'AY 17/18 Sem 2', '?', 1)
                        ]

        assert_equal(len(list_of_oversub_mod), len(required_list))
        assert_equal(sorted(list_of_oversub_mod), sorted(required_list))

        # Clean up the database
        model.delete_all_plans_of_student('D9818873B')
        model.delete_student('D9818873B')
        