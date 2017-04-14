'''
    This module contains the handler for web requests pertaining to
    the editing of a module's prerequisites.
'''


import json
from app import RENDER
import web
from components import model, session


class EditModulePrerequisites(object):
    '''
        This class handles the editing of a module's prerequisites.
    '''
    def GET(self):
        '''
            Handles the loading of the 'Edit Module Prerequisites' page.
        '''
        web.header('X-Frame-Options', 'SAMEORIGIN')
        web.header('X-Content-Type-Options', 'nosniff')
        web.header('X-XSS-Protection', '1')
        if not session.validate_session():
            raise web.seeother('/login')
        else:
            input_data = model.validate_input(web.input(), ["code"])
            module_code = input_data.code.upper()

            prerequisites = model.get_prerequisite_units(module_code)
            return RENDER.moduleEditPrerequisite(module_code, prerequisites)


    def POST(self):
        '''
            Handles the submission of updated module prerequisites
            for a target module.
        '''
        web.header('X-Frame-Options', 'SAMEORIGIN')
        web.header('X-Content-Type-Options', 'nosniff')
        web.header('X-XSS-Protection', '1')
        isSucessfullyUpdated = False

        input_data = model.validate_input(web.input(), ["code"], show_404=False)

        if input_data:
            module_code = input_data.code.upper()
            prerequisites = json.loads(input_data.prerequisites)
            isSucessfullyUpdated = model.edit_prerequisite(module_code, prerequisites)

        new_prerequisites = model.get_prerequisite_as_string(module_code)
        response = [isSucessfullyUpdated, new_prerequisites]

        return json.dumps(response)
