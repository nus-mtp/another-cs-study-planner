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
        if not session.validate_session():
            raise web.seeother('/login')
        else:
            input_data = model.validate_input(web.input(), ["code"])
            module_code = input_data.code

            module_info = model.get_module(module_code)
            if module_info is None:
                raise web.notfound(RENDER.notfound("Module " +\
                 module_code + " does not exist in the system."))

            prerequisites = model.get_prerequisite_units(module_code)
            return RENDER.moduleEditPrerequisite(module_code, prerequisites)


    def POST(self):
        '''
            Handles the submission of updated module prerequisites
            for a target module.
        '''
        module_code = web.input().get('code')
        prerequisites = json.loads(web.input().get('prerequisites'))

        isSucessfullyUpdated = model.edit_prerequisite(module_code, prerequisites)

        return isSucessfullyUpdated
