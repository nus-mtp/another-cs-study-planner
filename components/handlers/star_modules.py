'''
    This module handles starring of modules.
'''

import web
from app import RENDER
from components import model, session
from components.handlers.outcome import Outcome


class StarModule(object):
    '''
        Class handles starring and unstarring of modules.
    '''

    def GET(self):
        '''
            This function is called when /starModule is accessed.
        '''
        if not session.validate_session():
            raise web.seeother('/login')
        else:
            module_code = web.input().star
            action = web.input().action
            if action == "star":
                model.star_module(module_code, web.cookies().get('user'))
            else:
                model.unstar_module(module_code, web.cookies().get('user'))
            raise web.seeother('/viewModule?code=' + module_code)


class StarredModulesList(object):
    '''
        Class handles showing of starredModules
    '''

    def GET(self):
        '''
            This function is called when /starredModules is accessed.
        '''
        if not session.validate_session():
            raise web.seeother('/login')
        else:
            starred_module_infos = model.get_starred_modules(web.cookies().get('user'))
            return RENDER.starredModulesListing(starred_module_infos)