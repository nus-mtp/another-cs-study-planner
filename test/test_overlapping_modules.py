'''
    contains test cases for overlapping_modules.py
    How this works:
    #1 check that page can be accessed throught URL
    #2 check that page contents are what is expected with example
    #2 check that components found on page are same as expected when
        using form to search for a certain mod.
'''
from nose.tools import assert_equal
from paste.fixture import TestApp
from app import APP, SESSION

class TestCode(object):
    '''
        this class runs the tests cases for overlapping_modules.py
    '''

    URL_ALL = '/overlappingModules'
    URL_EXCEPTION_HANDLE = '/overlappingModules'

    TABLE_COLUMN_MODULE_1 = '<th>Module 1</th>'
    TABLE_COLUMN_MODULE_1_NAME = '<th>Name of Module 1</th>'
    TABLE_COLUMN_MODULE_2 = '<th data-sortable="false">Module 2</th>'
    TABLE_COLUMN_MODULE_2_NAME = '<th>Name of Module 2</th>'
    TABLE_COLUMN_AY_SEM = '<th>For AY-Sem</th>'
    TABLE_COLUMN_NUM_STUDENTS = '<th>Number of Students</th>'


    def __init__(self):
        self.middleware = None
        self.test_app = None


    def setUp(self):
        '''
            Sets up the 'app.py' fixture
        '''
        SESSION['id'] = 2
        self.middleware = []
        self.test_app = TestApp(APP.wsgifunc(*self.middleware))


    def test_page_access(self):
        '''
            tests if the page can be accessed
        '''
        page = self.test_app.get(self.URL_ALL)
        assert_equal(page.status, 200)

        page = self.test_app.get(self.URL_EXCEPTION_HANDLE)
        assert_equal(page.status, 200)


    def test_page_contents(self):
        '''
            tests if expected contents are present in the page
        '''
        page = self.test_app.get(self.URL_ALL)
        page.mustcontain(self.TABLE_COLUMN_MODULE_1)
        page.mustcontain(self.TABLE_COLUMN_MODULE_1_NAME)
        page.mustcontain(self.TABLE_COLUMN_MODULE_2)
        page.mustcontain(self.TABLE_COLUMN_MODULE_2_NAME)
        page.mustcontain(self.TABLE_COLUMN_AY_SEM)
        page.mustcontain(self.TABLE_COLUMN_NUM_STUDENTS)
