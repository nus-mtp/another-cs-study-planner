'''
    This module handles session authentication and
    session handling for test cases
'''
import hashlib
import uuid
import web
import components.model

DUMMY_USER_ID = 'testUser'
DUMMY_PASSWORD = '12345678'
URL_DEFAULT_LOGIN = '/login'
URL_DEFAULT_LOGOUT = '/logout'

def validate_session():
    '''
        Check if session is valid by checking if
        a) user is logged in
        b) logged in user is who they claim to be
    '''
    try:
        # Check if user logged in successfully
        loginStatus = web.ctx.session._initializer.get('loginStatus')
        if loginStatus != web.ACCOUNT_LOGIN_SUCCESSFUL:
            return False

        # Check if user is the logged in user
        user = web.cookies().get('user')
        if web.ctx.session._initializer.get('userId') != user:
            return False
        return True
    except:
        return False


def set_up(test_app):
    '''
        Sets up for test cases by
        creating a dummy user for logging in sessions
    '''
    delete_dummy_user_for_tests()
    create_dummy_user_for_tests()
    login_session_for_tests(test_app)

def tear_down(test_app):
    '''
        Cleans up after one test cases concludes by
        deleting the dummy user and logging the user out
    '''
    delete_dummy_user_for_tests()
    logout_session_for_tests(test_app)


def create_dummy_user_for_tests():
    '''
        Creates a dummy valid user that will be
        used for creating sessions for test cases.
    '''
    salt = uuid.uuid4().hex
    hashed_password = hashlib.sha512(DUMMY_PASSWORD + salt).hexdigest()
    components.model.add_admin(DUMMY_USER_ID, salt, hashed_password)


def login_session_for_tests(test_app):
    '''
        Logs in the dummy user for test cases
    '''
    root = test_app.get(URL_DEFAULT_LOGIN)
    login_form = root.forms__get()["loginForm"]
    login_form.__setitem__("username", DUMMY_USER_ID)
    login_form.__setitem__("password", DUMMY_PASSWORD)
    login_form.submit()


def delete_dummy_user_for_tests():
    '''
        Deletes the dummy user used for
        creating sessions for test cases.
    '''
    components.model.delete_admin(DUMMY_USER_ID)


def logout_session_for_tests(test_app):
    '''
        Logs out the dummy user for test cases
    '''
    test_app.post(URL_DEFAULT_LOGOUT)
