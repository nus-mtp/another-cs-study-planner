'''
    test_login_registration.py tests the page views and navigations for
    user login and registration.

    Firstly, we specify a target URL for conducting UI testing.

    Then, we proceed to test the following things:
    #1 Accessing the target page should be possible (i.e. response code should be 200 OK).
    #2 The necessary HTML elements are contained in the page view for target page.
    #3 Navigating to other valid pages from the target page should be successful.

    For #3, we do not check the full correctness of the UI for the other pages, as this
    will be handled by its corresponding test cases.

    Since the login-registration page requires the presence of a valid user account
    as well as the necessary web environment variables, we import other components
    that are required, which are:

    1) model (from components) -> to insert a dummy valid user account
    2) hashlib -> to facilitate insertion of dummy valid user account
    3) uuid -> to facilitate insertion of dummy valid user account
    4) web -> to maintain the needed web environment variables that handle the login
'''


import hashlib
import uuid
from paste.fixture import TestApp
from nose.tools import assert_equal
import app
from components import model



class TestCode(object):
    '''
        This class contains methods that tests the page views and navigations inside
        the target page.
    '''


    URL_DEFAULT_LOGIN = '/login'
    URL_INDEX = '/'
    URL_DEFAULT_LOGOUT = '/logout'

    FORM_USER_LOGIN = '<form id="loginForm" action="/verifyLogin" method="post">'
    FORM_USER_LOGIN_USERNAME_LABEL = '<label for="username">Username</label>'
    FORM_USER_LOGIN_USERNAME_FIELD = '<input type="text" id="username" ' +\
                                     'name="username"/>'
    FORM_USER_LOGIN_PASSWORD_LABEL = '<label for="password">Password</label>'
    FORM_USER_LOGIN_PASSWORD_FIELD = '<input type="text" id="password" ' +\
                                     'name="password"/>'
    FORM_USER_LOGIN_BUTTON = '<input class="btn btn-primary" ' +\
                              'type="submit" value="Login" />'

    FORM_USER_REGISTRATION = '<form id="registerForm" action="" method="post">'
    FORM_USER_REGISTRATION_USERNAME_LABEL = '<label for="username">Username</label>'
    FORM_USER_REGISTRATION_USERNAME_FIELD = '<input type="text" id="username" ' +\
                                            'name="username"/>'
    FORM_USER_REGISTRATION_PASSWORD_LABEL = '<label for="password">Password</label>'
    FORM_USER_REGISTRATION_PASSWORD_FIELD = '<input type="text" id="password" ' +\
                                            'name="password"/>'
    FORM_USER_REGISTRATION_BUTTON = '<input class="btn btn-info" ' +\
                              'type="submit" value="Register" />'

    HEADER_ALREADY_LOGGED_IN = 'You have already logged in.'
    BUTTON_ALREADY_LOGGED_IN = '<a href="/"><button class="btn btn-primary">' +\
                               'Enter</button></a>'

    SCRIPT_ACCOUNT_CREATE_SUCCESSFUL = 'window.alert("Your account has been ' +\
                                       'created successfully.");'
    SCRIPT_ACCOUNT_CREATE_UNSUCCESSFUL = 'window.alert("The username has been ' +\
                                         'taken. Please register with a different ' +\
                                         'username.");'
    SCRIPT_ACCOUNT_LOGIN_UNSUCCESSFUL = 'window.alert("Login credentials are ' +\
                                        'incorrect. Please try again.");'

    def __init__(self):
        self.middleware = None
        self.test_app = None

    def setUp(self):
        '''
            Sets up the 'app.py' fixture, along with the important
            user accounts states.
        '''
        self.middleware = []
        app.APP.add_processor(app.web.loadhook(app.session_hook))
        self.test_app = TestApp(app.APP.wsgifunc(*self.middleware))
        model.delete_admin("user")
        model.delete_admin("user2")
        self.create_dummy_user()


    def tearDown(self):
        '''
            Removes any trace of dummy accounts that were present
            during the invocation of all the test cases and logs out if needed.
        '''
        model.delete_admin("user")
        model.delete_admin("user2")
        self.test_app.post(self.URL_DEFAULT_LOGOUT)


    def create_dummy_user(self):
        '''
            Creates the dummy valid user that will be used in
            this series of test cases.
        '''
        salt = uuid.uuid4().hex
        hashed_password = hashlib.sha512("12345678" + salt).hexdigest()
        model.add_admin("user", salt, hashed_password)


    def test_login_valid_response(self):
        '''
            Tests whether user can access page for showing fixed module
            mountings without request errors.
        '''
        root = self.test_app.get(self.URL_DEFAULT_LOGIN)

        # checks if HTTP response code is 200 (= OK)
        assert_equal(root.status, 200)


    def test_redirect_to_login_response(self):
        '''
            Tests whether user WILL be redirected from home page if
            user has not logged in.
        '''
        root = self.test_app.get(self.URL_INDEX)

        # checks if HTTP response code is 303 (= See Other)
        assert_equal(root.status, 303)

        redirected = root.follow()
        assert_equal(redirected.status, 200)
        # Presence of these elements indicates that the request direction is correct.
        # Checks if page contains 'User Login' title
        redirected.mustcontain("User Login")


    def test_valid_login_submission_response(self):
        '''
            Tests if user is redirected to index upon successful login.
        '''
        root = self.test_app.get(self.URL_DEFAULT_LOGIN)
        login_form = root.forms__get()["loginForm"]
        login_form.__setitem__("username", "user")
        login_form.__setitem__("password", "12345678")
        response = login_form.submit()

        # checks if HTTP response code is 303 (= See Other)
        assert_equal(response.status, 303)

        redirected = response.follow()
        assert_equal(redirected.status, 200)

        # Presence of these elements indicates that the request direction is correct.
        # Checks if page contains title of All Modules page
        redirected.mustcontain("All Modules")

        #FAIL
    def test_blank_username_login_submission_response(self):
        '''
            Tests if user should fail to login if username
            field blank.
        '''
        root = self.test_app.get(self.URL_DEFAULT_LOGIN)
        login_form = root.forms__get()["loginForm"]
        login_form.__setitem__("password", "12345678")
        response = login_form.submit()

        # checks if HTTP response code is 303 (= See Other)
        assert_equal(response.status, 303)

        redirected = response.follow()
        assert_equal(redirected.status, 200)

        # Presence of these elements indicates that the request direction is correct.
        # Checks if page contains 'User Login' title
        redirected.mustcontain("User Login")
        redirected.mustcontain(self.SCRIPT_ACCOUNT_LOGIN_UNSUCCESSFUL)

        #FAIL
    def test_blank_password_login_submission_response(self):
        '''
            Tests if user should fail to login if password
            field is blank.
        '''
        root = self.test_app.get(self.URL_DEFAULT_LOGIN)
        login_form = root.forms__get()["loginForm"]
        login_form.__setitem__("username", "user")
        response = login_form.submit()

        # checks if HTTP response code is 303 (= See Other)
        assert_equal(response.status, 303)

        redirected = response.follow()
        assert_equal(redirected.status, 200)

        # Presence of these elements indicates that the request direction is correct.
        # Checks if page contains 'User Login' title
        redirected.mustcontain(self.SCRIPT_ACCOUNT_LOGIN_UNSUCCESSFUL)
        redirected.mustcontain("User Login")


    def test_invalid_account_login_submission_response(self):
        '''
            Tests if user should fail to login with non-existent account.
        '''
        root = self.test_app.get(self.URL_DEFAULT_LOGIN)
        login_form = root.forms__get()["loginForm"]
        login_form.__setitem__("username", "nonexistent")
        login_form.__setitem__("password", "12345678")
        response = login_form.submit()

        # checks if HTTP response code is 303 (= See Other)
        assert_equal(response.status, 303)

        redirected = response.follow()
        assert_equal(redirected.status, 200)

        # Presence of these elements indicates that the request direction is correct.
        # Checks if page contains 'User Login' title
        redirected.mustcontain("User Login")
        redirected.mustcontain(self.SCRIPT_ACCOUNT_LOGIN_UNSUCCESSFUL)

        #FAIL
    def test_already_logged_in_response(self):
        '''
            Tests if user should not see the login form if he has
            already logged in to the system.
        '''
        root = self.test_app.get(self.URL_DEFAULT_LOGIN)
        login_form = root.forms__get()["loginForm"]
        login_form.__setitem__("username", "user")
        login_form.__setitem__("password", "12345678")
        response = login_form.submit()

        # checks if HTTP response code is 303 (= See Other)
        assert_equal(response.status, 303)

        redirected = response.follow()
        assert_equal(redirected.status, 200)

        # Presence of these elements indicates that the request direction is correct.
        # Checks if page contains title of All Modules page
        redirected.mustcontain("All Modules")

        login_page = redirected.goto(self.URL_DEFAULT_LOGIN, method="get")
        assert_equal(login_page.status, 200)

        login_page.mustcontain(self.HEADER_ALREADY_LOGGED_IN)
        login_page.mustcontain(self.BUTTON_ALREADY_LOGGED_IN)

    def test_valid_registration_submission_response(self):
        '''
            Tests if user is redirected correctly upon successful registration.
        '''
        root = self.test_app.get(self.URL_DEFAULT_LOGIN)
        registration_form = root.forms__get()["registerForm"]
        registration_form.__setitem__("username", "user2")
        registration_form.__setitem__("password", "12345678")
        response = registration_form.submit()

        # checks if HTTP response code is 303 (= See Other)
        assert_equal(response.status, 303)

        redirected = response.follow()
        assert_equal(redirected.status, 200)

        # Presence of these elements indicates that the request direction is correct.
        # Checks if page contains 'User Login' title
        redirected.mustcontain("User Login")
        redirected.mustcontain(self.SCRIPT_ACCOUNT_CREATE_SUCCESSFUL)


    def test_blank_username_registration_submission_response(self):
        '''
            Tests if account registration with no username triggers validation.
        '''
        root = self.test_app.get(self.URL_DEFAULT_LOGIN)
        registration_form = root.forms__get()["registerForm"]
        registration_form.__setitem__("password", "12345678")
        response = registration_form.submit()

        # checks if HTTP response code is 200 (= OK)
        # No redirection occurs if any field is blank
        assert_equal(response.status, 200)

        # Presence of these elements indicates that the request direction is correct.
        # Checks if page contains 'User Login' title and the validation message.
        response.mustcontain("User Login")
        response.mustcontain("Required")


    def test_blank_password_registration_submission_response(self):
        '''
            Tests if account registration with no password triggers validation.
        '''
        root = self.test_app.get(self.URL_DEFAULT_LOGIN)
        registration_form = root.forms__get()["registerForm"]
        registration_form.__setitem__("username", "user2")
        response = registration_form.submit()

        # checks if HTTP response code is 200 (= OK)
        # No redirection occurs if any field is blank
        assert_equal(response.status, 200)

        # Presence of these elements indicates that the request direction is correct.
        # Checks if page contains 'User Login' title and the validation message.
        response.mustcontain("User Login")
        response.mustcontain("Required")


    def test_duplicate_username_registration_submission_response(self):
        '''
            Tests if account registration with a pre-existing username
            triggers validation.
        '''
        root = self.test_app.get(self.URL_DEFAULT_LOGIN)
        registration_form = root.forms__get()["registerForm"]
        registration_form.__setitem__("username", "user")
        registration_form.__setitem__("password", "12345678")
        response = registration_form.submit()

        # checks if HTTP response code is 303 (= See Other)
        # Redirection occurs if no fields are blank.
        assert_equal(response.status, 303)

        redirected = response.follow()
        assert_equal(redirected.status, 200)

        # Presence of these elements indicates that the request direction is correct.
        # Checks if page contains 'User Login' title and the validation message.
        redirected.mustcontain("User Login")
        redirected.mustcontain(self.SCRIPT_ACCOUNT_CREATE_UNSUCCESSFUL)
