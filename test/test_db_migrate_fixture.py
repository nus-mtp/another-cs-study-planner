'''
    test_db_migrate.py test the application's database-migration page
'''
from paste.fixture import TestApp
from nose.tools import assert_equal
from app import APP
from components import session

class TestCode(object):
    '''
        This class runs the test cases to test the database migration page
    '''


    URL_VALID = '/migrateDatabase'

    ACKNOWLEDGEMENT_SCRIPT_1 = '<script type="text/javascript">'
    ACKNOWLEDGEMENT_SCRIPT_2 = '$("#db-migration-acknowledgement")' +\
                             '.click(function()'
    ACKNOWLEDGEMENT_SCRIPT_BODY_1 = 'if (this.checked)'
    ACKNOWLEDGEMENT_SCRIPT_BODY_2 = 'proceedBtn.style.display = "";'
    ACKNOWLEDGEMENT_SCRIPT_BODY_3 = 'else'
    ACKNOWLEDGEMENT_SCRIPT_BODY_4 = 'proceedBtn.style.display = "none";'

    BACK_BUTTON = '<a class="btn btn-lg btn-primary" ' +\
                  'id="db-migrate-go-back" href="/">Go Back</a>'
    PROCEED_BUTTON = '<button class="btn btn-lg btn-danger" ' +\
                     'id="db-migrate-btn" type="submit" ' +\
                     'style="display: none;">' +\
                     'Proceed with Database Migration</button>'


    def __init__(self):
        '''
            Initialise testcode
        '''
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


    def test_db_migrate_page_valid_response(self):
        '''
            Tests if user can access the database migration page without request errors.
        '''
        root = self.test_app.get(self.URL_VALID)

        # checks if HTTP response code is 200 (= OK)
        assert_equal(root.status, 200)


    def test_db_migrate_page_valid_contents(self):
        '''
            Tests if the expected contents should show up in
            the database migration page.
        '''
        root = self.test_app.get(self.URL_VALID)

        root.mustcontain(self.ACKNOWLEDGEMENT_SCRIPT_1)
        root.mustcontain(self.ACKNOWLEDGEMENT_SCRIPT_2)
        root.mustcontain(self.ACKNOWLEDGEMENT_SCRIPT_BODY_1)
        root.mustcontain(self.ACKNOWLEDGEMENT_SCRIPT_BODY_2)
        root.mustcontain(self.ACKNOWLEDGEMENT_SCRIPT_BODY_3)
        root.mustcontain(self.ACKNOWLEDGEMENT_SCRIPT_BODY_4)

        root.mustcontain(self.BACK_BUTTON)
        root.mustcontain(self.PROCEED_BUTTON)


    def test_db_migrate_page_back_button(self):
        '''
            Tests whether the back button in the page works.
        '''
        root = self.test_app.get(self.URL_VALID)

        response = root.click(linkid="db-migrate-go-back")

        assert_equal(response.status, 200)
        response.mustcontain("Welcome")
