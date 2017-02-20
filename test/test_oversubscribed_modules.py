'''
    test_oversubscribed_modules.py tests the page views and navigations for
    viewing oversubscribed modules (modules with demand > quota).

    Firstly, we specify a target URL for conducting UI testing.

    Then, we proceed to test the following things:
    #1 Accessing the target page should be possible (i.e. response code should be 200 OK).
    #2 The necessary HTML elements are contained in the page view for target page.
    #3 Navigating to other valid pages from the target page should be successful.

    For #3, we do not check the full correctness of the UI for the other pages, as this
    will be handled by its corresponding test cases.
'''


from paste.fixture import TestApp
from nose.tools import assert_equal
from app import APP, SESSION


class TestCode(object):
    '''
        This class contains methods that tests the page views and navigations inside
        the target page.
    '''


    URL_STUDENT_ENROLLMENT = '/oversubscribedModules'

    TABLE_HEADER_MODULE_CODE = '<th>Code</th>'
    TABLE_HEADER_MODULE_AY_SEM = '<th>AY-Semester</th>'
    TABLE_HEADER_MODULE_QUOTA = '<th>Class Quota</th>'
    TABLE_HEADER_MODULE_DEMAND = '<th>Student Demand</th>'


    def __init__(self):
        self.middleware = None
        self.test_app = None


    def  setUp(self):
        '''
            Sets up the 'app.py' fixture
        '''
        SESSION['id'] = 2
        self.middleware = []
        self.test_app = TestApp(APP.wsgifunc(*self.middleware))


    def test_oversubscribed_modules_valid_response(self):
        '''
            Tests whether user can access page for showing student
            enrollment without request errors.
        '''
        root = self.test_app.get(self.URL_STUDENT_ENROLLMENT)

        assert_equal(root.status, 200)


    def test_oversubscribed_modules_contents(self):
        '''
            Tests if the student enrollment page contains
            the necessary views.
        '''
        root = self.test_app.get(self.URL_STUDENT_ENROLLMENT)

        root.mustcontain(self.TABLE_HEADER_MODULE_CODE)
        root.mustcontain(self.TABLE_HEADER_MODULE_AY_SEM)
        root.mustcontain(self.TABLE_HEADER_MODULE_QUOTA)
        root.mustcontain(self.TABLE_HEADER_MODULE_DEMAND)
