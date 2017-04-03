'''
    test_modules_before_others_ui.py tests the page views for
    viewing modules taken before a specified module

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
        tests the ui elemetents of modules taken before another module
    '''
    URL_NORMAL = '/moduleTakenPriorToOthers'
    CONTENT_TITLE = '<h1 class="text-center"><b>Modules Taken Prior'+\
                    ' to Other Modules</b></h1>'
    CONTENT_DESCRIPTION = '<p class="text-center">Shows all pairs of'+\
                          ' modules where module A is taken prior to module B</p>'
    CONTENT_FORM = '<form action="/moduleTakenPriorToOthers" id="module-filter-form" method="GET">'
    CONTENT_FORM_TITLE = '<p>Tell me the number of students who have taken</p>'
    CONTENT_FORM_MODULEA = '<input type="text" name="moduleA", placeholder="Enter module'+\
                           ' code here" pattern="[a-zA-Z0-9\s]+" '+\
                           'oninvalid="this.setCustomValidity(\'Module'+\
                           ' code must be alphanumeric and not empty\')" '+\
                           'oninput="setCustomValidity(\'\')" required>'
    CONTENT_FORM_MODULEB = '<input style="display:inline-block;" type="text" name="moduleB", '+\
                           'placeholder="Enter module code here" pattern="[a-zA-Z0-9\s]+" '+\
                           'oninvalid="this.setCustomValidity(\'Module code must be alphanumeric '+\
                           'and not empty\')" oninput="setCustomValidity(\'\')" required>'
    CONTENT_FORM_SELECT = '<select style="display:inline-block;" name="aysem" required>'
    CONTENT_TABLE = '<table class="table display dataTable table-bordered table-hover'+\
                    ' text-center" id="modules-taken-prior-table">'
    CONTENT_BUTTON = '<input class="btn btn-primary" style="margin-top: '+\
                     '10px;" type="submit" value="Go">'

    FORM_NAME = 'module-filter-form'
    REDIRECT_PAGE = '<h3 style="margin-bottom: 20px;">Students who took <b><a '+\
                    'href="/viewModule?code=CS1010"'+\
                    ' target="_blank" data-toggle="tooltip" title="View general info for'+\
                    ' CO1020>CS1020</a></b> prior to taking <b><a '+\
                    'href="/viewModule?code=$moduleB" '+\
                    'target="_blank" data-toggle="tooltip" title="View general '+\
                    'info for CS1020">CS1020</a></b> in <u>AY 16/17 Sem 2</u></h3>'

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

    def test_modules_taken_before_others_response(self):
        '''
            Tests that we can access the page
        '''
        root = self.test_app.get(self.URL_NORMAL)
        assert_equal(root.status, 200)

    def test_modules_taken_before_others_contents(self):
        '''
            Test that the contents on the page are as expected.
        '''
        root = self.test_app.get(self.URL_NORMAL)
        root.mustcontain(self.CONTENT_TITLE)
        root.mustcontain(self.CONTENT_DESCRIPTION)
        root.mustcontain(self.CONTENT_FORM)
        root.mustcontain(self.CONTENT_FORM_TITLE)
        root.mustcontain(self.CONTENT_FORM_MODULEA)
        root.mustcontain(self.CONTENT_FORM_MODULEB)
        root.mustcontain(self.CONTENT_FORM_SELECT)
        root.mustcontain(self.CONTENT_TABLE)
        root.mustcontain(self.CONTENT_BUTTON)

    def test_modules_taken_before_others_submit(self):
        '''
            tests taht the submit button will cause a redirect
        '''
        root = self.test_app.get(self.URL_NORMAL)

        form = root.forms__get()[self.FORM_NAME]
        form.__setitem__("moduleA", "CS1010")
        form.__setitem__("moduleB", "CS2010")
        form.__setitem__("aysem", "AY 16/17 Sem 2")

        response = form.submit()
        #check response is 200 OK
        assert_equal(response.status, 200)
        response.mustcontain()

    @raises(Exception)
    def test_modules_taken_before_others_submit_invalid(self):
        '''
            tests taht the submit button will cause an exception
        '''
        root = self.test_app.get(self.URL_NORMAL)
        form = root.forms__get()[self.FORM_NAME]
        form.__setitem__("aysem", "AY 16/17 Sem 3")
        form.__setitem__("moduleA", "CS1010")
        form.__setitem__("moduleB", "CS2010")
        response = form.submit()
