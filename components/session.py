'''
    This module handles session authentication and
    session handling for test cases
'''
import hashlib
import uuid
import datetime
import web
import components.model

DUMMY_USER_ID = 'testUser'
DUMMY_PASSWORD = '12345678'
URL_DEFAULT_LOGIN = '/login'
URL_DEFAULT_LOGOUT = '/logout'

COOKIE_TIME = 60*10

def init_session(user_id):
    '''
        Create a session id and enter it into the database,
        then set the cookie.
    '''
    session_salt = uuid.uuid4().hex
    components.model.add_session(user_id, session_salt)
    session_id = hashlib.sha512(user_id + session_salt).hexdigest()
    web.setcookie('user', user_id, COOKIE_TIME, httponly=True)
    web.setcookie('session_id', session_id, COOKIE_TIME, httponly=True)


def validate_session():
    '''
        Check if session is valid by checking if
        cookies have been tampered with.
        Also refreshes session.
    '''
    try:
        user = web.cookies().get('user')
        session_id = web.cookies().get('session_id')
        refresh_sessions(user, session_id)
        return components.model.validate_session(user, session_id)
    except:
        return False


def refresh_sessions(user, session_id):
    '''
        Refresh the session by extending the cookie expiry time.
    '''
    web.setcookie('user', user, COOKIE_TIME, httponly=True)
    web.setcookie('session_id', session_id, COOKIE_TIME, httponly=True)


def clean_up_sessions():
    '''
        Remove all sessions that have expired
        from database.
    '''
    yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
    components.model.clean_old_sessions(yesterday)


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
    login_form.__setitem__("id", DUMMY_USER_ID)
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
