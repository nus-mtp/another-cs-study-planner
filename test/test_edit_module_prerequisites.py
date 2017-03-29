'''
    this class tests the page for editing module prerequisites.
'''

from paste.fixture import TestApp
from nose.tools import assert_equal, raises
from app import APP
from components import session
from components.handlers.module_edit_prerequisites import EditModulePrerequisites

class TestCode(object):
    '''
        In this test suite, we test whether buttons are present, and if
        any links or buttons (that are not invoking any JavaScript functions) are working.

        Some features/functions here cannot be tested using the nose framework (such as
        the add-unit and save-changes buttons, since they invoke JavaScript functions and
        are not actions of firing requests at the app).
    '''
    URL_EDIT_MODULE_PREREQ_SPECIFIC_VALID = '/editModulePrerequisites?code=BT5110'
    URL_EDIT_MODULE_PREREQ_SPECIFIC_INVALID_CODE = '/editModulePrerequisites?code=CS0123'

    EDIT_MODULE_TITLE = '<h1 class="text-center"><b>Edit Prerequisites for ' +\
                        '<u id="module-code">BT5110</u></b></h1>'
    EDIT_MODULE_PREREQUISITES_FORM = '<form id="prerequisites-form" action="#" method="post">'
    EDIT_MODULE_PREREQUISITES_TABLE_INTERFACE = '<table class="table table-hover text-center" ' +\
                                                'id="edit-prereq-interface">'
    EDIT_MODULE_PREREQUISITES_ADD_UNIT_BUTTON = '<button class="btn btn-lg btn-primary" ' +\
                                                'id="add-prereq-unit" ' +\
                                                'data-toggle="tooltip" data-placement="top" ' +\
                                                'title="Add Prerequisite Unit" ' +\
                                                'onclick="addPrereqUnit()"><span ' +\
                                                'class="glyphicon glyphicon-plus">' +\
                                                '</span></button>'
    EDIT_MODULE_PREREQUISITES_SAVE_BUTTON = '<button class="btn btn-lg btn-primary" ' +\
                                            'id="save-changes" ' +\
                                            'data-toggle="tooltip" data-placement="top" ' +\
                                            'title="Save Changes" onclick="saveChanges()">' +\
                                            '<span class="glyphicon glyphicon-floppy-disk">' +\
                                            '</span></button>'
    EDIT_MODULE_PREREQUISITES_REVERT_BUTTON = '<a class="btn btn-lg btn-primary" ' +\
                                              'id="revert-changes" ' +\
                                              'data-toggle="tooltip" data-placement="top" ' +\
                                              'title="Revert All Changes" ' +\
                                              'href="/editModulePrerequisites?code=BT5110">' +\
                                              '<span class="glyphicon glyphicon-refresh">' +\
                                              '</span></a>'


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


    def test_module_prereq_edit_direct_access_correct_response(self):
        '''
            Tests whether user can access a page for showing
            edit-module-prerequisites page directly through a valid URL.
        '''
        root = self.test_app.get(self.URL_EDIT_MODULE_PREREQ_SPECIFIC_VALID)
        assert_equal(root.status, 200)

        root.mustcontain(self.EDIT_MODULE_TITLE)
        root.mustcontain(self.EDIT_MODULE_PREREQUISITES_FORM)
        root.mustcontain(self.EDIT_MODULE_PREREQUISITES_TABLE_INTERFACE)
        root.mustcontain(self.EDIT_MODULE_PREREQUISITES_ADD_UNIT_BUTTON)
        root.mustcontain(self.EDIT_MODULE_PREREQUISITES_SAVE_BUTTON)
        root.mustcontain(self.EDIT_MODULE_PREREQUISITES_REVERT_BUTTON)


    @raises(Exception)
    def test_module_prereq_edit_direct_access_invalid_code_url(self):
        '''
            Tests whether user will fail to access edit-module-prerequisites
            page if an invalid URL (invalid module code) is used.
        '''
        root = self.test_app.get(self.URL_EDIT_MODULE_PREREQ_SPECIFIC_INVALID_CODE)


    def test_module_prereq_edit_revert_option_button(self):
        '''
            Tests whether the revert-changes button works.
        '''
        root = self.test_app.get(self.URL_EDIT_MODULE_PREREQ_SPECIFIC_VALID)
        response = root.click(linkid="revert-changes")

        assert_equal(response.status, 200)

        response.mustcontain(self.EDIT_MODULE_TITLE)
        response.mustcontain(self.EDIT_MODULE_PREREQUISITES_FORM)
        response.mustcontain(self.EDIT_MODULE_PREREQUISITES_TABLE_INTERFACE)
        response.mustcontain(self.EDIT_MODULE_PREREQUISITES_ADD_UNIT_BUTTON)
        response.mustcontain(self.EDIT_MODULE_PREREQUISITES_SAVE_BUTTON)
        response.mustcontain(self.EDIT_MODULE_PREREQUISITES_REVERT_BUTTON)
