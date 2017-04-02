'''
    test_students_affected_by_module.py
'''

from paste.fixture import TestApp
from nose.tools import assert_equal
from app import APP
from components import session


class TestCode(object):
    '''
        This class runs test cases for studentsAffectedByModule.py
    '''

    URL_NORMAL = '/studentsAffectedByModule?code=IT1005&aysem=AY+17%2F18+Sem+1'
    CONTENT_TITLE = '<h1 class="text-center">Students Taking This Module</h1>'
    CONTENT_DESCRIPTION = '<p class="text-center">Show students who <b>have taken</b>, '+\
                          'are <b>currently taking</b>, or are <b>planning to take</b> this module.</p>'
    CONTENT_SUBTITLE = 'For <b>IT1005</b> in <b>AY 17/18 Sem 1</b>'


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
        root.mustcontain(self.CONTENT_DESCRIPTION)
