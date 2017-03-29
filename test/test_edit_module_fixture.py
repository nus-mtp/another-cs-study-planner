'''
    this class tests editModule.html and links to it
'''

from paste.fixture import TestApp
from nose.tools import assert_equal, raises
from app import APP
from components import session

class TestCode(object):
    '''
        go to pages linking to edit, press edit, check if edit is loaded correctly
    '''

    URL_MODULE_VIEW = '/viewModule?code=BT5110'
    URL_INDIVIDUAL_MODULE_VIEW = '/individualModuleInfo?code=BT5110&aysem=AY+17%2F18+Sem+1'
    URL_EDIT_MODULE_SPECIFIC_VALID = '/editMounting?code=BT5110&aysem=AY+17%2F18+Sem+1'
    URL_EDIT_MODULE_SPECIFIC_INVALID_CODE = '/editMounting?code=CS0123&aysem=AY+17%2F18+Sem+1'
    URL_EDIT_MODULE_SPECIFIC_INVALID_AY_SEM = '/editMounting?code=BT5110&aysem=AY+17%2F19+Sem+1'

    EDIT_MODULE_SPECIFIC_BUTTON_FORM_NAME = 'edit-module-button'
    EDIT_MODULE_SPECIFIC_FORM_NAME = 'edit-module-form'

    EDIT_MODULE_TITLE = ' <h1 class="title text-center">Edit <b>General Information</b>'+\
                        ' For <b>BT5110</b></h1>'
    EDIT_MODULE_SPECIFIC_TITLE = ' <h1 class="title text-center">Edit <b>BT5110</b> ' +\
                                 'For <b>AY 17/18 Sem 1</b></h1>'
    EDIT_MODULE_PREREQUISITES_BUTTON = '<a class="btn btn-primary" ' +\
                                       'href="/editModulePrerequisites?code=BT5110" ' +\
                                       'target="_blank">Edit Prerequisites</a>'
    TESTING_MODULE = 'BT5110'

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


    def test_access_module_edit_from_module_listing(self):
        '''
            Tests whether user can access a page for showing module edit from module view page.
        '''
        root = self.test_app.get(self.URL_MODULE_VIEW)
        assert_equal(root.status, 200)

        submit_button = root.forms__get()[self.EDIT_MODULE_SPECIFIC_BUTTON_FORM_NAME]
        response = submit_button.submit()

        assert_equal(response.status, 200)

        response.mustcontain(self.EDIT_MODULE_TITLE)
        response.mustcontain(self.EDIT_MODULE_PREREQUISITES_BUTTON)


    def test_access_module_edit_from_individual_module_view(self):
        '''
            Tests whether user can access a page for showing module edit from individual
            module view page.
        '''
        root = self.test_app.get(self.URL_INDIVIDUAL_MODULE_VIEW)
        assert_equal(root.status, 200)
        submit_button = root.forms__get()[self.EDIT_MODULE_SPECIFIC_BUTTON_FORM_NAME]
        response = submit_button.submit()

        assert_equal(response.status, 200)

        response.mustcontain(self.EDIT_MODULE_TITLE)


    def test_module_edit_direct_access_correct_response(self):
        '''
            Tests whether user can access a page for showing module edit directly
            through a valid URL.
        '''
        root = self.test_app.get(self.URL_EDIT_MODULE_SPECIFIC_VALID)
        assert_equal(root.status, 200)

        root.mustcontain(self.EDIT_MODULE_SPECIFIC_TITLE)


    @raises(Exception)
    def test_module_edit_direct_access_invalid_code_url(self):
        '''
            Tests whether user will fail to access edit-module
            page if an invalid URL (invalid module code) is used.
        '''
        root = self.test_app.get(self.URL_EDIT_MODULE_SPECIFIC_INVALID_CODE)


    @raises(Exception)
    def test_module_edit_direct_access_invalid_aysem_url(self):
        '''
            Tests whether user will fail to access edit-module
            page if an invalid URL (invalid AY-Semester) is used.
        '''
        root = self.test_app.get(self.URL_EDIT_MODULE_SPECIFIC_INVALID_AY_SEM)


    def test_module_edit_submit_response(self):
        '''
            Tests whether pressing submit in edit module page results to the correct
            response.
        '''
        root = self.test_app.get(self.URL_MODULE_VIEW)
        assert_equal(root.status, 200)

        submit_button = root.forms__get()[self.EDIT_MODULE_SPECIFIC_BUTTON_FORM_NAME]
        goto_edit_response = submit_button.submit()

        assert_equal(goto_edit_response.status, 200)
        #successfully reached editmodule page
        goto_edit_response.mustcontain(self.EDIT_MODULE_TITLE)

        edit_submit_button = goto_edit_response.forms__get()[self.EDIT_MODULE_SPECIFIC_FORM_NAME]
        submit_edit_response = edit_submit_button.submit()
        #redirect back to module view
        assert_equal(submit_edit_response.status, 200)

        #successfully reached original moduleview page
        root.mustcontain("Module Info Overview")
        root.mustcontain(self.TESTING_MODULE)


    def test_module_edit_submit_invalid_quota(self):
        '''
            Tests whether submitting the edit-module form with invalid
            inputs will fail.
        '''
        root = self.test_app.get(self.URL_EDIT_MODULE_SPECIFIC_VALID)
        edit_module_mounting_form = root.forms__get()["edit-mounting-form"]
        edit_module_mounting_form.__setitem__("quota", -1)
        response = edit_module_mounting_form.submit()

        assert_equal(response.status, 200)
        response.mustcontain("alert('Error: Failed to edit module.');")
