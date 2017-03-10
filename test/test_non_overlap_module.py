'''
    test_non_overlap_module.py tests the page views for
    viewing module pairs which no one takes together

    Firstly, we specify a target URL for conducting UI testing.

    Then, we proceed to test the following things:
    #1 Accessing the target page should be possible (i.e. response code should be 200 OK).
    #2 The necessary HTML elements are contained in the page view for target page.

'''


from paste.fixture import TestApp
from nose.tools import assert_equal
from app import APP, SESSION


class TestCode(object):
    '''
        This class contains methods that tests the page views inside
        the target page.
    '''


    URL_NON_OVERLAP_MODS = '/nonOverlappingModules'

    TABLE_HEADER_MODULE_CODE_ONE = '<th>Module Code 1</th>'
    TABLE_HEADER_MODULE_CODE_TWO = '<th>Module Code 2</th>'
    TABLE_HEADER_MODULE_AY_SEM = '<th>AY-Semester</th>'


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


    def test_non_overlapping_modules_valid_response(self):
        '''
            Tests whether user can access page for showing non
            overlapping modules without request errors.
        '''
        root = self.test_app.get(self.URL_NON_OVERLAP_MODS)

        assert_equal(root.status, 200)


    def test_non_overlapping_modules_contents(self):
        '''
            Tests if the non-overlapping modules page contains
            the necessary views.
        '''
        root = self.test_app.get(self.URL_NON_OVERLAP_MODS)

        root.mustcontain(self.TABLE_HEADER_MODULE_CODE_ONE)
        root.mustcontain(self.TABLE_HEADER_MODULE_CODE_TWO)
        root.mustcontain(self.TABLE_HEADER_MODULE_AY_SEM)
