'''
    test_add_module.py tests the add module page
'''

import web
from paste.fixture import TestApp
from nose.tools import assert_equal
from app import APP
from components import session


class TestCode(object):
    '''
        runs tests to test accessability and components in add module page
    '''
    HEADER_TITLE = '<h1 class="text-center"><b>Add Module</b></h1>'
    FORM_LABEL_CODE = '<label for="module-code" class="col-2 col-form-table">' +\
                      'Module Code:</label>'
    FORM_INPUT_CODE = '<input class="form-control" type="text" id="module-code" ' +\
                      'name="code" pattern="[A-Z]{2,3}[0-9]{4}[A-Z]{0,2}" ' +\
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
