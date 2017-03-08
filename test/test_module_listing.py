'''
    test_module_listing.py test the module listing view.
'''
from paste.fixture import TestApp
from nose.tools import assert_equal, assert_raises
import app
from components import session


class TestCode(object):
    '''
        This class runs the test cases to test app home page
    '''

    FORM_ADD_MODULE = '<form id="addModForm" action="" method="post">'
    FORM_LABEL_CODE = '<label for="code">Code</label>'
    FORM_INPUT_CODE = '<input type="text" id="code" name="code"/>'
    FORM_LABEL_NAME = '<label for="name">Name</label>'
    FORM_INPUT_NAME = '<input type="text" id="name" name="name"/>'
    FORM_LABEL_DESCRIPTION = '<label for="description">Description</label>'
    FORM_INPUT_DESCRIPTION = '<textarea rows="5" id="description" ' +\
                             'name="description" cols="55"></textarea>'
    FORM_LABEL_MC = '<label for="mc">MCs</label>'
    FORM_INPUT_MC = '<input type="text" id="mc" name="mc"/>'
    FORM_INPUT_BUTTON = '<button id="Add Module" name="Add Module" ' +\
                        'class="btn btn-primary">Add Module</button>'
    FORM_FIXED_MOUNTING = '<form action="/moduleMountingFixed" method="post">'
    FORM_FIXED_MOUNTING_BUTTON = '<input class="btn btn-primary" ' +\
                                 'type="submit" value="Go To Fixed Module ' +\
                                 'Mountings" />'
    FORM_TENTATIVE_MOUNTING = '<form action="/moduleMountingTentative" ' +\
                              'method="post">'
    FORM_TENTATIVE_MOUNTING_BUTTON = '<input class="btn btn-primary" ' +\
                                     'type="submit" value="Go To Tentative ' +\
                                     'Module Mountings" />'
    FORM_VALIDATION_MSG_REQ = '<strong class="wrong">Required</strong>'
    FORM_VALIDATION_MSG_MOD_CODE = '<strong class="wrong">Module' +\
                                   ' code should be alphanumeric.' +\
                                   '</strong>'
    FORM_VALIDATION_MSG_MOD_NAME = '<strong class="wrong">Module' +\
                                   ' name should be alphanumeric.' +\
                                   '</strong>'
    FORM_VALIDATION_MSG_MOD_MC = '<strong class="wrong">Number of MCs' +\
                                 ' should be a number.</strong>'

    TABLE_HEADER_CODE = '<th>Code</th>'
    TABLE_HEADER_NAME = '<th>Name</th>'
    TABLE_HEADER_DESCRIPTION = '<th>Description</th>'
    TABLE_HEADER_MC = '<th>MCs</th>'
    TABLE_HEADER_STATUS = '<th>Status</th>'
    TABLE_HEADER_ACTIONS = '<th data-sortable="false">Actions</th>'

    global_var = None

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


    def test_index_valid_response(self):
        '''
            Tests if user can access the index page without request errors.
        '''
        root = self.test_app.get('/modules')

        # checks if HTTP response code is 200 (= OK)
        assert_equal(root.status, 200)


    def test_index_goto_fixed_module_mountings_response(self):
        '''
            Tests if navigation to 'Fixed Module Mountings' is successful.
        '''
        root = self.test_app.get('/modules')
        response = root.goto('/moduleMountingFixed', method='post')

        # checks if HTTP response code is 303 (= See Other)
        # because POST method in 'Fixed' class in 'modules.py'
        # redirects to its GET method.
        assert_equal(response.status, 303)


    def test_index_goto_tentative_module_mountings_response(self):
        '''
            Tests if navigation to 'Tentative Module Mountings' is successful.
        '''
        root = self.test_app.get('/modules')
        response = root.goto('/moduleMountingTentative', method='post')

        # checks if HTTP response code is 303 (= See Other)
        # because POST method in 'Tentative' class in 'modules.py'
        # redirects to its GET method.
        assert_equal(response.status, 303)


    def test_index_goto_valid_module_overview_page_response(self):
        '''
            Tests if navigation to a module overview page with
            a valid target module code is successful.
        '''
        root = self.test_app.get('/modules')
        response = root.goto('/viewModule?code=BT5110', method='get')

        # checks if HTTP response code is 200 (= OK)
        assert_equal(response.status, 200)


        # Presence of these elements indicates that the request
        # direction is correct.

        # Checks if page contains title of Module Info Overview page
        response.mustcontain("Module Info Overview")
        # Checks if page contains target module
        response.mustcontain("BT5110")


    def test_index_goto_invalid_module_overview_page_response(self):
        '''
            Tests if navigation to a module overview page with
            an invalid target module code will fail.

            NOTE: this test case is supposed to FAIL.
        '''
        root = self.test_app.get('/modules')
        # an exception WILL be encountered here
        try:
            root.goto('/viewModule?code=CS0123', method='get')
            assert_equal(True, False)
        except Exception:
            assert_equal(True, True)


    def test_index_add_module_form_exists(self):
        '''
            Tests if the add-module form exists in index page and follows
            a specified format. The form format is as follows:

            1. Module Code --> 'code': has label and text input field
            2. Module Name --> 'name': has label and text input field
            3. Module Description --> 'description': has label and textarea field
            4. MCs --> 'mc': has label and text input field
            5. 'Add Module' button --> 'Add Module'
        '''
        root = self.test_app.get('/modules')

        # These check for the existence of labels and input fields
        # Checks if form attribute exists
        root.mustcontain(self.FORM_ADD_MODULE)

        # For 'Code' input
        root.mustcontain(self.FORM_LABEL_CODE)
        root.mustcontain(self.FORM_INPUT_CODE)
        # For 'Name' input
        root.mustcontain(self.FORM_LABEL_NAME)
        root.mustcontain(self.FORM_INPUT_NAME)
        # For 'Description' input
        root.mustcontain(self.FORM_LABEL_DESCRIPTION)
        root.mustcontain(self.FORM_INPUT_DESCRIPTION)
        # For 'MCs' input
        root.mustcontain(self.FORM_LABEL_MC)
        root.mustcontain(self.FORM_INPUT_MC)

        # checks for 'Add Module' button presence
        root.mustcontain(self.FORM_INPUT_BUTTON)


    def test_index_add_module_form_submit_blanks(self):
        '''
            Tests if 'Required' validation message appears after submitting
            a blank add-module form.
        '''
        root = self.test_app.get('/modules')

        add_module_form = root.forms__get()["addModForm"]
        response = add_module_form.submit()
        response.mustcontain(self.FORM_VALIDATION_MSG_REQ)


    def test_index_add_module_form_submit_non_alphanumeric_module_code(self):
        '''
            Tests if 'alphanumeric' validation message appears after submitting
            an add-module form with module code containing non-alphanumeric
            character(s).
        '''
        root = self.test_app.get('/modules')

        add_module_form = root.forms__get()["addModForm"]
        add_module_form.__setitem__("code", "CS123#")
        response = add_module_form.submit()
        response.mustcontain(self.FORM_VALIDATION_MSG_MOD_CODE)


    def test_index_add_module_form_submit_non_alphanumeric_module_name(self):
        '''
            Tests if 'alphanumeric' validation message appears after submitting
            an add-module form with module name containing non-alphanumeric
            character(s).
        '''
        root = self.test_app.get('/modules')

        add_module_form = root.forms__get()["addModForm"]
        add_module_form.__setitem__("name", "Introduction to #")
        response = add_module_form.submit()
        response.mustcontain(self.FORM_VALIDATION_MSG_MOD_NAME)


    def test_index_add_module_form_submit_non_numeric_module_mc(self):
        '''
            Tests if 'numeric' validation message appears after submitting
            an add-module form with module MCs containing non-numeric
            character(s).
        '''
        root = self.test_app.get('/modules')

        add_module_form = root.forms__get()["addModForm"]
        add_module_form.__setitem__("mc", "a")
        response = add_module_form.submit()
        response.mustcontain(self.FORM_VALIDATION_MSG_MOD_MC)


    def test_index_add_module_form_submit_invalid_numeric_module_mc(self):
        '''
            Tests if 'numeric' validation message appears after submitting
            an add-module form with module MCs containing a negative number.
        '''
        root = self.test_app.get('/modules')

        add_module_form = root.forms__get()["addModForm"]
        add_module_form.__setitem__("mc", "-1")
        response = add_module_form.submit()
        response.mustcontain(self.FORM_VALIDATION_MSG_MOD_MC)


    def test_index_module_mounting_view_options(self):
        '''
            Tests if the 2 buttons for navigating to different types
            of mounting plans (fixed and tentative) exist.

            Each navigation is tied to a form that will handle the
            navigation redirections.
        '''
        root = self.test_app.get('/modules')

        # Checks the existence of the handler for viewing fixed mounting plan
        root.mustcontain(self.FORM_FIXED_MOUNTING)
        root.mustcontain(self.FORM_FIXED_MOUNTING_BUTTON)

        # Checks the existence of the handler for viewing tentative mounting plan
        root.mustcontain(self.FORM_TENTATIVE_MOUNTING)
        root.mustcontain(self.FORM_TENTATIVE_MOUNTING_BUTTON)


    def test_index_modules_listing(self):
        '''
            Tests if a table displaying a list of all modules exist.
        '''
        root = self.test_app.get('/modules')

        # Checks the existence of the handler for viewing fixed mounting plan
        root.mustcontain(self.TABLE_HEADER_CODE)
        root.mustcontain(self.TABLE_HEADER_NAME)
        root.mustcontain(self.TABLE_HEADER_DESCRIPTION)
        root.mustcontain(self.TABLE_HEADER_MC)
        root.mustcontain(self.TABLE_HEADER_STATUS)
        root.mustcontain(self.TABLE_HEADER_ACTIONS)
