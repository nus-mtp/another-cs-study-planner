from paste.fixture import TestApp
from nose.tools import *
from modules import app
import os

class TestCode():

    URL_MODULE_MOUNTING_FIXED = '/moduleMountingFixed'
    URL_MODULE_VIEW_OVERVIEW = '/viewModule?code=BT5110'
    URL_MODULE_VIEW_INVALID = '/viewModule?code=CS0123'

    FORM_ALL_MODULES = '<form class="navForm" action="/modules" method="post">'
    FORM_ALL_MODULES_BUTTON = '<input class="btn btn-primary" ' +\
                              'type="submit" value="Go To All Modules">'
    FORM_TENTATIVE_MOUNTING = '<form class="navForm" action=' +\
                              '"/moduleMountingTentative" ' +\
                              'method="post">'
    FORM_TENTATIVE_MOUNTING_BUTTON = '<input class="btn btn-primary" ' +\
                                     'type="submit" value="Go To Tentative ' +\
                                     'Module Mountings">'

    TABLE_HEADER_CODE = '<th>Code</th>'
    TABLE_HEADER_NAME = '<th>Name</th>'
    TABLE_HEADER_MOUNTING = '<th>Mounted In</th>'
    TABLE_HEADER_MC = '<th>Quota</th>'
    TABLE_HEADER_ACTION = '<th>Action</th>'

    """
        Tests whether user can access page for showing fixed module
        mountings without request errors.
    """
    def test_fixed_module_mounting_valid_response(self):
        # loads a 'modules.py' fixture
        middleware = []
        testApp = TestApp(app.wsgifunc(*middleware))
        root = testApp.get(self.URL_MODULE_MOUNTING_FIXED)

        # checks if HTTP response code is 200 (= OK)
        assert_equal(root.status, 200)


    """
        Tests if navigation to a module overview page with
        a valid target module code is successful.
    """
    def test_fixed_module_mounting_goto_valid_module_overview_page_response(
            self):
        middleware = []
        testApp = TestApp(app.wsgifunc(*middleware))
        root = testApp.get(self.URL_MODULE_MOUNTING_FIXED)
        response = root.goto(self.URL_MODULE_VIEW_OVERVIEW, method='get')

        # checks if HTTP response code is 200 (= OK)
        assert_equal(response.status, 200)

        """
            Presence of these elements indicates that the request
            direction is correct.
        """
        # Checks if page contains title of Module Info Overview page
        response.mustcontain("Module Info Overview")
        # Checks if page contains target module
        response.mustcontain("BT5110")


    """
        Tests if navigation to a module overview page with
        an invalid target module code will fail.

        NOTE: this test case is supposed to FAIL.
    """
    @raises(Exception)
    def test_fixed_module_mounting_goto_invalid_module_overview_page_response(
            self):
        middleware = []
        testApp = TestApp(app.wsgifunc(*middleware))
        root = testApp.get(self.URL_MODULE_MOUNTING_FIXED)
        # an exception WILL be encountered here
        response = root.goto(self.URL_MODULE_VIEW_INVALID, method='get')


    """
        Tests if navigations to full module listing and tentative
        module mounting plans exist.
    """
    def test_fixed_module_mounting_view_options(self):
        middleware = []
        testApp = TestApp(app.wsgifunc(*middleware))
        root = testApp.get(self.URL_MODULE_MOUNTING_FIXED)
        
        # Checks the existence of the handler for viewing fixed mounting plan
        root.__contains__(self.FORM_ALL_MODULES)
        root.__contains__(self.FORM_ALL_MODULES_BUTTON)

        # Checks the existence of the handler for viewing tentative mounting plan
        root.__contains__(self.FORM_TENTATIVE_MOUNTING)
        root.__contains__(self.FORM_TENTATIVE_MOUNTING_BUTTON)


    """
        Tests if a table displaying list of modules for fixed
        module mounting exists.
    """
    def test_fixed_module_mounting_module_listing(self):
        middleware = []
        testApp = TestApp(app.wsgifunc(*middleware))
        root = testApp.get(self.URL_MODULE_MOUNTING_FIXED)

        root.__contains__(self.TABLE_HEADER_CODE)
        root.__contains__(self.TABLE_HEADER_NAME)
        root.__contains__(self.TABLE_HEADER_MOUNTING)
        root.__contains__(self.TABLE_HEADER_MC)
        root.__contains__(self.TABLE_HEADER_ACTION)
