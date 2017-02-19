'''
    This module contains the handler for web requests pertaining to
    the editing of a module's info.
'''


from app import RENDER, SESSION
import web
from components import model


class EditMod(object):
    '''
        This class handles the editing of module info
    '''
    def POST(self):
        '''
            Handles the loading and submission of the 'edit module' form
        '''
        data = web.input()
        form_status = data.status
        module_code = data.code

        if form_status == "load":
            module_info = model.get_module(module_code)
            return RENDER.moduleEdit_stub(module_info)

        elif form_status == "submit":
            module_name = data.name
            description = data.desc
            mc = data.mc

            outcome = model.update_module(module_code, module_name, description, mc)
            if outcome is True:
                SESSION['editModMsg'] = "Module info edited sucessfully!"
            else:
                SESSION['editModMsg'] = "Sorry, an error has occurred!"

            raise web.seeother('/viewModule?code='+module_code)
