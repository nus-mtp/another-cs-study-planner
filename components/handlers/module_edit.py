'''
    This module contains the handler for web requests pertaining to
    the editing of a module.
'''


from app import RENDER
import web
from components import model


class EditModuleInfo(object):
    '''
        This class handles the editing of module info
        (Module name, description and MCs)
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
            overlapping_mod_list = model.get_mod_taken_together_with(module_code)
            return RENDER.moduleEdit(module_info, overlapping_mod_list)

        elif form_status == "submit":
            module_name = data.name
            description = data.desc
            mc = data.mc

            outcome = model.update_module(module_code, module_name, description, mc)
            if outcome is True:
                web.ctx.session._initializer['editModMsg'] = "Module info edited sucessfully!"
            else:
                web.ctx.session._initializer['editModMsg'] = "Sorry, an error has occurred!"

            raise web.seeother('/viewModule?code='+module_code)


class EditMountingInfo(object):
    '''
        This class handles the editing of mounting info
        (Mounting status and quota)
    '''
    def POST(self):
        '''
            Handles the loading and submission of the 'edit mounting' form
        '''
        data = web.input()
        form_status = data.status
        module_code = data.code
        ay_sem = data.aySem
        try:
            quota = data.quota
            if quota == "":
                quota = None
        except AttributeError:
            quota = None

        if form_status == "load":
            mounting_value = data.mountingValue
            overlapping_list = model.get_mod_taken_together_with(module_code)
            return RENDER.mountingEdit(module_code, ay_sem, mounting_value, quota, overlapping_list)

        elif form_status == "submit":
            old_mounting_value = data.oldMountingValue
            mounting_status = data.mountingStatus

            if mounting_status == "Mounted":
                outcome = None
                if old_mounting_value == "1":
                    outcome = model.update_quota(module_code, ay_sem, quota)
                else:
                    outcome = model.add_tenta_mounting(module_code, ay_sem, quota)
            elif mounting_status == "Not Mounted":
                outcome = model.delete_tenta_mounting(module_code, ay_sem)

            if outcome is True:
                web.ctx.session._initializer['editMountMsg'] = "Mounting info edited sucessfully!"
            else:
                web.ctx.session._initializer['editMountMsg'] = "Sorry, an error has occurred!"

            raise web.seeother("individualModuleInfo?code="+module_code+"&targetAY="+\
                               ay_sem.replace(' ', '+').replace('/', '%2F'))
