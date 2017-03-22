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
from nose.tools import assert_equal
from app import APP
from components import session


class TestCode(object):
    '''
        This class contains methods that tests the page views and navigations inside
        the target page.
    '''


    URL_VIEW_MODULE_VALID = '/viewModule?code=BT5110'
    URL_VIEW_MODULE_INVALID = '/viewModule?code=CS0123'
    URL_STAR_MODULE = '/starModule?code=BT5110&action=star&return_path=/viewModule?code=BT5110'
    URL_UNSTAR_MODULE = '/starModule?code=BT5110&action=unstar&return_path=/viewModule?code=BT5110'

    URL_INDIV_MODULE_VIEW = '/individualModuleInfo?code=BT5110'
    URL_INDIV_MODULE_VIEW_INVALID = '/individualModuleInfo?code=CS0123'
    FORM_EDIT_MODULE_INFO = '<form id="edit-module-button" name="edit-module-button" '+\
                            'action="/editModule" method="get" class="no-padding-margin">'
    FORM_EDIT_MODULE_INFO_BUTTON = '<input class="dropdown-btn-custom" type="submit" value="Edit'+\
                                   ' General Module Info" data-toggle="tooltip" '+\
                                   'data-placement="right"'+\
                                   ' title="Edit the module\'s name, description, MC, '+\
                                   'pre-requisites and preclusions">'
    CONTENT_SUMMARY = "Module Info Overview"
    CONTENT_CODE = "BT5110"
    CONTENT_NAME = "Data Management and Warehousing"
    CONTENT_MC = "(4 MCs)"
    CONTENT_DESCRIPTION = "Module Description:"
    CONTENT_PRECLUSION = "Module Preclusions:"
    CONTENT_PREREQUISITE = "Module Prerequisites"
    CONTENT_INFO_FIXED = " <h4><b>Information for Current AY (Fixed)</b></h4>"
    CONTENT_INFO_TENTA = "Information for Future AYs (Tentative)"
    CONTENT_TABLE_MOUNT_FLAG = "<th>Mounted</th>"
    CONTENT_TABLE_QUOTA = "<th>Quota</th>"
    CONTENT_TABLE_STUDENT_DEMAND = "<th>Students Planning to Take</th>"


    FORM_OVERLAPPING_MODULE = '<form id="view-overlapping-with-module"'+\
                              ' name="view-overlapping-with-module"'+\
                              ' action="/overlappingWithModule" method="get" '+\
                              'class="no-padding-margin">'
    FORM_OVERLAPPING_MODULE_BUTTON = '<input type="submit" class="dropdown-btn-custom" '+\
                                     'value="View Modules'+\
                                     ' Overlapping With This Module" data-toggle="tooltip"'+\
                                     ' data-placement="right"'+\
                                     ' title="Show modules that are also taken with this module">'
    DROPDOWN_BTN = '<button type="button" class="btn btn-primary btn-lg dropdown-toggle '+\
                   'dropdown-btn-custom-main" data-toggle="dropdown" aria-haspopup="true" '+\
                   'aria-expanded="false">More Actions <span class="caret"></span></button>'

    CONTENT_STAR_BUTTON = '<span class="glyphicon glyphicon-star-empty">'
    CONTENT_UNSTAR_BUTTON = '<span class="glyphicon glyphicon-star">'


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


    def test_view_valid_module_overview_valid_response(self):
        '''
            Tests whether user can access page for showing module overview
            if target module is valid.
        '''
        root = self.test_app.get(self.URL_VIEW_MODULE_VALID)

        # checks if HTTP response code is 200 (= OK)
        assert_equal(root.status, 200)


    def test_view_invalid_module_overview_valid_response(self):
        '''
            Tests if user will fail to access page for showing module overview
            if target module is invalid.
        '''
        root = self.test_app.get(self.URL_VIEW_MODULE_INVALID)
        assert_equal(root.status, 200)

        # Presence of these elements indicates that the request direction is correct.
        # Checks if page contains 'Not Found'
        root.mustcontain("Not Found")


    def test_view_module_overview_goto_valid_individual_module(self):
        '''
            Tests if navigation to a valid individual module view
            is succesful.

            (i.e. navigation to module info for valid target module and
            valid target AY-semester and quota)
        '''
        root = self.test_app.get(self.URL_VIEW_MODULE_VALID)
        url = self.URL_INDIV_MODULE_VIEW + '&targetAY=AY+16%2F17+Sem+1'
        response = root.goto(url, method='get')

        # checks if HTTP response code is 200 (= OK)
        assert_equal(response.status, 200)


    def test_view_module_overview_goto_individual_module_invalid_code(self):
        '''
            Tests if navigation to an individual module view
            with invalid module code is unsuccesful.

            (i.e. navigation to module info for invalid target module and
            valid target AY-semester and quota)
        '''
        root = self.test_app.get(self.URL_VIEW_MODULE_VALID)
        url = self.URL_INDIV_MODULE_VIEW_INVALID + '&targetAY=AY+16%2F17+Sem+1'
        response = root.goto(url, method='get')

        assert_equal(response.status, 200)

        # Presence of these elements indicates that the request direction is correct.
        # Checks if page contains 'Not Found'
        response.mustcontain("Not Found")


    def test_view_module_overview_goto_individual_module_invalid_ay(self):
        '''
            Tests if navigation to an individual module view
            with invalid AY is unsuccesful.

            (i.e. navigation to module info for valid target module
            and semester but invalid AY)
        '''
        root = self.test_app.get(self.URL_VIEW_MODULE_VALID)
        url = self.URL_INDIV_MODULE_VIEW + '&targetAY=AY+16%2F18+Sem+1'
        response = root.goto(url, method='get')

        assert_equal(response.status, 200)
        response.mustcontain("Not Found")


    def test_view_module_overview_goto_individual_module_invalid_sem(self):
        '''
            Tests if navigation to an individual module view
            with invalid semester in URL is unsuccesful.

            (i.e. navigation to module info for valid target module
            and AY but invalid semester)
        '''
        root = self.test_app.get(self.URL_VIEW_MODULE_VALID)
        url = self.URL_INDIV_MODULE_VIEW + '&targetAY=AY+16%2F17+Sem+3'
        response = root.goto(url, method='get')

        assert_equal(response.status, 200)
        response.mustcontain("Not Found")


    def test_view_module_overview_contents(self):
        '''
            Tests if all the necessary info is displayed in the module
            overview page.
        '''
        root = self.test_app.get(self.URL_VIEW_MODULE_VALID)

        root.mustcontain(self.CONTENT_SUMMARY)
        root.mustcontain(self.CONTENT_CODE)
        root.mustcontain(self.CONTENT_NAME)
        root.mustcontain(self.CONTENT_MC)
        root.mustcontain(self.CONTENT_DESCRIPTION)
        root.mustcontain(self.CONTENT_PRECLUSION)
        root.mustcontain(self.CONTENT_PREREQUISITE)
        root.mustcontain(self.CONTENT_INFO_FIXED)
        root.mustcontain(self.CONTENT_INFO_TENTA)
        root.mustcontain(self.CONTENT_TABLE_MOUNT_FLAG)
        root.mustcontain(self.CONTENT_TABLE_QUOTA)
        root.mustcontain(self.CONTENT_TABLE_STUDENT_DEMAND)
        root.mustcontain(self.CONTENT_STAR_BUTTON)
        root.mustcontain(self.FORM_EDIT_MODULE_INFO)
        root.mustcontain(self.FORM_EDIT_MODULE_INFO_BUTTON)
        root.mustcontain(self.FORM_OVERLAPPING_MODULE)
        root.mustcontain(self.FORM_OVERLAPPING_MODULE_BUTTON)
        root.mustcontain(self.DROPDOWN_BTN)

    def test_contains_overlapping_module_table(self):
        '''
            Tests if user can access the 'Edit General Module Info' option
        '''
        root = self.test_app.get(self.URL_VIEW_MODULE_VALID)
        edit_form = root.forms__get()["edit-module-button"]

        response = edit_form.submit()
        assert_equal(response.status, 200)

    def test_goto_overlapping_with_module(self):
        '''
            test if user can access to moverlapping with module page
        '''
        root = self.test_app.get(self.URL_VIEW_MODULE_VALID)
        edit_form = root.forms__get()["view-overlapping-with-module"]

        response = edit_form.submit()
        assert_equal(response.status, 200)


    def test_click_star_button(self):
        '''
            Tests if user can star and unstar modules by clicking the button.
        '''
        root = self.test_app.get(self.URL_VIEW_MODULE_VALID)
        response = root.goto(self.URL_STAR_MODULE, method='get')
        assert_equal(response.status, 303)
        # follow back to view module page
        redirected = response.follow()
        assert_equal(redirected.status, 200)
        redirected.mustcontain(self.CONTENT_UNSTAR_BUTTON)

        # test unstarring now
        response = redirected.goto(self.URL_UNSTAR_MODULE, method='get')
        assert_equal(response.status, 303)
        # follow back to view module page
        redirected = response.follow()
        assert_equal(redirected.status, 200)
        redirected.mustcontain(self.CONTENT_STAR_BUTTON)
