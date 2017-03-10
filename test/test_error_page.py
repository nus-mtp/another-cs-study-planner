'''
    this page tests accessability and components of the error page
'''
from paste.fixture import TestApp
from nose.tools import assert_equal
from app import APP, SESSION
import web

class TestCode(object):
    '''
        This classes tests the accessability and components of the error page
    '''

    URL_NORMAL = '/errorPage?error=testerror'
    URL_EXCEPTION_TRIGGER = '/errorPage'
    ELEMENT_ERROR = 'testerror'
    ELEMENT_HEADER = '<h1>Error Occured:</h1>'
    ELEMENT_ERROR_MSG = '<h2>testerror</h2>'
    ELEMENT_EXCEPTION_MSG = '<h2>AttributeError: no error message supplied.</h2>'

    def __init__(self):
        self.middleware = None
        self.test_app = None


    def setUp(self):
        '''
            Sets up the 'app.py' fixture
        '''
        self.middleware = []
        self.test_app = TestApp(APP.wsgifunc(*self.middleware))
        # Sets up the simulated 'login' state
        SESSION['id'] = web.ACCOUNT_LOGIN_SUCCESSFUL


    def test_error_page_access(self):
        '''
            check if error page is accessable
        '''
        root = self.test_app.get(self.URL_NORMAL)
        assert_equal(root.status, 200)

    def test_valid_access_content(self):
        '''
            check if error page contains correct content
        '''
        root = self.test_app.get(self.URL_NORMAL)
        assert_equal(root.status, 200)
        root.mustcontain(self.ELEMENT_HEADER)
        root.mustcontain(self.ELEMENT_ERROR_MSG)

    def test_invalid_access_content(self):
        '''
            tests if error page can handle exception of when no error message is inputed.
        '''
        root = self.test_app.get(self.URL_EXCEPTION_TRIGGER)
        assert_equal(root.status, 200)
        root.mustcontain(self.ELEMENT_HEADER)
        root.mustcontain(self.ELEMENT_EXCEPTION_MSG)
