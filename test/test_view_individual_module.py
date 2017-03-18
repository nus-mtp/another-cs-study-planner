'''
    test_view_individual_module.py tests the app's view individual mod page
'''
from paste.fixture import TestApp
from nose.tools import assert_equal
from app import APP
from components import session

class TestCode(object):
    '''
        This class runs the test cases to test app's view individual mod page
    '''

    URL_CONTAIN_CODE_AY_QUOTA = '/individualModuleInfo?' +\
                                'code=BT5110' +\
                                '&targetAY=AY+16%2F17+Sem+1' +\
                                '&quota=60'
    URL_CONTAIN_FUTURE_AY = '/individualModuleInfo?' +\
                            'code=BT5110' +\
                            '&targetAY=AY+17%2F18+Sem+1' +\
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
    URL_CONTAIN_CODE_AY_NO_QUOTA = '/individualModuleInfo' +\
                                   '?code=CP3880' +\
                                   '&targetAY=AY+16%2F17+Sem+1'+\
                                   '&quota='

    FORM_EDIT_MODULE_INFO = '<form id="edit-module-button" name="edit-module-button" ' +\
                            'action="/editModule" method="get">'
    FORM_EDIT_MODULE_INFO_BUTTON = '<input class="btn btn-lg btn-primary" ' +\
                                   'type="submit" value="Edit General Module Info" ' +\
                                   'data-toggle="tooltip" data-placement="right" ' +\
                                   'title="Edit the module\'s name, description, '+\
                                   'MC, pre-requisites and preclusions">'
    FORM_EDIT_SPECIFIC_MODULE_INFO = '<form id="edit-mounting-button" ' +\
                                     'name="edit-mounting-button" ' +\
                                     'action="/editMounting" method="get">'
    FORM_EDIT_SPECIFIC_MODULE_INFO_BUTTON = '<input class="btn btn-lg btn-primary" ' +\
                                            'type="submit" value="Edit Specific ' +\
                                            'Module Info" data-toggle="tooltip" ' +\
                                            'data-placement="right" title="Edit the ' +\
                                            'module\'s mounting and quota">'

    CONTENT_SUMMARY = '<h1 class="text-center"><b>Module Info for <u>AY 16/17 ' +\
                      'Sem 1</u></b></h1>'
    CONTENT_SUMMARY_FUTURE_AY = '<h1 class="text-center"><b>Module Info for ' +\
                                '<u>AY 17/18 Sem 1</u></b></h1>'
    CONTENT_CODE = "BT5110"
    CONTENT_NAME = "Data Management and Warehousing"
    CONTENT_MC = "(4 MCs)"
    CONTENT_BUTTON_TO_OVERVIEW_DATA = '<input type="hidden" name="code" ' +\
                                      'value="BT5110" />'
    CONTENT_BUTTON_TO_OVERVIEW_BUTTON = '<input class="btn btn-lg btn-primary" ' +\
                                        'type="submit" value="Back to Overview" />'
    CONTENT_DESCRIPTION = "Module Description:"
    CONTENT_PRECLUSION = "Module Preclusions:"
    CONTENT_PREREQUISITE = "Module Prerequisites"
    CONTENT_QUOTA = "Class Quota"
    CONTENT_QUOTA_ACTUAL = "60"
    CONTENT_STATS = "Module Statistics"
    CONTENT_CLASS_QUOTA_BLANK = "?"

    CONTENT_OVERLAPPING_MODULES_TABLE = '<table id="common-module-table" ' +\
                                        'class="table table-bordered table-hover' +\
                                        ' display dataTable">'
    CONTENT_OVERLAPPING_MODULES_TABLE_MODULE_1 = '<th>Module 1</th>'
    CONTENT_OVERLAPPING_MODULES_TABLE_MODULE_1_NAME = '<th>Name of Module 1</th>'
    CONTENT_OVERLAPPING_MODULES_TABLE_MODULE_2 = '<th>Module 2</th>'
    CONTENT_OVERLAPPING_MODULES_TABLE_MODULE_2_NAME = '<th>Name of Module 2</th>'
    CONTENT_OVERLAPPING_MODULES_TABLE_AY_SEM = '<th>For AY-Sem</th>'
    CONTENT_OVERLAPPING_MODULES_TABLE_NUM_STUDENTS = '<th>Number of Students</th>'


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


    def test_view_individual_module_valid_response(self):
        '''
            Tests whether user can access page for showing module overview
            if target module is valid.
        '''
        root = self.test_app.get(self.URL_CONTAIN_CODE_AY_QUOTA)

        # checks if HTTP response code is 200 (= OK)
        assert_equal(root.status, 200)


    def test_view_individual_module_invalid_code_response(self):
        '''
            Tests if user will fail to access page for showing module overview
            if target module is invalid.
        '''
        root = self.test_app.get(self.URL_CONTAIN_INVALID_CODE_AY_QUOTA)
        assert_equal(root.status, 200)

        # Presence of these elements indicates that the request direction is correct.
        # Checks if page contains 'Not Found'
        root.mustcontain("Not Found")


    '''
        Tests if user will fail to access page for showing module overview
        if the target AY-semester is invalid.
    '''
    def test_view_individual_module_invalid_ay_sem_response(self):
        # AY-Semester used here is '16/18 Sem 1'
        root = self.test_app.get(self.URL_CONTAIN_CODE_INVALID_AY_QUOTA)
        assert_equal(root.status, 200)

        # Presence of these elements indicates that the request direction is correct.
        # Checks if page contains 'Not Found'
        root.mustcontain("Not Found")


    def test_view_individual_module_contents(self):
        '''
            Tests if all the necessary info is displayed in the individual
            module view page.
        '''
        root = self.test_app.get(self.URL_CONTAIN_CODE_AY_QUOTA)

        root.mustcontain(self.CONTENT_SUMMARY)
        root.mustcontain(self.CONTENT_CODE)
        root.mustcontain(self.CONTENT_NAME)
        root.mustcontain(self.CONTENT_MC)
        root.mustcontain(self.CONTENT_BUTTON_TO_OVERVIEW_DATA)
        root.mustcontain(self.CONTENT_BUTTON_TO_OVERVIEW_BUTTON)
        root.mustcontain(self.CONTENT_DESCRIPTION)
        root.mustcontain(self.CONTENT_QUOTA)
        root.mustcontain(self.CONTENT_QUOTA_ACTUAL)
        root.mustcontain(self.CONTENT_STATS)
        root.mustcontain(self.FORM_EDIT_MODULE_INFO)
        root.mustcontain(self.FORM_EDIT_MODULE_INFO_BUTTON)


    def test_view_individual_module_contents_with_future_ay(self):
        '''
            Tests if all the necessary info is displayed in the individual
            module view page with future AY and Semester.
        '''
        root = self.test_app.get(self.URL_CONTAIN_FUTURE_AY)

        root.mustcontain(self.CONTENT_SUMMARY_FUTURE_AY)
        root.mustcontain(self.CONTENT_CODE)
        root.mustcontain(self.CONTENT_NAME)
        root.mustcontain(self.CONTENT_MC)
        root.mustcontain(self.CONTENT_BUTTON_TO_OVERVIEW_DATA)
        root.mustcontain(self.CONTENT_BUTTON_TO_OVERVIEW_BUTTON)
        root.mustcontain(self.CONTENT_DESCRIPTION)
        root.mustcontain(self.CONTENT_QUOTA)
        root.mustcontain(self.CONTENT_QUOTA_ACTUAL)
        root.mustcontain(self.CONTENT_STATS)
        root.mustcontain(self.FORM_EDIT_MODULE_INFO)
        root.mustcontain(self.FORM_EDIT_MODULE_INFO_BUTTON)
        root.mustcontain(self.FORM_EDIT_SPECIFIC_MODULE_INFO)
        root.mustcontain(self.FORM_EDIT_SPECIFIC_MODULE_INFO_BUTTON)


    def test_view_individual_module_no_quota_valid_response(self):
        '''
            Tests the contents when there is no quota specified
        '''
        root = self.test_app.get(self.URL_CONTAIN_CODE_AY_NO_QUOTA)

        root.mustcontain(self.CONTENT_CLASS_QUOTA_BLANK)


    def test_overlapping_table(self):
        '''
            Test if the overlapping modules table is available
        '''
        root = self.test_app.get(self.URL_CONTAIN_CODE_AY_QUOTA)

        root.mustcontain(self.CONTENT_OVERLAPPING_MODULES_TABLE)
        root.mustcontain(self.CONTENT_OVERLAPPING_MODULES_TABLE_MODULE_1)
        root.mustcontain(self.CONTENT_OVERLAPPING_MODULES_TABLE_MODULE_1_NAME)
        root.mustcontain(self.CONTENT_OVERLAPPING_MODULES_TABLE_MODULE_2)
        root.mustcontain(self.CONTENT_OVERLAPPING_MODULES_TABLE_MODULE_2_NAME)
        root.mustcontain(self.CONTENT_OVERLAPPING_MODULES_TABLE_AY_SEM)
        root.mustcontain(self.CONTENT_OVERLAPPING_MODULES_TABLE_NUM_STUDENTS)


    def test_goto_edit_general_info(self):
        '''
            Tests if user can access the 'Edit General Module Info' option
        '''
        root = self.test_app.get(self.URL_CONTAIN_CODE_AY_QUOTA)
        edit_form = root.forms__get()["edit-module-button"]

        response = edit_form.submit()
        assert_equal(response.status, 200)


    def test_goto_edit_specific_info(self):
        '''
            Tests if user can access the 'Edit Specific Module Info' option
        '''
        root = self.test_app.get(self.URL_CONTAIN_FUTURE_AY)
        edit_form = root.forms__get()["edit-mounting-button"]

        response = edit_form.submit()
        assert_equal(response.status, 200)
