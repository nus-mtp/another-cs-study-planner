'''
    This module contains the handler for web requests pertaining to
    the Delete Module page.
'''


from app import RENDER
import web
from components import model, session
from components.handlers.outcome import Outcome


class DeleteMod(object):
    '''
        This class handles the display of the Delete Module page
        and the deletion of a module
    '''
    def GET(self):
        '''
            Handles the display of the Delete Module page
        '''
        if not session.validate_session():
            raise web.seeother('/login')
        else:
            module_infos = model.get_new_modules()
            return RENDER.deleteModule(module_infos)


    def POST(self):
        '''
            Handles the deletion of a module
        '''
        # Verify that module exists
        input_data = model.validate_input(web.input(), ["code"], show_404=False)
        try:
            module_code = input_data.code
        except AttributeError:
            return Outcome().POST("delete_module", False, None)

        # Verify that module's status is 'New'
        module_infos = model.get_new_modules()
        new_modules = [module_info[0] for module_info in module_infos]
        if module_code not in new_modules:
            return Outcome().POST("delete_module", False, None)

        else:
            outcome = model.delete_module(module_code)
            return Outcome().POST("delete_module", outcome, module_code)
