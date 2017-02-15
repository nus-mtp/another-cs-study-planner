'''
    This module contains the handler for web requests pertaining to
    a module's information overview.
'''


from app import RENDER
import web
from components import model


class IndividualModule(object):
    '''
        This class handles the display on a single module mounting
    '''
    def GET(self):
        ''' Retrieve and render all the info of a module mounting '''
        input_data = web.input()
        module_code = input_data.code
        module_info = model.get_module(module_code)
        target_ay = input_data.targetAY
        quota = input_data.quota
        return RENDER.individualModuleInfo(module_info, target_ay, quota)


    def POST(self):
        ''' Redirect '''
        raise web.seeother('/')
