'''
    contains test cases for overlapping_modules.py
    How this works:
    #1 check that page can be accessed throught URL
    #2 check that page contents are what is expected with example
    #2 check that components found on page are same as expected when
        using form to search for a certain mod.
'''
from nose.tools import assert_equal
from paste.fixture import TestApp
from app import APP, SESSION

class TestCode(object):
    '''
        this class runs the tests cases for overlapping_modules.py
    '''

    URL_ALL = '/overlappingModules?code='
    URL_CS1010 = '/overlappingModules?code=CS1010'
    URL_EXCEPTION_HANDLE = '/overlappingModules'

    FORM_ID = 'search-modules-taken-tgt-form'

    def __init__(self):
        self.middleware = None
        self.test_app = None

    def setUp(self):
        '''
            Sets up the 'app.py' fixture
        '''
        SESSION['id'] = 2
        self.middleware = []
        self.test_app = TestApp(APP.wsgifunc(*self.middleware))

    def test_page_access(self):
        '''
            tests if the page can be accessed
        '''
        page = self.test_app.get(self.URL_ALL)
        assert_equal(page.status, 200)

        page = self.test_app.get(self.URL_CS1010)
        assert_equal(page.status, 200)

        page = self.test_app.get(self.URL_EXCEPTION_HANDLE)
        assert_equal(page.status, 200)

    def test_page_contents(self):
        '''
            tests if contents are as expected when there is no code
        '''
        page = self.test_app.get(self.URL_ALL)
        page.mustcontain("Modules taken together in the same semester")

    def test_page_example_contents(self):
        '''
            tests if contents as as expected when the code is CS1010
        '''
        page_cs1010 = self.test_app.get(self.URL_CS1010)

        page_cs1010.mustcontain("Results for Modules taken together same semester with CS1010")

    def test_form(self):
        '''
            tests if the find modules usually taken with form exists and works
            as expected
        '''
        page = self.test_app.get(self.URL_ALL)
        form = page.forms__get()[self.FORM_ID]
        form.__setitem__("code", "CS1010")
        response = form.submit()

        assert_equal(response.status, 303)

        #followed must be the same as redirection using url
        redirected = response.follow()
        page_cs1010 = self.test_app.get(self.URL_CS1010)

        assert_equal(redirected.body, page_cs1010.body)
