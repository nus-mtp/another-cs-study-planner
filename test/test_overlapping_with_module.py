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
    URL_NORMAL_GENERAL = '/overlappingWithModule?code=BT5110'
    URL_NORMAL_SPECIFIC = '/overlappingWithModule?code=BT5110&aysem=AY+17%2F18+Sem+1'
    CONTENT_OVERLAPPING_MODULES_TABLE = '<table id="common-module-table" ' +\
                                        'class="table table-bordered table-hover display ' +\
                                        'dataTable">'
    CONTENT_OVERLAPPING_MODULES_TITLE_SPECIFIC = '<h1 class="text-center">Modules'+\
                                                 ' Overlapping with '+\
                                        '<b>BT5110</b> for <b>AY 17/18 Sem 1</b></h1>'
    CONTENT_OVERLAPPING_MODULES_TITLE_GENERAL = '<h1 class="text-center">Modules'+\
                                                ' Overlapping with '+\
                                        '<b>BT5110</b> for <b>All Semesters</b></h1>'
    CONTENT_OVERLAPPING_MODULES_DESCRIPTION_SPECIFIC = '<p class="text-center">'+\
                                                       'Shows all modules taken'+\
                                              ' together with this module at a '+\
                                              'specified semester.</p>'
    CONTENT_OVERLAPPING_MODULES_DESCRIPTION_GENERAL = '<p class="text-center">Shows '+\
                                                      'all modules taken'+\
                                                      ' together with this module in '+\
                                                      'all semesters.</p>'
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

    def test_overlapping_with_module_response_general(self):
        '''
            Tests whether user can access page for overlapping module
        '''
        root = self.test_app.get(self.URL_NORMAL_GENERAL)
        assert_equal(root.status, 200)

    def test_overlapping_with_module_response_specific(self):
        '''
            Tests if user can access page for overlapping with module in ay sem
        '''
        root = self.test_app.get(self.URL_NORMAL_SPECIFIC)
        assert_equal(root.status, 200)

    def test_overlapping_with_module_general_contents(self):
        '''
            Tests if the page contains expected contents when accessing with module
        '''
        root = self.test_app.get(self.URL_NORMAL_GENERAL)

        root.mustcontain(self.CONTENT_OVERLAPPING_MODULES_TABLE)
        root.mustcontain(self.CONTENT_OVERLAPPING_MODULES_TABLE_MODULE)
        root.mustcontain(self.CONTENT_OVERLAPPING_MODULES_TABLE_MODULE_NAME)
        root.mustcontain(self.CONTENT_OVERLAPPING_MODULES_TABLE_AY_SEM)
        root.mustcontain(self.CONTENT_OVERLAPPING_MODULES_TABLE_NUM_STUDENTS)
        root.mustcontain(self.CONTENT_OVERLAPPING_MODULES_TITLE_GENERAL)
        root.mustcontain(self.CONTENT_OVERLAPPING_MODULES_DESCRIPTION_GENERAL)

    def test_overlapping_with_module_specific_contents(self):
        '''
            Tests if the page contains expected contents when accessing module of aysem
        '''
        root = self.test_app.get(self.URL_NORMAL_SPECIFIC)

        root.mustcontain(self.CONTENT_OVERLAPPING_MODULES_TABLE)
        root.mustcontain(self.CONTENT_OVERLAPPING_MODULES_TABLE_MODULE)
        root.mustcontain(self.CONTENT_OVERLAPPING_MODULES_TABLE_MODULE_NAME)
        root.mustcontain(self.CONTENT_OVERLAPPING_MODULES_TABLE_NUM_STUDENTS)
        root.mustcontain(self.CONTENT_OVERLAPPING_MODULES_TITLE_SPECIFIC)
        root.mustcontain(self.CONTENT_OVERLAPPING_MODULES_DESCRIPTION_SPECIFIC)
