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
    URL_THIS_PAGE = '/starredModules'

    def GET(self):
        '''
            This function is called when /starredModules is accessed.
        '''
        if not session.validate_session():
            raise web.seeother('/login')
        else:
            starred_module_infos = model.get_starred_modules(web.cookies().get('user'))
            return RENDER.starredModulesListing(starred_module_infos)

    def POST(self):
        '''
            This function might be called from button links from other pages.
        '''

        # Detects if this function is called from button links from another page.
        referrer_page = web.ctx.env.get('HTTP_REFERER', self.URL_THIS_PAGE)
        parts = referrer_page.split("/")
        referrer_page_shortform = "/" + parts[len(parts) - 1]
        # If referred from another page, direct to this page straight away.
        if referrer_page_shortform != self.URL_THIS_PAGE:
            raise web.seeother(self.URL_THIS_PAGE)

        try:
            data = web.input()
            action = data.action  # if action is not 'delete', will trigger AttributeError
            module_code = data.code
            model.unstar_module(module_code, web.cookies().get('user'))
            outcome = model.delete_module(module_code)
            if not outcome:
                model.star_module(module_code, web.cookies().get('user'))
            return Outcome().POST("star_delete_module", outcome, module_code)

        except AttributeError:
            raise web.seeother(self.URL_THIS_PAGE)
