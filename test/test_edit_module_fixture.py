'''
    this class tests editModule.html and links to it
'''

from paste.fixture import TestApp
from nose.tools import assert_equal
from app import APP, SESSION

class TestCode(object):
    '''
        go to pages linking to edit, press edit, check if edit is loaded correctly
    '''

    URL_MODULE_VIEW = '/viewModule?code=BT5110'
    URL_INDIVIDUAL_MODULE_VIEW = '/individualModuleInfo?code=BT5110&targetAY=AY+17%2F18+Sem+1'

    EDIT_MODULE_BUTTON_FORM_NAME = 'edit-module-button'
    EDIT_MODULE_FORM_NAME = 'edit-module-form'

    def __init__(self):
        self.middleware = None
        self.test_app = None

    def setUp(self):
        '''
            sets up fixture, along with user account states.
        '''
        self.middleware = []
        self.test_app = TestApp(APP.wsgifunc(*self.middleware))
        SESSION['id'] = 2

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
