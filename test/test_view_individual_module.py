'''
    test_view_individual_module.py tests the app's view individual mod page
'''
from paste.fixture import TestApp
from nose.tools import assert_equal, raises
from modules import APP

class TestCode(object):
    '''
        This class runs the test cases to test app's view individual mod page
    '''

    URL_CONTAIN_CODE_AY_QUOTA = '/individualModuleInfo?' +\
                                'code=BT5110' +\
                                '&targetAY=AY+16%2F17+Sem+1' +\
                                '&quota=60'
    URL_CONTAIN_INVALID_CODE_AY_QUOTA = '/individualModuleInfo?' +\
                                'code=CS0123' +\
                                '&targetAY=AY+16%2F17+Sem+1' +\
                                '&quota=60'
    URL_CONTAIN_CODE_INVALID_AY_QUOTA = '/individualModuleInfo?' +\
                                        'code=BT5110' +\
                                        '&targetAY=AY+16%2F18+Sem+1' +\
                                        '&quota=60'
    URL_CONTAIN_CODE_AY_INVALID_QUOTA = '/individualModuleInfo?' +\
                                        'code=BT5110' +\
                                        '&targetAY=AY+16%2F17+Sem+1' +\
                                        '&quota=70'
    URL_CONRAIN_CODE_AY_NO_QUOTA = '/individualModuleInfo' +\
                                   '?code=CP3880' +\
                                   '&targetAY=AY+16%2F17+Sem+1'+\
                                   '&quota='

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
    CONTENT_CLASS_QUOTA_BLANK = "<p></p>"


    def test_view_individual_module_valid_response(self):
        '''
            Tests whether user can access page for showing module overview
            if target module is valid.
        '''
        # loads a 'modules.py' fixture
        middleware = []
        test_app = TestApp(APP.wsgifunc(*middleware))
        root = test_app.get(self.URL_CONTAIN_CODE_AY_QUOTA)

        # checks if HTTP response code is 200 (= OK)
        assert_equal(root.status, 200)


    @raises(Exception)
    def test_view_individual_module_invalid_code_response(self):
        '''
            Tests if user will fail to access page for showing module overview
            if target module is invalid.

            NOTE: this test case is supposed to FAIL
        '''
        # loads a 'modules.py' fixture
        middleware = []
        test_app = TestApp(APP.wsgifunc(*middleware))
        # an exception WILL be encountered here
        test_app.get(self.URL_CONTAIN_INVALID_CODE_AY_QUOTA)


    '''
        Tests if user will fail to access page for showing module overview
        if the target AY-semester is invalid.

        NOTE: this test case is supposed to FAIL
        NOTE: Checking for invalid AY-semester is not implemented
    '''
    '''
    @raises(Exception)
    def test_view_individual_module_invalid_ay_sem_response(self):
        # loads a 'modules.py' fixture
        middleware = []
        testApp = TestApp(APP.wsgifunc(*middleware))
        # AY-Semester used here is '16/18 Sem 1'
        # an exception WILL be encountered here
        root = testApp.get(self.URL_CONTAIN_CODE_INVALID_AY_QUOTA)
    '''


    '''
        Tests if user will fail to access page for showing module overview
        if the quota associated with the target module is invalid.

        NOTE: this test case is supposed to FAIL
        NOTE: Checking for invalid module quota is not implemented
    '''
    '''
    @raises(Exception)
    def test_view_invalid_module_overview_invalid_quota_response(self):
        # loads a 'modules.py' fixture
        middleware = []
        testApp = TestApp(APP.wsgifunc(*middleware))
        # Quota used here is '70' (actual is '60')
        # an exception WILL be encountered here
        root = testApp.get(self.URL_CONTAIN_CODE_AY_INVALID_QUOTA)
    '''


    def test_view_individual_module_search_form(self):
        '''
            Tests if the module-search form exists.

            NOTE: the current form is NON_FUNCTIONAL at the moment.
        '''
        middleware = []
        test_app = TestApp(APP.wsgifunc(*middleware))
        root = test_app.get(self.URL_CONTAIN_CODE_AY_QUOTA)

        root.mustcontain(self.FORM_SEARCH_MODULE)
        root.mustcontain(self.FORM_SEARCH_MODULE_LABEL_CODE)
        root.mustcontain(self.FORM_SEARCH_MODULE_INPUT_CODE_1)
        root.mustcontain(self.FORM_SEARCH_MODULE_INPUT_CODE_2)
        root.mustcontain(self.FORM_SEARCH_MODULE_AY_SEM_LABEL)
        root.mustcontain(self.FORM_SEARCH_MODULE_AY_SEM_INPUT)
        root.mustcontain(self.FORM_SEARCH_MODULE_AY_SEM_BUTTON)


    def test_view_individual_module_contents(self):
        '''
            Tests if all the necessary info is displayed in the module
            overview page.
        '''
        middleware = []
        test_app = TestApp(APP.wsgifunc(*middleware))
        root = test_app.get(self.URL_CONTAIN_CODE_AY_QUOTA)

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


    def test_view_individual_module_no_quota_valid_response(self):
        '''
            Tests the contents when there is no quota specified
        '''
        middleware = []
        test_app = TestApp(APP.wsgifunc(*middleware))
        root = test_app.get(self.URL_CONRAIN_CODE_AY_NO_QUOTA)

        root.mustcontain(self.CONTENT_CLASS_QUOTA_BLANK)
