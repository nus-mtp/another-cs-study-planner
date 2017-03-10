'''
    This module contains the handlers for add module page
'''

from app import RENDER, SESSION
import web
from components import model

class AddModule(object):
    '''
        This class handles displaying the add module form and it's posts
    '''
    def GET(self):
        '''
            render page with add module form
        '''
        if SESSION['id'] != web.ACCOUNT_LOGIN_SUCCESSFUL:
            raise web.seeother('/login')
        return RENDER.addModules()

    def POST(self):
        '''
            Handles the submitting of the add module form
        '''
        #get module values from form
        data = web.input()
        module_code = data.code
        module_name = data.name
        module_desc = data.description
        module_mc = data.mc

        #add
        outcome = model.add_module(module_code, module_name, module_desc, module_mc, 'New')
        if outcome is True:
            #add module success
            raise web.seeother('/viewModule?code=' + module_code)
        else:
            error = "module already exist"
            raise web.seeother('/errorPage?error=' + error)
