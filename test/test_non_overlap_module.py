'''
    test_non_overlap_module.py tests the page views for
    viewing module pairs which no one takes together

    Firstly, we specify a target URL for conducting UI testing.

    Then, we proceed to test the following things:
    #1 Accessing the target page should be possible (i.e. response code should be 200 OK).
    #2 The necessary HTML elements are contained in the page view for target page.

'''


from paste.fixture import TestApp
from nose.tools import assert_equal
from app import APP
from components import session


class TestCode(object):
    '''
        This class contains methods that tests the page views inside
        the target page.
    '''


    URL_NON_OVERLAP_MODS = '/nonOverlappingModules'
    URL_NON_OVERLAP_MODS_16_17_SEM2 = '/nonOverlappingModules?sem=AY%2016/17%20Sem%202'
    URL_NON_OVERLAP_MODS_INVALID = '/nonOverlappingModules?sem=AY%2016/18%20Sem%202'
    CURRENT_SEM = 'AY 16/17 Sem 1'
    DEFAULT_TITLE = 'Non-Overlapping Modules for AY 16/17 Sem 1'
    TEXT = '<p class="text-center" data-toggle="tooltip" data-placement="bottom" '+\
           'title="By default, these pairs are shown for the current AY-Semester.">Shows all module pairs '+\
           'which no student takes together in a particular semester.</p>'
    FORM = '<form id="ay-form" class="form-inline" action="/nonOverlappingModules" method="post">'
    SELECT_LABEL = '<label for="ay-sem">Select AY-Sem:</label>'
    SELECT_ELEMENT = '<select class="form-control" name="sem">'
    TABLE_HEADER_MODULE_CODE_ONE = '<th>Module 1</th>'
    TABLE_HEADER_MODULE_NAME_ONE = '<th>Name of Module 1</th>'
    TABLE_HEADER_MODULE_CODE_TWO = '<th>Module 2</th>'
    TABLE_HEADER_MODULE_NAME_TWO = '<th>Name of Module 2</th>'

    REDIRECT_CHANGED_CONTENT = 'Non-Overlapping Modules for AY 16/17 Sem 2'
    VALIDATING_TITLE = 'Validating...'
    SCRIPT_REDIRECT_TO_DEFAULT = "window.location = '/nonOverlappingModules'"
    SCRIPT_ERROR_MESSAGE = "alert('The AY-Semester you specified does not exist!');"
    def __init__(self):
        self.middleware = None
        self.test_app = None


    def  setUp(self):
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

    def test_non_overlapping_modules_valid_response(self):
        '''
            Tests whether user can access page for showing non
            overlapping modules without request errors.
        '''
        root = self.test_app.get(self.URL_NON_OVERLAP_MODS)

        assert_equal(root.status, 200)


    def test_non_overlapping_modules_contents(self):
        '''
            Tests if the non-overlapping modules page contains
            the necessary views.
        '''
        root = self.test_app.get(self.URL_NON_OVERLAP_MODS)

        root.mustcontain(self.DEFAULT_TITLE)
        root.mustcontain(self.TEXT)
        root.mustcontain(self.FORM)
        root.mustcontain(self.SELECT_LABEL)
        root.mustcontain(self.SELECT_ELEMENT)
        root.mustcontain(self.TABLE_HEADER_MODULE_CODE_ONE)
        root.mustcontain(self.TABLE_HEADER_MODULE_NAME_ONE)
        root.mustcontain(self.TABLE_HEADER_MODULE_CODE_TWO)
        root.mustcontain(self.TABLE_HEADER_MODULE_NAME_TWO)

    def test_redirect_button(self):
        '''
            tests if redirect works
        '''

        root = self.test_app.get(self.URL_NON_OVERLAP_MODS)
        form = root.forms__get()["ay-form"]
        form.__setitem__("sem", "AY 16/17 Sem 2")
        response = form.submit()

        #check response is 303 see other
        assert_equal(response.status, 303)

        redirected = response.follow()
        assert_equal(redirected.status, 200)

        #checks changed content of redirected field

        redirected.mustcontain(self.REDIRECT_CHANGED_CONTENT)

    def test_error_redirect(self):
        '''
            tests if redirect to outcome when ay-sem is invalid
        '''
        root = self.test_app.get(self.URL_NON_OVERLAP_MODS_INVALID)

        #checks if directs to validating page
        assert_equal(root.status, 200)
        root.mustcontain(self.VALIDATING_TITLE)

        #checks if validating page contain expected elements
        root.mustcontain(self.SCRIPT_REDIRECT_TO_DEFAULT)
        root.mustcontain(self.SCRIPT_ERROR_MESSAGE)
