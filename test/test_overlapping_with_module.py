'''
    tests if the individual module overlapping table contains what is should
'''

from paste.fixture import TestApp
from nose.tools import assert_equal
from app import APP
from components import session

class TestCode(object):
    '''
        tests if the individual module overlapping table contains what is should
    '''
    URL_NORMAL = '/overlappingWithModule?code=BT5110'
    CONTENT_OVERLAPPING_MODULES_TABLE = '<table id="common-module-table" ' +\
                                        'class="table table-bordered table-hover display ' +\
                                        'dataTable">'
    CONTENT_OVERLAPPING_MODULES_TABLE_MODULE = '<th>Module Code</th>'
    CONTENT_OVERLAPPING_MODULES_TABLE_MODULE_NAME = '<th>Module Name</th>'
    CONTENT_OVERLAPPING_MODULES_TABLE_AY_SEM = '<th>For AY-Sem</th>'
    CONTENT_OVERLAPPING_MODULES_TABLE_NUM_STUDENTS = '<th>Number of Students</th>'

    def __init__(self):
        self.middleware = None
        self.test_app = None


    def setUp(self):
        '''
            Sets up the 'app.py' fixture
        '''
        self.middleware = []
        self.test_app = TestApp(APP.wsgifunc(*self.middleware))
        session.set_up(self.test_app)


    def tearDown(self):
        '''
            Tears down 'app.py' fixture and logs out
        '''
        session.tear_down(self.test_app)

    def test_overlapping_with_module_response(self):
        '''
            Tests whether user can access page for overlapping module
        '''
        root = self.test_app.get(self.URL_NORMAL)
        assert_equal(root.status, 200)

    def test_overlapping_with_module_contents(self):
        '''
            Tests if the page contains expected contents
        '''
        root = self.test_app.get(self.URL_NORMAL)

        root.mustcontain(self.CONTENT_OVERLAPPING_MODULES_TABLE)
        root.mustcontain(self.CONTENT_OVERLAPPING_MODULES_TABLE_MODULE)
        root.mustcontain(self.CONTENT_OVERLAPPING_MODULES_TABLE_MODULE_NAME)
        root.mustcontain(self.CONTENT_OVERLAPPING_MODULES_TABLE_AY_SEM)
        root.mustcontain(self.CONTENT_OVERLAPPING_MODULES_TABLE_NUM_STUDENTS)
