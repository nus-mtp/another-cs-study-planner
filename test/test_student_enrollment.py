'''
    test_student_enrollment.py tests the page views and navigations for
    viewing student enrollment information.

    Firstly, we specify a target URL for conducting UI testing.

    Then, we proceed to test the following things:
    #1 Accessing the target page should be possible (i.e. response code should be 200 OK).
    #2 The necessary HTML elements are contained in the page view for target page.
    #3 Navigating to other valid pages from the target page should be successful.

    For #3, we do not check the full correctness of the UI for the other pages, as this
    will be handled by its corresponding test cases.
'''


from paste.fixture import TestApp
from nose.tools import assert_equal, raises
from app import APP


class TestCode(object):
    '''
        This class contains methods that tests the page views and navigations inside
        the target page.
    '''

    URL_STUDENT_ENROLLMENT = '/studentEnrollment'

    TABLE_HEADER_SENIORITY = '<th>Year of Study</th>'
    TABLE_HEADER_FOCUS_AREA = '<th>Focus Area</th>'
    TABLE_HEADER_STUDENT_COUNT = '<th>Number of Students</th>'

    TABLE_FOCUS_AREAS = [
        'Have Not Indicated',
        'Algorithms &amp; Theory',
        'Artificial Intelligence',
        'Computer Graphics and Games',
        'Database Systems',
        'Multimedia Information Retrieval',
        'Networking and Distributed Systems',
        'Parallel Computing',
        'Programming Languages',
        'Software Engineering'
    ]

    TABLE_YEARS_OF_STUDY = [
        '<td>1</td>',
        '<td>2</td>',
        '<td>3</td>',
        '<td>4</td>'
    ]


    def __init__(self):
        self.middleware = None
        self.test_app = None


    def setUp(self):
        '''
            Sets up the 'app.py' fixture
        '''
        self.middleware = []
        self.test_app = TestApp(APP.wsgifunc(*self.middleware))


    def test_student_enrollment_valid_response(self):
        '''
            Tests whether user can access page for showing student
            enrollment without request errors.
        ''' 
        root = self.test_app.get(self.URL_STUDENT_ENROLLMENT)

        assert_equal(root.status, 200)


    def test_student_enrollment_contents(self):
        '''
            Tests if the student enrollment page contains
            the necessary views.
        '''
        root = self.test_app.get(self.URL_STUDENT_ENROLLMENT)

        root.mustcontain(self.TABLE_HEADER_SENIORITY)
        root.mustcontain(self.TABLE_HEADER_FOCUS_AREA)
        root.mustcontain(self.TABLE_HEADER_STUDENT_COUNT)


    def test_student_enrollment_focus_area_table_contents(self):
        '''
            Tests if the focus area table contains the correct
            listing of all focus areas, inclusive of those who
            have not indicated any focus areas.
        '''
        root = self.test_app.get(self.URL_STUDENT_ENROLLMENT)

        root.mustcontain(self.TABLE_FOCUS_AREAS[0],
                         self.TABLE_FOCUS_AREAS[1],
                         self.TABLE_FOCUS_AREAS[2],
                         self.TABLE_FOCUS_AREAS[3],
                         self.TABLE_FOCUS_AREAS[4],
                         self.TABLE_FOCUS_AREAS[5],
                         self.TABLE_FOCUS_AREAS[6],
                         self.TABLE_FOCUS_AREAS[7],
                         self.TABLE_FOCUS_AREAS[8],
                         self.TABLE_FOCUS_AREAS[9])


    def test_student_enrollment_student_year_table_contents(self):
        '''
            Tests if the student year-of-study table contains the
            correct listing of all possible student years.

            Currently assumes that the most senior student is up
            to year 4 of study.
        '''
        root = self.test_app.get(self.URL_STUDENT_ENROLLMENT)

        root.mustcontain(self.TABLE_YEARS_OF_STUDY[0],
                         self.TABLE_YEARS_OF_STUDY[1],
                         self.TABLE_YEARS_OF_STUDY[2],
                         self.TABLE_YEARS_OF_STUDY[3])