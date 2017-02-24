
import web
from paste.fixture import TestApp
from nose.tools import assert_equal, raises
from app import APP, SESSION
from components.handlers.module_edit import EditModuleInfo

class TestCode(object):
    '''
        test_edit_module.py tests the app's moduleEdit page
    '''

    URL_MOUNTING_EDIT = '/editMounting'
    URL_INDIVIDUAL_MODULE_VIEW = '/individualModuleInfo?code=BT5110&targetAY=AY+17%2F18+Sem+1'
    EDIT_MOUNTING_BUTTON_NAME = 'edit-mounting-button'
    EDIT_MOUNTING_FORM_NAME = 'edit-mounting-form'
    
    URLS = (
        '/', 'components.handlers.index.Index',
        '/modules', 'components.handlers.module_listing.Modules',
        '/moduleMountingFixed', 'components.handlers.fixed_module_mountings.Fixed',
        '/moduleMountingTentative', 'components.handlers.tentative_module_mountings.Tentative',
        '/viewModule', 'components.handlers.module_overview.ViewMod',
        '/flagAsRemoved/(.*)', 'components.handlers.module_listing.FlagAsRemoved',
        '/flagAsActive/(.*)', 'components.handlers.module_listing.FlagAsActive',
        '/deleteModule/(.*)', 'components.handlers.module_listing.DeleteMod',
        '/editModule', 'components.handlers.module_edit.EditModuleInfo',
        '/editMounting', 'components.handlers.module_edit.EditMountingInfo',
        '/individualModuleInfo', 'components.handlers.module_view_in_ay_sem.IndividualModule',
        '/oversubscribedModules', 'components.handlers.oversub_mod.OversubModule',
        '/login', 'components.handlers.login.Login',
        '/verifyLogin', 'components.handlers.login.verifyLogin',
        '/studentEnrollment', 'components.handlers.student_enrollment.StudentEnrollmentQuery'
    )

    def __init__(self):
        self.b = None

    def setUp(self):
        '''
            sets up the app.py fixure
        '''
        SESSION['id'] = 2
        app = web.application(self.URLS, globals())
        self.b = app.browser()

    def test_mounting_edit_valid_response(self):
        '''
            tests whether user can access mounting edit page through
            mounting view.
        '''
        self.b.open(self.URL_INDIVIDUAL_MODULE_VIEW)
        self.b.select_form(name=self.EDIT_MOUNTING_BUTTON_NAME)
        self.b.submit()
        
        assert self.b.path == self.URL_MOUNTING_EDIT

    def test_mounting_edit_correct_response(self):
        '''
            tests whether user can access correct mounting edit page through
            mounting view.
        '''
        self.b.open(self.URL_INDIVIDUAL_MODULE_VIEW)
        self.b.select_form(name=self.EDIT_MOUNTING_BUTTON_NAME)
        self.b.submit()

        assert 'BT5110' in self.b.get_text()

    def test_mounting_edit_submit_button(self):
        '''
            tests whether the user accessed mounting edit page has a submit
            button and works as intended
        '''

        self.b.open(self.URL_INDIVIDUAL_MODULE_VIEW)
        self.b.select_form(name=self.EDIT_MOUNTING_BUTTON_NAME)
        self.b.submit()

        self.b.select_form(name=self.EDIT_MOUNTING_FORM_NAME)
        self.b.submit()

        text = self.b.get_text()

        assert self.b.path == self.URL_INDIVIDUAL_MODULE_VIEW
        assert 'Mounting info edited sucessfully!' in text
        assert 'BT5110' in text
