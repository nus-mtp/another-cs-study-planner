'''
    test_module_mounting_tentative.py tests the page views and navigations for
    viewing tentative mounting modules.

    Firstly, we specify a target URL for conducting UI testing.

    Then, we proceed to test the following things:
    #1 Accessing the target page should be possible (i.e. response code should be 200 OK).
    #2 The necessary HTML elements are contained in the page view for target page.
    #3 Navigating to other valid pages from the target page should be successful.

    For #3, we do not check the full correctness of the UI for the other pages, as this
    will be handled by its corresponding test cases.
'''


from paste.fixture import TestApp
from nose.tools import assert_equal, raises
from app import APP
from components import session


class TestCode(object):
    '''
        This class contains methods that tests the page views and navigations inside
        the target page.
    '''

    URL_MODULE_MOUNTING_TENTATIVE = '/moduleMountingTentative'
    URL_MODULE_VIEW_VALID = '/viewModule?code=BT5110'
    URL_MODULE_VIEW_INVALID = '/viewModule?code=CS0123'

    FORM_ALL_MODULES = '<form class="navForm" action="/modules" method="post">'
    FORM_ALL_MODULES_BUTTON = '<input class="btn btn-primary" type="submit" ' +\
                              'value="Go To Module Information" ' +\
                              'data-toggle="tooltip" data-placement="bottom" ' +\
                              'title="See all modules that exist in the system">'
    FORM_FIXED_MOUNTING = '<form class="navForm" action=' +\
                          '"/moduleMountingFixed" ' +\
                          'method="post">'
    FORM_FIXED_MOUNTING_BUTTON = '<input class="btn btn-primary" type="submit" ' +\
                                 'value="Go To Module Mountings for Current AY" ' +\
                                 'data-toggle="tooltip" data-placement="bottom" ' +\
                                 'title="See fixed module mountings for current AY">'

    TABLE_HEADER_CODE = '<th>Code</th>'
    TABLE_HEADER_NAME = '<th>Name</th>'
    TABLE_HEADER_MOUNTING_SEM_1 = '<th data-sortable="false">' +\
                                  'Mounted In Sem 1</th>'
    TABLE_HEADER_MOUNTING_SEM_2 = '<th data-sortable="false">' +\
                                  'Mounted In Sem 2</th>'
    TABLE_MOUNTING_SYMBOL_MOUNTED = '<span class="glyphicon glyphicon-ok" ' +\
                                    'data-toggle="tooltip" data-placement="bottom" ' +\
                                    'title="Mounted"></span>'
    TABLE_MOUNTING_SYMBOL_UNMOUNTED = '<span class="glyphicon glyphicon-remove" ' +\
                                      'data-toggle="tooltip" data-placement="bottom' +\
                                      '" title="Unmounted"></span>'
    TABLE_MOUNTING_SYMBOL_NOT_MOUNTED = '<span class="glyphicon glyphicon-minus" ' +\
                                        'data-toggle="tooltip" data-placement="' +\
                                        'bottom" title="Not Mounted"></span>'


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


    def test_tentative_module_mounting_valid_response(self):
        '''
            Tests whether user can access page for showing tentative module
            mountings without request errors.
        '''
        root = self.test_app.get(self.URL_MODULE_MOUNTING_TENTATIVE)

        # checks if HTTP response code is 200 (= OK)
        assert_equal(root.status, 200)


    def test_tentative_module_mounting_goto_valid_module_overview_response(
            self):
        '''
            Tests if navigation to a module overview page with
            a valid target module code is successful.
        '''
        root = self.test_app.get(self.URL_MODULE_MOUNTING_TENTATIVE)
        response = root.goto(self.URL_MODULE_VIEW_VALID, method='get')

        # checks if HTTP response code is 200 (= OK)
        assert_equal(response.status, 200)

        # Presence of these elements indicates that the request direction is correct.
        # Checks if page contains title of Module Info Overview page
        response.mustcontain("Module Info Overview")
        # Checks if page contains target module
        response.mustcontain("BT5110")


    @raises(Exception)
    def test_tentative_module_mounting_goto_invalid_module_overview_response(
            self):
        '''
            Tests if navigation to a module overview page with
            an invalid target module code will fail.

            NOTE: this test case is supposed to FAIL.
        '''
        root = self.test_app.get(self.URL_MODULE_MOUNTING_TENTATIVE)
        # an exception WILL be encountered here
        response = root.goto(self.URL_MODULE_VIEW_INVALID, method='get')


    def test_tentative_module_mounting_view_options(self):
        '''
            Tests if navigations to full module listing and fixed
            module mounting plans exist.
        '''
        root = self.test_app.get(self.URL_MODULE_MOUNTING_TENTATIVE)

        # Checks the existence of the handler for viewing fixed mounting plan
        root.mustcontain(self.FORM_ALL_MODULES)
        root.mustcontain(self.FORM_ALL_MODULES_BUTTON)

        # Checks the existence of the handler for viewing tentative mounting plan
        root.mustcontain(self.FORM_FIXED_MOUNTING)
        root.mustcontain(self.FORM_FIXED_MOUNTING_BUTTON)


    def test_tentative_module_mounting_module_listing(self):
        '''
            Tests if a table displaying list of modules for tentative
            module mounting exists.
        '''
        root = self.test_app.get(self.URL_MODULE_MOUNTING_TENTATIVE)

        root.mustcontain(self.TABLE_HEADER_CODE)
        root.mustcontain(self.TABLE_HEADER_NAME)
        root.mustcontain(self.TABLE_HEADER_MOUNTING_SEM_1)
        root.mustcontain(self.TABLE_HEADER_MOUNTING_SEM_2)
        root.mustcontain(self.TABLE_MOUNTING_SYMBOL_MOUNTED)
        root.mustcontain(self.TABLE_MOUNTING_SYMBOL_NOT_MOUNTED)
