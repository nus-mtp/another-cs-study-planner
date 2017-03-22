'''
    test_module_listing.py test the module listing view.
'''
from paste.fixture import TestApp
from nose.tools import assert_equal, raises
from app import APP
from components import session


class TestCode(object):
    '''
        This class runs the test cases to test app home page
    '''
    FORM_FIXED_MOUNTING = '<form action="/moduleMountingFixed" method="post">'
    FORM_FIXED_MOUNTING_BUTTON = '<input class="btn btn-primary" type="submit" ' +\
                                 'value="Go To Module Mountings for Current AY" ' +\
                                 'data-toggle="tooltip" data-placement="bottom" ' +\
                                 'title="See fixed module mountings for current AY">'
    FORM_TENTATIVE_MOUNTING = '<form action="/moduleMountingTentative" ' +\
                              'method="post">'
    FORM_TENTATIVE_MOUNTING_BUTTON = '<input class="btn btn-primary" type="submit" ' +\
                                     'value="Go To Module Mountings for Other AYs" ' +\
                                     'data-toggle="tooltip" data-placement="bottom" ' +\
                                     'title="See tentative module mountings for other AYs">'

    TABLE_HEADER_CODE = '<th>Code</th>'
    TABLE_HEADER_NAME = '<th>Name</th>'
    TABLE_HEADER_DESCRIPTION = '<th>Description</th>'
    TABLE_HEADER_MC = '<th>MCs</th>'
    TABLE_HEADER_STATUS = '<th>Is New Module?</th>'
    TABLE_HEADER_ACTIONS = '<th data-sortable="false">Actions</th>'

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


    def tearDown(self):
        '''
            Tears down 'app.py' fixture and logs out
        '''
        session.tear_down(self.test_app)


    def test_index_valid_response(self):
        '''
            Tests if user can access the index page without request errors.
        '''
        root = self.test_app.get('/modules')

        # checks if HTTP response code is 200 (= OK)
        assert_equal(root.status, 200)


    def test_index_goto_fixed_module_mountings_response(self):
        '''
            Tests if navigation to 'Fixed Module Mountings' is successful.
        '''
        root = self.test_app.get('/modules')
        response = root.goto('/moduleMountingFixed', method='post')

        # checks if HTTP response code is 303 (= See Other)
        # because POST method in 'Fixed' class in 'modules.py'
        # redirects to its GET method.
        assert_equal(response.status, 303)


    def test_index_goto_tentative_module_mountings_response(self):
        '''
            Tests if navigation to 'Tentative Module Mountings' is successful.
        '''
        root = self.test_app.get('/modules')
        response = root.goto('/moduleMountingTentative', method='post')

        # checks if HTTP response code is 303 (= See Other)
        # because POST method in 'Tentative' class in 'modules.py'
        # redirects to its GET method.
        assert_equal(response.status, 303)


    def test_index_goto_valid_module_overview_page_response(self):
        '''
            Tests if navigation to a module overview page with
            a valid target module code is successful.
        '''
        root = self.test_app.get('/modules')
        response = root.goto('/viewModule?code=BT5110', method='get')

        # checks if HTTP response code is 200 (= OK)
        assert_equal(response.status, 200)


        # Presence of these elements indicates that the request
        # direction is correct.

        # Checks if page contains title of Module Info Overview page
        response.mustcontain("Module Info Overview")
        # Checks if page contains target module
        response.mustcontain("BT5110")


    @raises(Exception)
    def test_index_goto_invalid_module_overview_page_response(self):
        '''
            Tests if navigation to a module overview page with
            an invalid target module code will fail.
        '''
        root = self.test_app.get('/modules')
        # an exception WILL be encountered here
        response = root.goto('/viewModule?code=CS0123', method='get')


    def test_index_module_mounting_view_options(self):
        '''
            Tests if the 2 buttons for navigating to different types
            of mounting plans (fixed and tentative) exist.

            Each navigation is tied to a form that will handle the
            navigation redirections.
        '''
        root = self.test_app.get('/modules')

        # Checks the existence of the handler for viewing fixed mounting plan
        root.mustcontain(self.FORM_FIXED_MOUNTING)
        root.mustcontain(self.FORM_FIXED_MOUNTING_BUTTON)

        # Checks the existence of the handler for viewing tentative mounting plan
        root.mustcontain(self.FORM_TENTATIVE_MOUNTING)
        root.mustcontain(self.FORM_TENTATIVE_MOUNTING_BUTTON)


    def test_index_modules_listing(self):
        '''
            Tests if a table displaying a list of all modules exist.
        '''
        root = self.test_app.get('/modules')

        # Checks the existence of the handler for viewing fixed mounting plan
        root.mustcontain(self.TABLE_HEADER_CODE)
        root.mustcontain(self.TABLE_HEADER_NAME)
        root.mustcontain(self.TABLE_HEADER_DESCRIPTION)
        root.mustcontain(self.TABLE_HEADER_MC)
        root.mustcontain(self.TABLE_HEADER_STATUS)
        root.mustcontain(self.TABLE_HEADER_ACTIONS)
