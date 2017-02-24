
import web
from paste.fixture import TestApp
from nose.tools import assert_equal, raises
from app import APP, SESSION
from components.handlers.module_edit import EditModuleInfo

class TestCode(object):
    '''
        test_edit_module.py tests the app's moduleEdit page
    '''
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
    
    URL_MODULE_EDIT = '/editModule'
    URL_MODULE_VIEW = '/viewModule?code=BT5110'

    EDIT_MODULE_BUTTON_FORM_NAME = 'edit-module-button'
    EDIT_MODULE_FORM_NAME = 'edit-module-form'
    
    def __init__(self):
        self.b = None

    def setUp(self):
        '''
            sets up the app.py fixure
        '''
        SESSION['id'] = 2
        app = web.application(self.URLS, globals())
        self.b = app.browser()
        

    def test_module_edit_valid_response(self):
        '''
            Tests whether user can access correct page for showing module edit from module view page.
        '''
        
        self.b.open(self.URL_MODULE_VIEW)

        self.b.select_form(name=self.EDIT_MODULE_BUTTON_FORM_NAME)
        self.b.submit()

        assert self.b.path == self.URL_MODULE_EDIT
        assert 'Edit: BT5110' in self.b.get_text()

    def test_module_edit_submit_button(self):

        '''
            Tests whether submit button exists and works as intended
        '''
        self.b.open(self.URL_MODULE_VIEW)

        self.b.select_form(name=self.EDIT_MODULE_BUTTON_FORM_NAME)
        self.b.submit()

        self.b.select_form(name=self.EDIT_MODULE_FORM_NAME)
        self.b.submit()
        
        assert self.b.path == self.URL_MODULE_VIEW
        assert 'BT5110' in self.b.get_text()
        
        
















        
