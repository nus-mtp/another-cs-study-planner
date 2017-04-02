'''
    this class tests editMounting.html and links to it
'''

from paste.fixture import TestApp
from nose.tools import assert_equal
from app import APP
from components import session

class TestCode(object):
    '''
        go to individual module view, press edit mounting, check if
        edit mounting is loaded correctly.
    '''
    URL_INDIVIDUAL_MOUNTING = '/individualModuleInfo?code=BT5110&aysem=AY+17%2F18+Sem+1'
    URL_EDIT_MOUNTING = '/editMounting?code=BT5110&aysem=AY+17%2F18+Sem+1'
    EDIT_MOUNTING_BUTTON_FORM_ID = 'edit-mounting-button'
    EDIT_MOUNTING_FORM_ID = 'edit-mounting-form'

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


    def test_mounting_edit_submit_button(self):
        '''
            tests whether the user accessed mounting edit page has a submit
            button and works as intended
        '''
        root = self.test_app.get(self.URL_EDIT_MOUNTING)
        assert_equal(root.status, 200)
        #tests if the correct page is loaded
        root.mustcontain('BT5110')
        root.mustcontain('Module Info')

        submit_edit_mounting_form = root.forms__get()[self.EDIT_MOUNTING_FORM_ID]
        root = submit_edit_mounting_form.submit()
        assert_equal(root.status, 200)

        #redirect back to individual module info page
        root.mustcontain("edited successfully")
