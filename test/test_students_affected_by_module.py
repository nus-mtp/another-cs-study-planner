'''
    test_students_affected_by_module.py
'''

from paste.fixture import TestApp
from nose.tools import assert_equal
from app import APP, SESSION

class TestCode(object):
    '''
        This class runs test cases for studentsAffectedByModule.py
    '''

    URL_NORMAL = '/studentsAffectedByModule?code=IT1005&aysem=AY+17%2F18+Sem+1'
    CONTENT_TITLE = 'Students Affected By Module Changes'
    CONTENT_SUBTITLE = 'For <b>IT1005</b> in <b>AY 17/18 Sem 1</b>'


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



    def test_response(self):
        '''
            tests if the page is accessable
        '''
        root = self.test_app.get(self.URL_NORMAL)
        assert_equal(root.status, 200)

    def test_title(self):
        '''
            tests if the title and sub title are correct
        '''
        root = self.test_app.get(self.URL_NORMAL)
        root.mustcontain(self.CONTENT_TITLE)
        root.mustcontain(self.CONTENT_SUBTITLE)
