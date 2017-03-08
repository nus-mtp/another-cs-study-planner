'''
    this class tests editMounting.html and links to it
'''

from paste.fixture import TestApp
from nose.tools import assert_equal
import app
from components import session

class TestCode(object):
    '''
        go to individual module view, press edit mounting, check if
        edit mounting is loaded correctly.
    '''
    URL_INDIVIDUAL_MOUNTING = '/individualModuleInfo?code=BT5110&targetAY=AY+17%2F18+Sem+1'
    EDIT_MOUNTING_BUTTON_FORM_ID = 'edit-mounting-button'
    EDIT_MOUNTING_FORM_ID = 'edit-mounting-form'

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

    def test_access_module_mounting_edit(self):
        '''
            Tests if edit mounting button on mounting page works as intended
        '''
        root = self.test_app.get(self.URL_INDIVIDUAL_MOUNTING)
        assert_equal(root.status, 200)
        #tests if the correct page is loaded
        root.mustcontain('BT5110')
        root.mustcontain('Module Info')

        edit_mounting_button = root.forms__get()[self.EDIT_MOUNTING_BUTTON_FORM_ID]
        response = edit_mounting_button.submit()

        assert_equal(response.status, 200)

        response.mustcontain('BT5110')
        response.mustcontain('Mounting Status:')

    def test_mounting_edit_submit_button(self):
        '''
            tests whether the user accessed mounting edit page has a submit
            button and works as intended
        '''
        root = self.test_app.get(self.URL_INDIVIDUAL_MOUNTING)
        assert_equal(root.status, 200)
        #tests if the correct page is loaded
        root.mustcontain('BT5110')
        root.mustcontain('Module Info')

        edit_mounting_button = root.forms__get()[self.EDIT_MOUNTING_BUTTON_FORM_ID]
        response = edit_mounting_button.submit()

        assert_equal(response.status, 200)

        response.mustcontain('BT5110')
        response.mustcontain('Mounting Status:')

        submit_edit_mounting_form = response.forms__get()[self.EDIT_MOUNTING_FORM_ID]
        response = submit_edit_mounting_form.submit()
        assert_equal(response.status, 200)

        #redirect back to individual module info page
        root.mustcontain("Module Info for")
        root.mustcontain("BT5110")

    def test_contains_overlapping_modules_table(self):
        '''
            tests if the overlapping modules table exists
        '''
        root = self.test_app.get(self.URL_INDIVIDUAL_MOUNTING)
        assert_equal(root.status, 200)
        #tests if the correct page is loaded
        root.mustcontain('BT5110')
        root.mustcontain('Module Info')

        edit_mounting_button = root.forms__get()[self.EDIT_MOUNTING_BUTTON_FORM_ID]
        response = edit_mounting_button.submit()

        assert_equal(response.status, 200)

        response.mustcontain(self.CONTENT_OVERLAPPING_MODULES_TABLE)
