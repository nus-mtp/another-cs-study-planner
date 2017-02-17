'''
    test_view_module.py tests the page views and navigations for
    viewing a target module's overview.

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

class TestCode(object):
    '''
        This class contains methods that tests the page views and navigations inside
        the target page.
    '''


    URL_VIEW_MODULE_VALID = '/viewModule?code=BT5110'
    URL_VIEW_MODULE_INVALID = '/viewModule?code=CS0123'

    FORM_SEARCH_MODULE = '<form class="search-form" id="search-form"'
    FORM_SEARCH_MODULE_LABEL_CODE = '<label for="module-code">Enter ' +\
                                    'Module Code: </label>'
    FORM_SEARCH_MODULE_INPUT_CODE_1 = '<input type="text"'
    FORM_SEARCH_MODULE_INPUT_CODE_2 = 'name="module-code"'
    FORM_SEARCH_MODULE_AY_SEM_LABEL = '<label for="ay-sem">Select Target ' +\
                                      'AY &amp; Semester: </label>'
    FORM_SEARCH_MODULE_AY_SEM_INPUT = '<select name="ay-sem" form="search-form">'
    FORM_SEARCH_MODULE_AY_SEM_BUTTON = '<button type="submit" class="btn ' +\
                                       'btn-primary">Search</button>'

    CONTENT_SUMMARY = "Module Info Overview"
    CONTENT_CODE = "BT5110"
    CONTENT_NAME = "Data Management and Warehousing"
    CONTENT_MC = "(4 MCs)"
    CONTENT_DESCRIPTION = "Module Description:"
    CONTENT_PRECLUSION = "Module Preclusions:"
    CONTENT_PREREQUISITE = "Module Prerequisites"
    CONTENT_QUOTA = "Class Quota for AY-Semesters"
    CONTENT_TABLE_AY_SEM = "<th>Mounted In</th>"
    CONTENT_TABLE_QUOTA = "<th>Quota</th>"
    CONTENT_TABLE_STUDENT_DEMAND = "<th>Students Planning to Take</th>"
    CONTENT_STATS = "Module Statistics"


    def test_view_valid_module_overview_valid_response(self):
        '''
            Tests whether user can access page for showing module overview
            if target module is valid.
        '''
        # loads a 'modules.py' fixture
        middleware = []
        test_app = TestApp(APP.wsgifunc(*middleware))
        root = test_app.get(self.URL_VIEW_MODULE_VALID)

        # checks if HTTP response code is 200 (= OK)
        assert_equal(root.status, 200)


    @raises(Exception)
    def test_view_invalid_module_overview_valid_response(self):
        '''
            Tests if user will fail to access page for showing module overview
            if target module is invalid.

            NOTE: this test case is supposed to FAIL
        '''
        # loads a 'modules.py' fixture
        middleware = []
        test_app = TestApp(APP.wsgifunc(*middleware))
        # an exception WILL be encountered here
        test_app.get(self.URL_VIEW_MODULE_INVALID)


    def test_view_module_overview_goto_valid_individual_module(self):
        '''
            Tests if navigation to a valid individual module view
            is succesful.

            (i.e. navigation to module info for valid target module and
            valid target AY-semester and quota)
        '''
        middleware = []
        test_app = TestApp(APP.wsgifunc(*middleware))
        root = test_app.get(self.URL_VIEW_MODULE_VALID)
        url = self.URL_VIEW_MODULE_VALID + '&targetAY=AY+16%2F17+Sem+1' +\
              '&quota=60'
        response = root.goto(url, method='get')

        # checks if HTTP response code is 200 (= OK)
        assert_equal(response.status, 200)


    @raises(Exception)
    def test_view_module_overview_goto_individual_module_invalid_code(self):
        '''
            Tests if navigation to an individual module view
            with invalid module code is unsuccesful.

            (i.e. navigation to module info for invalid target module and
            valid target AY-semester and quota)
        '''
        middleware = []
        test_app = TestApp(APP.wsgifunc(*middleware))
        root = test_app.get(self.URL_VIEW_MODULE_VALID)
        url = self.URL_VIEW_MODULE_INVALID + '&targetAY=AY+16%2F17+Sem+1' +\
              '&quota=60'
        root.goto(url, method='get')


    '''
        Tests if navigation to an individual module view
        with invalid AY-semester is unsuccesful.

        (i.e. navigation to module info for valid target module and
        quota, but invalid AY-semester)

        NOTE: Checking for invalid AY-semester is not implemented yet.
    '''
    '''
    @raises(Exception)
    def test_view_module_overview_goto_individual_module_invalid_ay_sem(self):
        middleware = []
        test_app = TestApp(app.wsgifunc(*middleware))
        root = test_app.get(self.URL_VIEW_MODULE_VALID)
        url = self.URL_VIEW_MODULE_VALID + '&targetAY=AY+16%2F18+Sem+1' +\
              '&quota=60'
        response = root.goto(url, method='get')
    '''


    '''
        Tests if navigation to an individual module view
        with invalid quota is unsuccesful.

        (i.e. navigation to module info for invalid quota and
        valid target module and AY-semester)

        NOTE: Checking for invalid quota is not implemented yet.
    '''
    '''
    @raises(Exception)
    def test_view_module_overview_goto_individual_module_invalid_quota(self):
        middleware = []
        test_app = TestApp(app.wsgifunc(*middleware))
        root = test_app.get(self.URL_VIEW_MODULE_VALID)
        url = self.URL_VIEW_MODULE_VALID + '&targetAY=AY+16%2F17+Sem+1' +\
              '&quota=70'
        response = root.goto(url, method='get')
    '''


    def test_view_module_overview_search_form(self):
        '''
            Tests if the module-search form exists.

            NOTE: the current form is NON_FUNCTIONAL at the moment.
        '''
        middleware = []
        testApp = TestApp(APP.wsgifunc(*middleware))
        root = testApp.get(self.URL_VIEW_MODULE_VALID)

        root.mustcontain(self.FORM_SEARCH_MODULE)
        root.mustcontain(self.FORM_SEARCH_MODULE_LABEL_CODE)
        root.mustcontain(self.FORM_SEARCH_MODULE_INPUT_CODE_1)
        root.mustcontain(self.FORM_SEARCH_MODULE_INPUT_CODE_2)
        root.mustcontain(self.FORM_SEARCH_MODULE_AY_SEM_LABEL)
        root.mustcontain(self.FORM_SEARCH_MODULE_AY_SEM_INPUT)
        root.mustcontain(self.FORM_SEARCH_MODULE_AY_SEM_BUTTON)


    def test_view_module_overview_contents(self):
        '''
            Tests if all the necessary info is displayed in the module
            overview page.
        '''
        middleware = []
        testApp = TestApp(APP.wsgifunc(*middleware))
        root = testApp.get(self.URL_VIEW_MODULE_VALID)

        root.mustcontain(self.CONTENT_SUMMARY)
        root.mustcontain(self.CONTENT_CODE)
        root.mustcontain(self.CONTENT_NAME)
        root.mustcontain(self.CONTENT_MC)
        root.mustcontain(self.CONTENT_DESCRIPTION)
        root.mustcontain(self.CONTENT_PRECLUSION)
        root.mustcontain(self.CONTENT_PREREQUISITE)
        root.mustcontain(self.CONTENT_QUOTA)
        root.mustcontain(self.CONTENT_TABLE_AY_SEM)
        root.mustcontain(self.CONTENT_TABLE_QUOTA)
        root.mustcontain(self.CONTENT_TABLE_STUDENT_DEMAND)
        root.mustcontain(self.CONTENT_STATS)
