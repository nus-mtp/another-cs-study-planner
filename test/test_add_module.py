'''
    test_add_module.py tests the add module page
'''

from paste.fixture import TestApp
from nose.tools import assert_equal, raises
from app import APP
from components import model, session


class TestCode(object):
    '''
        runs tests to test accessability and components in add module page
    '''
    HEADER_TITLE = '<h1 class="text-center"><b>Add Module</b></h1>'
    FORM_LABEL_CODE = '<label for="module-code" class="col-2 col-form-table">' +\
                      'Module Code:</label>'
    FORM_INPUT_CODE = '<input class="form-control" type="text" id="module-code" ' +\
                      'name="code" pattern="[a-zA-Z]{2,3}[0-9]{4}[a-zA-Z]{0,2}" ' +\
                      'placeholder="e.g. CS1231, CS1010J, LSM1302, GEM1004FC" ' +\
                      'required>'
    FORM_LABEL_NAME = '<label for="module-name">Module Name:</label>'

    FORM_INPUT_NAME = '<input class="form-control" type="text" id="module-name" ' +\
                      'name="name" pattern="[a-zA-Z0-9 \-]+$" placeholder="Enter ' +\
                      'Module Name" required>'
    FORM_LABEL_DESCRIPTION = '<label for="module-description">Module ' +\
                             'Description:</label>'
    FORM_TEXTAREA_DESCRIPTION = '<textarea class="form-control" type="text" rows="6"' +\
                                ' id="module-description" name="description" ' +\
                                'placeholder="Enter Module Description" ' +\
                                'required></textarea>'
    FORM_LABEL_MC = '<label for="module-mc">Module Credits:</label>'
    FORM_INPUT_MC = '<input class="form-control" type="number" min="0" max="12" ' +\
                    'id="module-mc" name="mc" placeholder="Number of MCs is between ' +\
                    '0 to 12" required>'
    FORM_INPUT_BUTTON = '<input class="btn btn-lg btn-primary" type="submit" value="Submit">'

    URL_NORMAL = '/addModule'

    TEST_ADD_MODULE_CODE = 'CS5555X'
    TEST_ADD_MODULE_CODE_RELAXED = 'cs5555j'
    TEST_ADD_MODULE_NAME = 'Test Add Module Name Nosetests'
    TEST_ADD_MODULE_DESCRIPTION = 'Test Add Module Description Nosetests'
    TEST_ADD_MODULE_MC = 4

    TEST_ADD_INVALID_MODULE_CODE = 'C$1234'
    TEST_ADD_INVALID_MODULE_NAME = 'I am @n invalid module description.'
    TEST_ADD_INVALID_MODULE_MC_MIN = -1
    TEST_ADD_INVALID_MODULE_MC_MAX = 13

    OUTCOME_SUCCESS_MESSAGE = "alert('Module %s has been added successfully!');"
    OUTCOME_SUCCESS_REDIRECT = "window.location = '/viewModule?code=%s';"

    OUTCOME = '<title>Validating...</title>'
    ERR_MESSAGE = 'Invalid input for module name/code/MCs/description'


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

        # These 3 lines delete any traces of other dummy module
        # data conflicting with the ones used in this test.
        model.delete_module(self.TEST_ADD_MODULE_CODE)
        model.delete_module(self.TEST_ADD_MODULE_CODE_RELAXED.upper())
        model.delete_module(self.TEST_ADD_INVALID_MODULE_CODE)


    def tearDown(self):
        '''
            Tears down 'app.py' fixture and logs out
        '''
        # These 3 lines delete any remaining traces of the modules
        model.delete_module(self.TEST_ADD_MODULE_CODE)
        model.delete_module(self.TEST_ADD_MODULE_CODE_RELAXED.upper())
        model.delete_module(self.TEST_ADD_INVALID_MODULE_CODE)

        session.tear_down(self.test_app)


    def test_add_module_valid_response(self):
        '''
            tests that add module page is accessable
        '''
        root = self.test_app.get(self.URL_NORMAL)
        assert_equal(root.status, 200)


    def test_add_module_page_content(self):
        '''
            tests that add module page contains all required labels and inputs
        '''
        root = self.test_app.get(self.URL_NORMAL)
        root.mustcontain(self.HEADER_TITLE)

        #for code
        root.mustcontain(self.FORM_LABEL_CODE)
        root.mustcontain(self.FORM_INPUT_CODE)
        #for name
        root.mustcontain(self.FORM_LABEL_NAME)
        root.mustcontain(self.FORM_INPUT_NAME)
        #for description
        root.mustcontain(self.FORM_LABEL_DESCRIPTION)
        root.mustcontain(self.FORM_TEXTAREA_DESCRIPTION)
        #for mc
        root.mustcontain(self.FORM_LABEL_MC)
        root.mustcontain(self.FORM_INPUT_MC)
        #checks that submit button exit
        root.mustcontain(self.FORM_INPUT_BUTTON)


    def test_add_module_with_valid_form_inputs(self):
        '''
            Tests that adding a module with all valid inputs should
            be successful.
        '''
        root = self.test_app.get(self.URL_NORMAL)

        addModuleForm = root.forms__get()['addModForm']
        addModuleForm.__setitem__('code', self.TEST_ADD_MODULE_CODE)
        addModuleForm.__setitem__('name', self.TEST_ADD_MODULE_NAME)
        addModuleForm.__setitem__('description', self.TEST_ADD_MODULE_DESCRIPTION)
        addModuleForm.__setitem__('mc', self.TEST_ADD_MODULE_MC)

        response = addModuleForm.submit()
        response.mustcontain((self.OUTCOME_SUCCESS_MESSAGE % self.TEST_ADD_MODULE_CODE))
        response.mustcontain(self.OUTCOME_SUCCESS_REDIRECT % self.TEST_ADD_MODULE_CODE)

        # For reusing data, delete it after it is successfully added.
        model.delete_module(self.TEST_ADD_MODULE_CODE)


    def test_add_module_with_valid_form_inputs_relaxed_module_code(self):
        '''
            Tests that adding a module with all valid inputs should
            be successful, with the module code having smaller case letters.
        '''
        root = self.test_app.get(self.URL_NORMAL)

        addModuleForm = root.forms__get()['addModForm']
        addModuleForm.__setitem__('code', self.TEST_ADD_MODULE_CODE_RELAXED)
        addModuleForm.__setitem__('name', self.TEST_ADD_MODULE_NAME)
        addModuleForm.__setitem__('description', self.TEST_ADD_MODULE_DESCRIPTION)
        addModuleForm.__setitem__('mc', self.TEST_ADD_MODULE_MC)

        response = addModuleForm.submit()
        print(response.status)

        response.mustcontain((self.OUTCOME_SUCCESS_MESSAGE %
                              self.TEST_ADD_MODULE_CODE_RELAXED.upper()))
        response.mustcontain(self.OUTCOME_SUCCESS_REDIRECT %
                              self.TEST_ADD_MODULE_CODE_RELAXED.upper())

        # For reusing data, delete it after it is successfully added.
        model.delete_module(self.TEST_ADD_MODULE_CODE_RELAXED)


    @raises(Exception)
    def test_add_module_with_blank_code_input(self):
        '''
            Tests that adding a module with blank module code
            should fail.
        '''
        root = self.test_app.get(self.URL_NORMAL)

        addModuleForm = root.forms__get()['addModForm']
        addModuleForm.__setitem__('code', None)
        addModuleForm.__setitem__('name', self.TEST_ADD_MODULE_NAME)
        addModuleForm.__setitem__('description', self.TEST_ADD_MODULE_DESCRIPTION)
        addModuleForm.__setitem__('mc', self.TEST_ADD_MODULE_MC)

        response = addModuleForm.submit()


    @raises(Exception)
    def test_add_module_with_blank_name_input(self):
        '''
            Tests that adding a module with blank module name
            should fail.
        '''
        root = self.test_app.get(self.URL_NORMAL)

        addModuleForm = root.forms__get()['addModForm']
        addModuleForm.__setitem__('code', self.TEST_ADD_MODULE_CODE)
        addModuleForm.__setitem__('name', None)
        addModuleForm.__setitem__('description', self.TEST_ADD_MODULE_DESCRIPTION)
        addModuleForm.__setitem__('mc', self.TEST_ADD_MODULE_MC)

        response = addModuleForm.submit()


    @raises(Exception)
    def test_add_module_with_blank_mc_input(self):
        '''
            Tests that adding a module with blank number of MCs
            should fail.
        '''
        root = self.test_app.get(self.URL_NORMAL)

        addModuleForm = root.forms__get()['addModForm']
        addModuleForm.__setitem__('code', self.TEST_ADD_MODULE_CODE)
        addModuleForm.__setitem__('name', self.TEST_ADD_MODULE_NAME)
        addModuleForm.__setitem__('description', self.TEST_ADD_MODULE_DESCRIPTION)
        addModuleForm.__setitem__('mc', None)

        response = addModuleForm.submit()


    # The below test cases are commented out as back-end validations are
    # not implemented yet.
    #
    # @raises(Exception)
    def test_add_module_with_invalid_module_code(self):
         '''
             Tests that adding a module with invalid module code
             should fail.
         '''
         root = self.test_app.get(self.URL_NORMAL)

         addModuleForm = root.forms__get()['addModForm']
         addModuleForm.__setitem__('code', self.TEST_ADD_INVALID_MODULE_CODE)
         addModuleForm.__setitem__('name', self.TEST_ADD_MODULE_NAME)
         addModuleForm.__setitem__('description', self.TEST_ADD_MODULE_DESCRIPTION)
         addModuleForm.__setitem__('mc', self.TEST_ADD_INVALID_MODULE_MC_MIN)

         response = addModuleForm.submit()
         assert_equal(response.status, 200)

         response.mustcontain(self.OUTCOME)
         response.mustcontain(self.ERR_MESSAGE)


    # @raises(Exception)
    # def test_add_module_with_invalid_module_name(self):
    #     '''
    #         Tests that adding a module with invalid module name
    #         should fail.
    #     '''
    #     root = self.test_app.get(self.URL_NORMAL)

    #     addModuleForm = root.forms__get()['addModForm']
    #     addModuleForm.__setitem__('code', self.TEST_ADD_MODULE_CODE)
    #     addModuleForm.__setitem__('name', self.TEST_ADD_INVALID_MODULE_NAME)
    #     addModuleForm.__setitem__('description', self.TEST_ADD_MODULE_DESCRIPTION)
    #     addModuleForm.__setitem__('mc', self.TEST_ADD_INVALID_MODULE_MC_MIN)

    #     response = addModuleForm.submit()


    # @raises(Exception)
    # def test_add_module_with_invalid_mc_lower_boundary(self):
    #     '''
    #         Tests that adding a module with invalid number of MCs
    #         before lower boundary should fail.
    #     '''
    #     root = self.test_app.get(self.URL_NORMAL)

    #     addModuleForm = root.forms__get()['addModForm']
    #     addModuleForm.__setitem__('code', self.TEST_ADD_MODULE_CODE)
    #     addModuleForm.__setitem__('name', self.TEST_ADD_MODULE_NAME)
    #     addModuleForm.__setitem__('description', self.TEST_ADD_MODULE_DESCRIPTION)
    #     addModuleForm.__setitem__('mc', self.TEST_ADD_INVALID_MODULE_MC_MIN)

    #     response = addModuleForm.submit()


    # @raises(Exception)
    # def test_add_module_with_invalid_mc_upper_boundary(self):
    #     '''
    #         Tests that adding a module with invalid number of MCs
    #         beyond upper boundary should fail.
    #     '''
    #     root = self.test_app.get(self.URL_NORMAL)

    #     addModuleForm = root.forms__get()['addModForm']
    #     addModuleForm.__setitem__('code', self.TEST_ADD_MODULE_CODE)
    #     addModuleForm.__setitem__('name', self.TEST_ADD_MODULE_NAME)
    #     addModuleForm.__setitem__('description', self.TEST_ADD_MODULE_DESCRIPTION)
    #     addModuleForm.__setitem__('mc', self.TEST_ADD_INVALID_MODULE_MC_MAX)

    #     response = addModuleForm.submit()
