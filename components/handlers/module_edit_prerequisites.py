'''
    This module contains the handler for web requests pertaining to
    the editing of a module's prerequisites.
'''


from app import RENDER
import web
from components import model, session
from components.handlers.outcome import Outcome


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
                return RENDER.notfound("Module " + module_code + " does not exist in the system.")

            prerequisites = model.get_prerequisite_units(module_code)
            return RENDER.moduleEditPrerequisite(module_code, prerequisites)


    def POST(self):
        '''
            Handles the submission of updated module prerequisites
            for a target module.
        '''
        module_code = web.input()['code']
        prerequisites = web.input()['prerequisites']

        # TODO: call model API for updating the module prerequisites for a target module
        # isSucessfullyUpdated = model.<something>(module_code, prerequisites)
        '''
        return isSucessfullyUpdated
        '''