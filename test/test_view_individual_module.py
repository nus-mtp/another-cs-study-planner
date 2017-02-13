from paste.fixture import TestApp
from nose.tools import *
from modules import app
import os

class TestCode():

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

    CONTENT_SUMMARY = "Module Info for "
    CONTENT_TARGET_AY_SEM = "<b><u>AY 16/17 Sem 1</u></b>"
    CONTENT_CODE = "BT5110"
    CONTENT_NAME = "Data Management and Warehousing"
    CONTENT_MC = "(4 MCs)"
    CONTENT_BUTTON_EDIT = '<button class="btn btn-lg btn-primary" action="#">' +\
                          'Edit Module</button>'
    CONTENT_DESCRIPTION = "Module Description:"
    CONTENT_PRECLUSION = "Module Preclusions:"
    CONTENT_PREREQUISITE = "Module Prerequisites"
    CONTENT_QUOTA = "Class Quota"
    CONTENT_QUOTA_ACTUAL = "60"
    CONTENT_STATS = "Module Statistics"

    """
        Tests whether user can access page for showing module overview
        if target module is valid.
    """
    def test_view_individual_module_valid_response(self):
        # loads a 'modules.py' fixture
        middleware = []
        testApp = TestApp(app.wsgifunc(*middleware))
        url = '/individualModuleInfo?code=BT5110&targetAY=AY+16%2F17+Sem+1' +\
              '&quota=60'
        root = testApp.get(url)

        # checks if HTTP response code is 200 (= OK)
        assert_equal(root.status, 200)


    """
        Tests if user will fail to access page for showing module overview
        if target module is invalid.

        NOTE: this test case is supposed to FAIL
    """
    @raises(Exception)
    def test_view_individual_module_invalid_code_response(self):
        # loads a 'modules.py' fixture
        middleware = []
        testApp = TestApp(app.wsgifunc(*middleware))
        # an exception WILL be encountered here
        url = '/individualModuleInfo?code=CS0123&targetAY=AY+16%2F17+Sem+1' +\
              '&quota=60'
        root = testApp.get(url)


    """
        Tests if user will fail to access page for showing module overview
        if the target AY-semester is invalid.

        NOTE: this test case is supposed to FAIL
    """
    @raises(Exception)
    def test_view_individual_module_invalid_ay_sem_response(self):
        # loads a 'modules.py' fixture
        middleware = []
        testApp = TestApp(app.wsgifunc(*middleware))
        # AY-Semester used here is '16/18 Sem 1'
        # an exception WILL be encountered here
        url = '/individualModuleInfo?code=BT5110&targetAY=AY+16%2F18+Sem+1' +\
              '&quota=60'
        root = testApp.get(url)


    """
        Tests if user will fail to access page for showing module overview
        if the quota associated with the target module is invalid.

        NOTE: this test case is supposed to FAIL
    """
    @raises(Exception)
    def test_view_invalid_module_overview_invalid_quota_response(self):
        # loads a 'modules.py' fixture
        middleware = []
        testApp = TestApp(app.wsgifunc(*middleware))
        # Quota used here is '70' (actual is '60')
        # an exception WILL be encountered here
        url = '/individualModuleInfo?code=BT5110&targetAY=AY+16%2F18+Sem+1' +\
              '&quota=70'
        root = testApp.get(url)


    """
        Tests if the module-search form exists.

        NOTE: the current form is NON_FUNCTIONAL at the moment.
    """
    def test_view_individual_module_search_form(self):
        middleware = []
        testApp = TestApp(app.wsgifunc(*middleware))
        url = '/individualModuleInfo?code=BT5110&targetAY=AY+16%2F17+Sem+1' +\
              '&quota=60'
        root = testApp.get(url)

        root.mustcontain(self.FORM_SEARCH_MODULE)
        root.mustcontain(self.FORM_SEARCH_MODULE_LABEL_CODE)
        root.mustcontain(self.FORM_SEARCH_MODULE_INPUT_CODE_1)
        root.mustcontain(self.FORM_SEARCH_MODULE_INPUT_CODE_2)
        root.mustcontain(self.FORM_SEARCH_MODULE_AY_SEM_LABEL)
        root.mustcontain(self.FORM_SEARCH_MODULE_AY_SEM_INPUT)
        root.mustcontain(self.FORM_SEARCH_MODULE_AY_SEM_BUTTON)


    """
        Tests if all the necessary info is displayed in the module
        overview page.
    """
    def test_view_individual_module_contents(self):
        middleware = []
        testApp = TestApp(app.wsgifunc(*middleware))
        url = '/individualModuleInfo?code=BT5110&targetAY=AY+16%2F17+Sem+1' +\
              '&quota=60'
        root = testApp.get(url)

        root.mustcontain(self.CONTENT_SUMMARY + self.CONTENT_TARGET_AY_SEM)
        root.mustcontain(self.CONTENT_CODE)
        root.mustcontain(self.CONTENT_NAME)
        root.mustcontain(self.CONTENT_MC)
        root.mustcontain(self.CONTENT_BUTTON_EDIT)
        root.mustcontain(self.CONTENT_DESCRIPTION)
        root.mustcontain(self.CONTENT_PRECLUSION)
        root.mustcontain(self.CONTENT_PREREQUISITE)
        root.mustcontain(self.CONTENT_QUOTA)
        root.mustcontain(self.CONTENT_QUOTA_ACTUAL)
        root.mustcontain(self.CONTENT_STATS)
