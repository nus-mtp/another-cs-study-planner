'''
    test_delete_module.py test the page view of Delete Module
'''
from paste.fixture import TestApp
from nose.tools import assert_equal
from app import APP
from components import model
from components import session


class TestCode(object):
    '''
        This class runs the test cases to test Delete Module page
    '''
    TABLE_HEADER_CODE = '<th>Code</th>'
    TABLE_HEADER_NAME = '<th>Name</th>'
    TABLE_HEADER_DESCRIPTION = '<th>Description</th>'
    TABLE_HEADER_MC = '<th>MCs</th>'
    TABLE_HEADER_DELETE = '<th data-sortable="false">Delete</th>'

    DUMMY_MODULE_CODE = "DD1001"
    DUMMY_MODULE_NAME = "Dummy Module 1"

    global_var = None

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

        model.add_module(self.DUMMY_MODULE_CODE, self.DUMMY_MODULE_NAME, self.DUMMY_MODULE_NAME, 1, "New")


    def tearDown(self):
        '''
            Tears down 'app.py' fixture and logs out
        '''
        session.tear_down(self.test_app)

        model.delete_module(self.DUMMY_MODULE_CODE)


    def test_valid_response(self):
        '''
            Tests if user can access the index page without request errors.
        '''
        root = self.test_app.get('/deleteModule')

        # checks if HTTP response code is 200 (= OK)
        assert_equal(root.status, 200)


    def test_delete_module_table(self):
        '''
            Tests if a table displaying a list of deletable modules exist
        '''
        root = self.test_app.get('/deleteModule')

        # Checks the existence of the handler for viewing fixed mounting plan
        root.mustcontain(self.TABLE_HEADER_CODE)
        root.mustcontain(self.TABLE_HEADER_NAME)
        root.mustcontain(self.TABLE_HEADER_DESCRIPTION)
        root.mustcontain(self.TABLE_HEADER_MC)
        root.mustcontain(self.TABLE_HEADER_DELETE)


    def test_new_module(self):
        '''
            Tests if the Delete Module table contains a new module
        '''
        root = self.test_app.get('/deleteModule')

        root.mustcontain(self.DUMMY_MODULE_CODE)
        root.mustcontain(self.DUMMY_MODULE_NAME)

        



