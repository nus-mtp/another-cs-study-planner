'''
    This module handles starring of modules.
'''

import web
from app import RENDER
from components import model, session


class StarModule(object):
    '''
        Class handles starring and unstarring of modules.
    '''

    def GET(self):
        '''
            This function is called when /starModule is accessed.
        '''
        web.header('X-Frame-Options', 'SAMEORIGIN')
        web.header('X-Content-Type-Options', 'nosniff')
        web.header('X-XSS-Protection', '1')
        if not session.validate_session():
            raise web.seeother('/login')
        else:
            module_code = web.input().code
            action = web.input().action
            return_path = web.input().return_path
            # modify return path if individual module info to include aySem
            if return_path == '/individualModuleInfo':
                target_ay = web.input().aysem
                return_path = return_path + '?code=' + module_code + '&aysem=' + target_ay
            if action == "star":
                model.star_module(module_code, web.cookies().get('user'))
            else:
                model.unstar_module(module_code, web.cookies().get('user'))
            raise web.seeother(return_path)


class StarredModulesList(object):
    '''
        Class handles showing of starredModules
    '''
    URL_THIS_PAGE = '/starredModules'

    def GET(self):
        '''
            This function is called when /starredModules is accessed.
        '''
        web.header('X-Frame-Options', 'SAMEORIGIN')
        web.header('X-Content-Type-Options', 'nosniff')
        web.header('X-XSS-Protection', '1')
        if not session.validate_session():
            raise web.seeother('/login')
        else:
            starred_module_infos = model.get_starred_modules(web.cookies().get('user'))
            return RENDER.starredModulesListing(starred_module_infos)
