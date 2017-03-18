'''
    test_module_specified_class_size.py tests the modules with specified class
    size listing view in specified AY-Semester.
'''
from paste.fixture import TestApp
from nose.tools import assert_equal
from app import APP
from components import session


class TestCode(object):
    '''
        This class runs the test cases to test the modules with specified class
        size listing view in specified AY-Semester.
    '''
    URL_PAGE = '/moduleSpecificSize'
    URL_PAGE_VALID_SUBMIT = 'moduleSpecificSize?sem=AY%2016/17%20Sem%201&' + \
                            'lowerClassSize=2&higherClassSize=90'
    URL_PAGE_INVALID_AYSEM = 'moduleSpecificSize?sem=AY%2016/18%20Sem%201&' + \
                             'lowerClassSize=2&higherClassSize=90'
    URL_PAGE_INVALID_RANGE = 'moduleSpecificSize?sem=AY%2016/17%20Sem%201&' + \
                             'lowerClassSize=31&higherClassSize=30'
    URL_PAGE_INVALID_RANGE_INPUT = 'moduleSpecificSize?sem=AY%2016/17%20Sem%201&' + \
                                   'lowerClassSize=e&higherClassSize=30'

    CONTENT_HEADER = 'Modules with Specific Class Size'
    CONTENT_SUBHEADER = 'Shows all modules with specific class size in specified AY-Semester'

    FORM_QUERY_AY_SEM_AND_CLASS_SIZE = '<form id="mod-class-size-form" ' + \
                                       'action="/moduleSpecificSize" ' + \
                                       'method="post" class="form-inline">'
    FORM_QUERY_AY_SEM_LABEL = '<label for="ay-sem">Find modules in </label>'
    FORM_QUERY_AY_SEM_SELECT = '<select class="form-control" name="sem" required>'
    FORM_QUERY_AY_SEM_OPTION = '<option value="" disabled selected hidden>Please choose a ' + \
                               'target AY-Semester</option>'
    FORM_QUERY_LOW_CLASS_SIZE_LABEL = '<label for="low"> with class size between </label>'
    FORM_QUERY_LOW_CLASS_SIZE_INPUT = '<input type="number" class="form-control" ' + \
                                      'name="lowerClassSize" min="0" max="999" required>'
    FORM_QUERY_HIGH_CLASS_SIZE_LABEL = '<label for="high"> and </label>'
    FORM_QUERY_HIGH_CLASS_SIZE_INPUT = '<input type="number" class="form-control" ' + \
                                       'name="higherClassSize" min="0" max="999" required>'
    FORM_QUERY_SUBMIT_BUTTON = '<input type="submit"  value="Submit" class="btn btn-primary">'

    TABLE_HEADER_TITLE_FOR_PAGE_VALID = 'Modules in AY 16/17 Sem 1 with class size ' + \
                                        'between 2 and 90:'
    TABLE_DATATABLE = '<table class="table display dataTable table-bordered table-hover ' + \
                      'text-center" id="mod-specific-size-table">'
    TABLE_HEADER_CODE = '<th>Module Code</th>'
    TABLE_HEADER_NAME = '<th>Name of Module</th>'
    TABLE_HEADER_QUOTA = '<th>Quota / Class Size</th>'

    SCRIPT_INVALID_AYSEM = "alert('The AY-Semester you specified does not exist!')"
    SCRIPT_INVALID_RANGE = "alert('You have specified an invalid range!')"

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


    def test_mod_specific_class_size_valid_response(self):
        '''
            Tests if user can access the modules with specified class size
            page without request errors.
        '''
        root = self.test_app.get(self.URL_PAGE)

        # checks if HTTP response code is 200 (= OK)
        assert_equal(root.status, 200)


    def test_mod_specific_class_size_valid_submit_response(self):
        '''
            Tests if submitting valid input is successful.
        '''
        root = self.test_app.get(self.URL_PAGE)
        response = root.goto(self.URL_PAGE_VALID_SUBMIT, method='post')

        # Submitting will redirect, test for HTTP response code 303 (= See Other)
        assert_equal(response.status, 303)

        redirected = response.follow()
        # redirected page must have HTTP response code 200 (= OK)
        assert_equal(redirected.status, 200)

        # Presence of these elements indicates that the request
        # direction is correct.

        # Checks if page contains title of Module With Specified Class Size page
        redirected.mustcontain(self.CONTENT_HEADER)
        # Checks if page contains the tables.
        redirected.mustcontain(self.TABLE_HEADER_TITLE_FOR_PAGE_VALID)
        redirected.mustcontain(self.TABLE_DATATABLE)
        redirected.mustcontain(self.TABLE_HEADER_CODE)
        redirected.mustcontain(self.TABLE_HEADER_NAME)
        redirected.mustcontain(self.TABLE_HEADER_QUOTA)


    def test_mod_specific_class_size_valid_url_page_response(self):
        '''
            Tests if the table retrieval from a valid input url entered is
            successful, through "typing" on the address bar, using
            GET method.
        '''
        root = self.test_app.get(self.URL_PAGE)
        response = root.goto(self.URL_PAGE_VALID_SUBMIT, method='get')

        # checks if HTTP response code is 200 (= OK)
        assert_equal(response.status, 200)

        # Presence of these elements indicates that the request
        # direction is correct.

        # Checks if page contains title of Module With Specified Class Size page
        response.mustcontain(self.CONTENT_HEADER)
        # Checks if page contains the tables.
        response.mustcontain(self.TABLE_HEADER_TITLE_FOR_PAGE_VALID)
        response.mustcontain(self.TABLE_DATATABLE)
        response.mustcontain(self.TABLE_HEADER_CODE)
        response.mustcontain(self.TABLE_HEADER_NAME)
        response.mustcontain(self.TABLE_HEADER_QUOTA)


    def test_mod_specific_class_size_invalid_aysem_submit_response(self):
        '''
            Tests if submitting invalid ay_sem input will fail.
        '''
        root = self.test_app.get(self.URL_PAGE)

        response = root.goto(self.URL_PAGE_INVALID_AYSEM, method='post')
        # Submitting will redirect, test for HTTP response code 303 (= See Other)
        assert_equal(response.status, 303)

        redirected = response.follow()
        # redirected page must have HTTP response code 200 (= OK)
        assert_equal(redirected.status, 200)

        # Tests if correct error script is shown.
        redirected.mustcontain(self.SCRIPT_INVALID_AYSEM)


    def test_mod_specific_class_size_invalid_aysem_url_page_response(self):
        '''
            Tests if typing invalid ay_sem in url will fail.
        '''
        root = self.test_app.get(self.URL_PAGE)

        response = root.goto(self.URL_PAGE_INVALID_AYSEM, method='get')

        # checks if HTTP response code is 200 (= OK)
        assert_equal(response.status, 200)

        # Tests if correct error script is shown.
        response.mustcontain(self.SCRIPT_INVALID_AYSEM)


    def test_mod_specific_class_size_invalid_range_submit_response(self):
        '''
            Tests if submitting invalid range input will fail.
        '''
        root = self.test_app.get(self.URL_PAGE)

        response = root.goto(self.URL_PAGE_INVALID_RANGE, method='post')
        # Submitting will redirect, test for HTTP response code 303 (= See Other)
        assert_equal(response.status, 303)

        redirected = response.follow()
        # redirected page must have HTTP response code 200 (= OK)
        assert_equal(redirected.status, 200)

        # Tests if correct error script is shown.
        redirected.mustcontain(self.SCRIPT_INVALID_RANGE)


    def test_mod_specific_class_size_invalid_range_url_page_response(self):
        '''
            Tests if typing invalid range in url will fail.
        '''
        root = self.test_app.get(self.URL_PAGE)

        response = root.goto(self.URL_PAGE_INVALID_RANGE, method='get')

        # redirected page must have HTTP response code 200 (= OK)
        assert_equal(response.status, 200)

        # Tests if correct error script is shown.
        response.mustcontain(self.SCRIPT_INVALID_RANGE)


    def test_mod_specific_class_size_invalid_range_input_url_page_response(self):
        '''
            Tests if typing invalid input (not number) for range in url will fail.
        '''
        root = self.test_app.get(self.URL_PAGE)

        response = root.goto(self.URL_PAGE_INVALID_RANGE_INPUT, method='get')

        # redirected page must have HTTP response code 200 (= OK)
        assert_equal(response.status, 200)

        # Tests if correct error script is shown.
        response.mustcontain(self.SCRIPT_INVALID_RANGE)


    def test_mod_specific_class_size_default(self):
        '''
            Tests if the default page elements are correctly loaded
        '''
        root = self.test_app.get(self.URL_PAGE)

        # Checks the existence of the handler for viewing the page for
        # modules with specified class size
        root.mustcontain(self.CONTENT_HEADER)
        root.mustcontain(self.CONTENT_SUBHEADER)
        root.mustcontain(self.FORM_QUERY_AY_SEM_AND_CLASS_SIZE)
        root.mustcontain(self.FORM_QUERY_AY_SEM_LABEL)
        root.mustcontain(self.FORM_QUERY_AY_SEM_SELECT)
        root.mustcontain(self.FORM_QUERY_AY_SEM_OPTION)
        root.mustcontain(self.FORM_QUERY_LOW_CLASS_SIZE_LABEL)
        root.mustcontain(self.FORM_QUERY_LOW_CLASS_SIZE_INPUT)
        root.mustcontain(self.FORM_QUERY_HIGH_CLASS_SIZE_LABEL)
        root.mustcontain(self.FORM_QUERY_HIGH_CLASS_SIZE_INPUT)
        root.mustcontain(self.FORM_QUERY_SUBMIT_BUTTON)
