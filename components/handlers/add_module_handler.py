'''
    This module contains the handlers for add module page
'''

from app import RENDER
import web
from components import model, session
from components.handlers.outcome import Outcome

class AddModule(object):
    '''
        This class handles displaying the add module form and it's posts
    '''
    def GET(self):
        '''
            render page with add module form
        '''
        if not session.validate_session():
            raise web.seeother('/login')

        return RENDER.addModules()

    def POST(self):
        '''
            Handles the submitting of the add module form
        '''
        #get module values from form
        try:
            data = web.input()
            module_code = data.code.upper()
            module_name = data.name
            module_desc = data.description
            module_mc = data.mc
            #string is valid
            if not (model.check_code(module_code) and model.check_name(module_name)
                    and model.check_mcs(module_mc)):
                return model.outcome_invalid()

            outcome = model.add_module(module_code, module_name, module_desc, module_mc, 'New')
            return Outcome().POST("add_module", outcome, module_code)
        except AttributeError:
            return Outcome().POST("add_module", False, None)
