'''
    test_edit_all_mountings_and_quotas.py test the page view of Edit All Mountings and Quotas
'''
from paste.fixture import TestApp
from nose.tools import assert_equal
from app import APP
from components import session


class TestCode(object):
    '''
        This class runs the test cases to test Edit All Mountings and Quotas page
    '''
    PAGE_URL = '/editAll'

    SELECT_MODULE_LABEL = 'Select module(s) to edit:'
    SELECT_MODULE_INPUT = '<input type="text" id="select-mod-to-edit" class="typeahead" ' +\
                          'data-provide="typeahead"' +\
                          ' placeholder="Enter module code or name here"'

    TABLE_HEADER_CODE = '<th>Code</th>'
    TABLE_HEADER_NAME = '<th>Name</th>'
    TABLE_HEADER_MOUNTED_IN_SEM1 = '<th>Mounted In Sem 1</th>'
    TABLE_HEADER_SEM1_QUOTA = '<th>Sem 1 Quota</th>'
    TABLE_HEADER_MOUNTED_IN_SEM2 = '<th>Mounted In Sem 2</th>'
    TABLE_HEADER_SEM2_QUOTA = '<th>Sem 2 Quota</th>'
    TABLE_HEADER_REMOVE = '<th>Remove</th>'
    TABLE_NO_MODULES = 'No modules selected'

    BUTTON_SAVE_CHANGES = '<button type="submit" class="btn btn-primary edit-all-bottom-button" ' +\
                          'data-toggle="tooltip" data-placement="bottom" title="Save changes" '
    BUTTON_RESET_TABLE = '<button type="button" id="edit-all-reset-button" ' +\
                         'class="btn btn-primary edit-all-bottom-button" ' +\
                         'data-toggle="tooltip" data-placement="bottom" title="Reset table" '

    OUTCOME_TITLE = '<title>Validating...</title>'
    OUTCOME_SUCCESS_MESSAGE = 'Modules have been edited successfully!'
    OUTCOME_FAILURE_MESSAGE = 'Error: Failed to edit modules'


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


    def test_valid_response(self):
        '''
            Tests if user can access the page without request errors.
        '''
        root = self.test_app.get(self.PAGE_URL)

        # checks if HTTP response code is 200 (= OK)
        assert_equal(root.status, 200)


    def test_edit_all_mountings_and_quotas_page_view(self):
        '''
            Tests if a table displaying modules to be edited exist
        '''
        root = self.test_app.get(self.PAGE_URL)

        # Checks the existence of the handler for viewing fixed mounting plan
        root.mustcontain(self.SELECT_MODULE_LABEL)
        root.mustcontain(self.SELECT_MODULE_INPUT)
        root.mustcontain(self.TABLE_HEADER_CODE)
        root.mustcontain(self.TABLE_HEADER_NAME)
        root.mustcontain(self.TABLE_HEADER_MOUNTED_IN_SEM1)
        root.mustcontain(self.TABLE_HEADER_SEM1_QUOTA)
        root.mustcontain(self.TABLE_HEADER_MOUNTED_IN_SEM2)
        root.mustcontain(self.TABLE_HEADER_SEM2_QUOTA)
        root.mustcontain(self.TABLE_HEADER_REMOVE)
        root.mustcontain(self.BUTTON_SAVE_CHANGES)
        root.mustcontain(self.BUTTON_RESET_TABLE)


    def test_submit_edit_all_form(self):
        '''
            Tests that the Edit All form can be submitted and the correct outcome message is shown
        '''
        root = self.test_app.get(self.PAGE_URL)

        editAllForm = root.forms__get()['edit-all-form']
        editAllForm.__setitem__('BT5110_isEdited', "True")
        editAllForm.__setitem__('BT5110_Sem1Quota', 60)  # valid quota

        response = editAllForm.submit()
        assert_equal(response.status, 200)

        response.mustcontain(self.OUTCOME_TITLE)
        response.mustcontain(self.OUTCOME_SUCCESS_MESSAGE)

        root = self.test_app.get(self.PAGE_URL)

        editAllForm = root.forms__get()['edit-all-form']
        editAllForm.__setitem__('BT5110_isEdited', "True")
        editAllForm.__setitem__('BT5110_Sem1Quota', "aaa")  # invalid quota

        response = editAllForm.submit()
        assert_equal(response.status, 200)

        response.mustcontain(self.OUTCOME_TITLE)
        response.mustcontain(self.OUTCOME_FAILURE_MESSAGE)


    def test_reset_edit_all(self):
        '''
            Tests that the Edit All table can be reset
        '''
        root = self.test_app.get(self.PAGE_URL)

        response = root.clickbutton(buttonid='edit-all-reset-button')
        response.mustcontain(self.TABLE_NO_MODULES)
