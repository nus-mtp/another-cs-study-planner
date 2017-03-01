'''
    This module creates an application instance with a configured URL router.
'''


import web
import base64, pickle, sys
sys.argv=[] # pickle needs sys.argv... 

init_values = {'id': None,
               'keyError': False,
               'displayErrorMessage': False,
               'editModMsg': None,
               'editMountMsg': None}

web.ACCOUNT_CREATED_SUCCESSFUL = 1
web.ACCOUNT_CREATED_UNSUCCESSFUL = -1
web.ACCOUNT_LOGIN_SUCCESSFUL = 2
web.ACCOUNT_LOGIN_UNSUCCESSFUL = -2

web.config.session_parameters['ignore_expiry'] = False

disk_store = web.session.DiskStore('./sessions')

def init_session(app):
    print('Initializing new session...')
    session = web.session.Session(app, disk_store,
                                      initializer=init_values)._initializer

def get_session(app):
    session_id = web.cookies().get('webpy_session_id')
    session = open('./sessions/'+session_id)
    pickled = base64.decodestring(session.read())
    session_instance = pickle.loads(pickled)
    print('Got Session,', session_instance)
    return session_instance

def get_session_value(session, key):
    return session[key]

                              

'''
THIS CODE SHOULD CREATE A FILE IN THE SESSION FOLDER + WEB CONFIG SESSION (total = 2)
IN FUTURE FILES, SHOULD PULL FROM SESSION FOLDER USING HANDLER
SOMEHOW

if not web.config.get('session'):
    ### Define the initial session
    ### Store the data in the directory './sessions'
    init = {'count':0}
    store = web.session.DiskStore('./sessions')
    session = web.session.Session(app, store, initializer=init)
    
    ### Store it somewhere we can access
    web.config.session = session
else:
    ### If it is already created, just use the old one
    session = web.config.session

https://ongspxm.wordpress.com/2014/12/02/tutorial-using-sessions-in-web-py/
'''



