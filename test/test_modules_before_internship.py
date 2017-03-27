'''
    test_modules_before_internship_ui.py tests the page views for
    viewing modules taken before internship

    Firstly, we specify a target URL for conducting UI testing.

    Then, we proceed to test the following things:
    #1 Accessing the target page should be possible (i.e. response code should be 200 OK).
    #2 The necessary HTML elements are contained in the page view for target page.

'''


from paste.fixture import TestApp
from nose.tools import assert_equal, raises
from app import APP
from components import session


class TestCode(object):
    '''
        This class contains methods that tests the page views inside
        the target page.
    '''


    URL_MODS_BEFORE_INTERNSHIP = '/moduleTakenPriorToInternship'
    URL_MODS_BEFORE_INTERNSHIP_SPECIFIC = '/moduleTakenPriorToInternship?aysem=AY%2016/17%20Sem%202'
    URL_MODS_BEFORE_INTERNSHIP_INVALID = '/moduleTakenPriorToInternship?aysem=AY%2016/18%20Sem%202'
    CURRENT_SEM = 'AY 16/17 Sem 1'
    DEFAULT_TITLE = 'Modules Taken Prior to Internship for'
    TEXT = '<p class="text-center">Shows all modules taken by students prior to taking ' +\
           'internship for a particular semester, and how many students took them.</b> ' +\
           '<span class="glyphicon glyphicon-info-sign" data-toggle="tooltip" ' +\
           'data-placement="bottom" title="By default, this shows all data before ' +\
           'students take internship in the current AY-Sem."></span></p>'
    FORM = '<form id="ay-form" class="form-inline" ' +\
           'action="/moduleTakenPriorToInternship" method="post">'
    SELECT_LABEL = '<label for="ay-sem">Select AY-Sem:</label>'
    SELECT_ELEMENT = '<select class="form-control selectpicker" name="aysem">'
    TABLE_HEADER_MODULE_CODE = '<th>Code</th>'
    TABLE_HEADER_MODULE_NAME = '<th>Name</th>'
    TABLE_HEADER_NUM_STUDENTS = '<th>Number of Students</th>'

    REDIRECT_CHANGED_CONTENT = 'Modules Taken Prior to Internship for AY 16/17 Sem 2'
    SCRIPT_REDIRECT_TO_DEFAULT = "window.location = '/moduleTakenPriorToInternship'"
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


    def test_modules_before_internship_valid_response(self):
        '''
            Tests whether user can access page for showing non
            overlapping modules without request errors.
        '''
        root = self.test_app.get(self.URL_MODS_BEFORE_INTERNSHIP)

        assert_equal(root.status, 200)


    def test_non_overlapping_modules_contents(self):
        '''
            Tests if the non-overlapping modules page contains
            the necessary views.
        '''
        root = self.test_app.get(self.URL_MODS_BEFORE_INTERNSHIP)

        root.mustcontain(self.DEFAULT_TITLE)
        root.mustcontain(self.TEXT)
        root.mustcontain(self.FORM)
        root.mustcontain(self.SELECT_LABEL)
        root.mustcontain(self.SELECT_ELEMENT)
        root.mustcontain(self.TABLE_HEADER_MODULE_CODE)
        root.mustcontain(self.TABLE_HEADER_MODULE_NAME)
        root.mustcontain(self.TABLE_HEADER_NUM_STUDENTS)


    def test_redirect_button(self):
        '''
            tests if redirect works
        '''

        root = self.test_app.get(self.URL_MODS_BEFORE_INTERNSHIP)
        form = root.forms__get()["ay-form"]
        form.__setitem__("aysem", "AY 16/17 Sem 2")
        response = form.submit()

        #check response is 303 see other
        assert_equal(response.status, 303)

        redirected = response.follow()
        assert_equal(redirected.status, 200)

        #checks changed content of redirected field

        redirected.mustcontain(self.REDIRECT_CHANGED_CONTENT)


    @raises(Exception)
    def test_error_redirect(self):
        '''
            tests if redirect to outcome when ay-sem is invalid
        '''
        root = self.test_app.get(self.URL_MODS_BEFORE_INTERNSHIP_INVALID)

        #checks if directs to validating page
        assert_equal(root.status, 200)
