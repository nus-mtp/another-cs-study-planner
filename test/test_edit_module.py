'''
    this class tests editModule.html and links to it
'''
import web
from app import APP, SESSION

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
        '/login', 'componentpys.handlers.login.Login',
        '/verifyLogin', 'components.handlers.login.verifyLogin',
        '/studentEnrollment', 'components.handlers.student_enrollment.StudentEnrollmentQuery'
    )

    URL_MODULE_EDIT = '/editModule'
    URL_MODULE_VIEW = '/viewModule?code=BT5110'
    URL_INDIVIDUAL_MODULE_VIEW = '/individualModuleInfo?code=BT5110&targetAY=AY+17%2F18+Sem+1'

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
            Tests whether user can access a page for showing module edit from module view page.
        '''

        self.b.open(self.URL_MODULE_VIEW)

        self.b.select_form(name=self.EDIT_MODULE_BUTTON_FORM_NAME)
        self.b.submit()

        assert self.b.path == self.URL_MODULE_EDIT

    def test_module_edit_correct_response(self):
        '''
            Tests if the user can access a the correct module edit page
        '''
        self.b.open(self.URL_MODULE_VIEW)

        self.b.select_form(name=self.EDIT_MODULE_BUTTON_FORM_NAME)
        self.b.submit()

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

    def test_module_edit_access_from_individual_module_info(self):
        '''
            tests if the button from individual_module_info page works
            leads to edit module page as intended.
        '''
        self.b.open(self.URL_INDIVIDUAL_MODULE_VIEW)
        self.b.select_form(name=self.EDIT_MODULE_BUTTON_FORM_NAME)
        self.b.submit()

        assert self.b.path == self.URL_MODULE_EDIT
        assert 'Edit: BT5110' in self.b.get_text()
