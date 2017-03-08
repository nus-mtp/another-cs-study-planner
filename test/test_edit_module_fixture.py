'''
    this class tests editModule.html and links to it
'''

from paste.fixture import TestApp
from nose.tools import assert_equal
import app
from components import session

class TestCode(object):
    '''
        go to pages linking to edit, press edit, check if edit is loaded correctly
    '''

    URL_MODULE_VIEW = '/viewModule?code=BT5110'
    URL_INDIVIDUAL_MODULE_VIEW = '/individualModuleInfo?code=BT5110&targetAY=AY+17%2F18+Sem+1'

    EDIT_MODULE_BUTTON_FORM_NAME = 'edit-module-button'
    EDIT_MODULE_FORM_NAME = 'edit-module-form'

    CONTENT_OVERLAPPING_MODULES_TABLE = '<table id="common-module-table" ' +\
                                        'class="table table-bordered table-hover display ' +\
                                        'dataTable">'

    def __init__(self):
        self.middleware = None
        self.test_app = None

    def setUp(self):
        '''
            Sets up the 'app.py' fixture
        '''
        self.middleware = []
        app.APP.add_processor(app.web.loadhook(app.session_hook))
        self.test_app = TestApp(app.APP.wsgifunc(*self.middleware))
        session.set_up(self.test_app)


    def tearDown(self):
        '''
            Tears down 'app.py' fixture and logs out
        '''
        session.tear_down(self.test_app)


    def test_module_edit_correct_response(self):
        '''
            Tests whether user can access a page for showing module edit from module view page.
        '''
        root = self.test_app.get(self.URL_MODULE_VIEW)
        assert_equal(root.status, 200)

        submit_button = root.forms__get()[self.EDIT_MODULE_BUTTON_FORM_NAME]
        response = submit_button.submit()

        assert_equal(response.status, 200)

        response.mustcontain('Edit: BT5110')

    def test_module_edit_submit_response(self):
        '''
            Tests whether pressing submit in edit module page results to the correct
            response.
        '''
        root = self.test_app.get(self.URL_MODULE_VIEW)
        assert_equal(root.status, 200)

        submit_button = root.forms__get()[self.EDIT_MODULE_BUTTON_FORM_NAME]
        goto_edit_response = submit_button.submit()

        assert_equal(goto_edit_response.status, 200)
        #successfully reached editmodule page
        goto_edit_response.mustcontain('Edit: BT5110')

        edit_submit_button = goto_edit_response.forms__get()[self.EDIT_MODULE_FORM_NAME]
        submit_edit_response = edit_submit_button.submit()
        #redirect back to module view
        assert_equal(submit_edit_response.status, 200)

        #successfully reached original moduleview page
        root.mustcontain("Module Info Overview")
        root.mustcontain("BT5110")


    def test_access_module_edit_from_individual_module_view(self):
        '''
            Tests if the edit module button on mounting page works as intended
        '''
        root = self.test_app.get(self.URL_INDIVIDUAL_MODULE_VIEW)
        assert_equal(root.status, 200)
        submit_button = root.forms__get()[self.EDIT_MODULE_BUTTON_FORM_NAME]
        response = submit_button.submit()

        assert_equal(response.status, 200)

        response.mustcontain('Edit: BT5110')

    def test_contains_overlapping_modules_table(self):
        '''
            Tests if overlapping modules table exist
        '''
        root = self.test_app.get(self.URL_INDIVIDUAL_MODULE_VIEW)
        assert_equal(root.status, 200)
        submit_button = root.forms__get()[self.EDIT_MODULE_BUTTON_FORM_NAME]
        response = submit_button.submit()

        assert_equal(response.status, 200)

        response.mustcontain(self.CONTENT_OVERLAPPING_MODULES_TABLE)
