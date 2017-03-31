'''
    test_modules_modified.py tests the application's Modified Modules page.
'''
from paste.fixture import TestApp
from nose.tools import assert_equal, raises, assert_false
from app import APP
from components import session

class TestCode(object):
    '''
        This class runs the test cases to test the Modified Modules page
    '''


    URL_VALID_GENERAL_CHANGE_LISTING = '/modifiedModules'
    URL_VALID_SPECIFIC_MOUNTING_CHANGE = '/modifiedModules?' +\
                                         'modifyType=mounting&code=MM1006'
    URL_VALID_SPECIFIC_QUOTA_CHANGE = '/modifiedModules?' +\
                                      'modifyType=quota&code=MM1008'
    URL_VALID_SPECIFIC_DETAILS_CHANGE = '/modifiedModules?' +\
                                        'modifyType=moduleDetails&code=MM1009'
    URL_INVALID_MODULE_CODE = '/modifiedModules?' +\
                              'modifyType=mounting&code=MM0000'
    URL_INVALID_CHANGE_TYPE = '/modifiedModules?' +\
                              'modifyType=mounting&code=MM1009'

    TAB_VIEW_HEADERS = '<ul class="nav nav-tabs nav-justified">'
    TAB_VIEW_CONTENT = '<div class="tab-content">'
    TAB_VIEW_ALL = '<div class="tab-pane active" id="all">'
    TAB_VIEW_MOUNTING = '<div class="tab-pane" id="mounting">'
    TAB_VIEW_QUOTA = '<div class="tab-pane" id="quota">'
    TAB_VIEW_MODULE_DETAILS = '<div class="tab-pane" id="moduleDetails">'

    ALL_TABLES_CODE_HEADER = '<th>Code</th>'
    ALL_TABLES_NAME_HEADER = '<th>Name</th>'
    ALL_TABLES_RESTORE_HEADER = '<th data-sortable="false">Restore</th>'

    SUMMARY_TABLE_MOUNTING_FLAG = '<th>Is Mounting Modified?</th>'
    SUMMARY_TABLE_QUOTA_FLAG = '<th>Is Quota Modified?</th>'
    SUMMARY_TABLE_DETAILS_FLAG = '<th>Is Module Details Modified?</th>'

    MOUNTING_CHANGES_TABLE_MOUNTING_CHANGE = '<th>Change in Mounting</th>'

    QUOTA_CHANGES_TABLE_OLD_QUOTA = 'Old Quota</th>'
    QUOTA_CHANGES_TABLE_NEW_QUOTA = 'New Quota</th>'
    QUOTA_CHANGES_TABLE_QUOTA_CHANGE = '<th>Change in Quota</th>'

    DETAIL_CHANGES_TABLE_DETAIL_CHANGE = '<th>Change in Details</th>'
    DETAIL_CHANGES_TABLE_DETAIL_CHANGE_BUTTON = '<input class="btn btn-lg ' +\
                                                'btn-primary" type="submit" ' +\
                                                'value="Restore Details">'

    DETAIL_CHANGES_TARGET_MODULE_PANELS = '<div class="panel panel-primary">'
    DETAIL_CHANGES_TARGET_MODULE_OLD_DETAILS = '<h3 class="text-center">' +\
                                               'Old Details</h3>'
    DETAIL_CHANGES_TARGET_MODULE_NEW_DETAILS = '<h3 class="text-center">' +\
                                               'New Details</h3>'
    DETAIL_CHANGES_TARGET_MODULE_NAME_HEADER = '<div class="panel-heading">' +\
                                               '<b>Name</b></div>'
    DETAIL_CHANGES_TARGET_MODULE_DESC_HEADER = '<div class="panel-heading">' +\
                                               '<b>Description</b></div>'
    DETAIL_CHANGES_TARGET_MODULE_MC_HEADER = '<div class="panel-heading">' +\
                                             '<b>MCs</b></div>'
    DETAIL_CHANGES_TARGET_MODULE_PANEL_BODY = '<div class="panel-body">'

    RESTORE_BUTTON_GLYPHICON = '<span class="glyphicon glyphicon-refresh"></span>'

    def __init__(self):
        '''
            Initialise testcode
        '''
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


    def test_view_page_for_all_modules_valid_response(self):
        '''
            Tests if viewing page displaying module changes
            for all modules with correct URL is successful.
        '''
        root = self.test_app.get(self.URL_VALID_GENERAL_CHANGE_LISTING)
        assert_equal(root.status, 200)


    def test_view_page_for_all_modules_valid_contents(self):
        '''
            Tests if expected contents are present in the
            page for viewing all module changes.
        '''
        root = self.test_app.get(self.URL_VALID_GENERAL_CHANGE_LISTING)

        root.mustcontain(self.TAB_VIEW_HEADERS)
        root.mustcontain(self.TAB_VIEW_CONTENT)
        root.mustcontain(self.TAB_VIEW_ALL)
        root.mustcontain(self.TAB_VIEW_MOUNTING)
        root.mustcontain(self.TAB_VIEW_QUOTA)
        root.mustcontain(self.TAB_VIEW_MODULE_DETAILS)

        root.mustcontain(self.ALL_TABLES_CODE_HEADER)
        root.mustcontain(self.ALL_TABLES_NAME_HEADER)
        root.mustcontain(self.ALL_TABLES_RESTORE_HEADER)

        root.mustcontain(self.SUMMARY_TABLE_MOUNTING_FLAG)
        root.mustcontain(self.SUMMARY_TABLE_QUOTA_FLAG)
        root.mustcontain(self.SUMMARY_TABLE_DETAILS_FLAG)

        root.mustcontain(self.MOUNTING_CHANGES_TABLE_MOUNTING_CHANGE)

        root.mustcontain(self.QUOTA_CHANGES_TABLE_OLD_QUOTA)
        root.mustcontain(self.QUOTA_CHANGES_TABLE_NEW_QUOTA)
        root.mustcontain(self.QUOTA_CHANGES_TABLE_QUOTA_CHANGE)

        root.mustcontain(self.DETAIL_CHANGES_TABLE_DETAIL_CHANGE)


    def test_view_target_module_mounting_change_valid_response(self):
        '''
            Tests if viewing page displaying mounting changes
            for a target module with correct URL is successful.
        '''
        root = self.test_app.get(self.URL_VALID_SPECIFIC_MOUNTING_CHANGE)
        assert_equal(root.status, 200)


    def test_view_target_module_mounting_change_valid_contents(self):
        '''
            Tests if expected contents are present in viewing the
            page for displaying mounting changes for a target module
            with correct URL.
        '''
        root = self.test_app.get(self.URL_VALID_SPECIFIC_MOUNTING_CHANGE)

        root.mustcontain('Modified Mounting of <b>MM1006</b>')
        root.mustcontain(self.ALL_TABLES_CODE_HEADER)
        root.mustcontain(self.ALL_TABLES_NAME_HEADER)
        root.mustcontain(self.ALL_TABLES_RESTORE_HEADER)
        root.mustcontain(self.MOUNTING_CHANGES_TABLE_MOUNTING_CHANGE)


    def test_view_target_module_quota_change_valid_response(self):
        '''
            Tests if viewing page displaying quota changes
            for a target module with correct URL is successful.
        '''
        root = self.test_app.get(self.URL_VALID_SPECIFIC_QUOTA_CHANGE)
        assert_equal(root.status, 200)


    def test_view_target_module_quota_change_valid_contents(self):
        '''
            Tests if expected contents are present in viewing the
            page displaying quota changes for a target module
            with correct URL.
        '''
        root = self.test_app.get(self.URL_VALID_SPECIFIC_QUOTA_CHANGE)

        root.mustcontain('Modified Quota of <b>MM1008</b>')
        root.mustcontain(self.ALL_TABLES_CODE_HEADER)
        root.mustcontain(self.ALL_TABLES_NAME_HEADER)
        root.mustcontain(self.ALL_TABLES_RESTORE_HEADER)
        root.mustcontain(self.QUOTA_CHANGES_TABLE_OLD_QUOTA)
        root.mustcontain(self.QUOTA_CHANGES_TABLE_NEW_QUOTA)
        root.mustcontain(self.QUOTA_CHANGES_TABLE_QUOTA_CHANGE)
        root.mustcontain(self.RESTORE_BUTTON_GLYPHICON)


    def test_view_target_module_details_change_valid_response(self):
        '''
            Tests if viewing page displaying details changes
            for a target module with correct URL is successful.
        '''
        root = self.test_app.get(self.URL_VALID_SPECIFIC_DETAILS_CHANGE)
        assert_equal(root.status, 200)


    def test_view_target_module_details_change_valid_contents(self):
        '''
            Tests if expected contents are present in viewing the
            page displaying details changes for a target module
            with correct URL.
        '''
        root = self.test_app.get(self.URL_VALID_SPECIFIC_DETAILS_CHANGE)

        root.mustcontain('Modified Module Details of <b>MM1009</b>')
        root.mustcontain(self.DETAIL_CHANGES_TARGET_MODULE_PANELS)
        root.mustcontain(self.DETAIL_CHANGES_TARGET_MODULE_OLD_DETAILS)
        root.mustcontain(self.DETAIL_CHANGES_TARGET_MODULE_NEW_DETAILS)
        root.mustcontain(self.DETAIL_CHANGES_TARGET_MODULE_NAME_HEADER)
        root.mustcontain(self.DETAIL_CHANGES_TARGET_MODULE_DESC_HEADER)
        root.mustcontain(self.DETAIL_CHANGES_TARGET_MODULE_MC_HEADER)
        root.mustcontain(self.DETAIL_CHANGES_TARGET_MODULE_PANEL_BODY)
        root.mustcontain(self.DETAIL_CHANGES_TABLE_DETAIL_CHANGE_BUTTON)


    @raises(Exception)
    def test_view_changes_for_invalid_module_response(self):
        '''
            Tests if viewing page displaying module changes
            for a non-existent module should fail.

            Expected view is the custom 404 Not Found page.
        '''
        root = self.test_app.get(self.URL_INVALID_MODULE_CODE)


    def test_view_invalid_changes_for_module_response(self):
        '''
            Tests if viewing page displaying invalid module
            changes for a valid module should fail.

            Expected view is an empty table.
        '''
        root = self.test_app.get(self.URL_INVALID_CHANGE_TYPE)
        assert_equal(root.status, 200)
        root.mustcontain("Modified Mounting of <b>MM1009</b>")

        #Should not contain the restore button (since table is empty)
        assert_false(self.RESTORE_BUTTON_GLYPHICON in root)
