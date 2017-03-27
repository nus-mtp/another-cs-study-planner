'''
    This module contains the handler for web requests pertaining to
    full modules listing.
'''


from app import RENDER
import web
from components import model, session
from components.handlers.outcome import Outcome


class Modules(object):
    '''
        This class handles the 'Add Module' form and the displaying of list of modules
    '''
    URL_THIS_PAGE = '/modules'

    def aggregate_modules_for_focus(self, module_infos):
        '''
            This function groups modules that appear more than once with different focus areas
            into a single module.
        '''
        module_code_index = 0
        focus_area_index = 5
        aggregated_module_infos = []
        for i in range(1, len(module_infos)):
            if module_infos[i - 1][module_code_index] == module_infos[i][module_code_index]:
                new_module = list(module_infos[i - 1])
                new_module[focus_area_index] += ", " + module_infos[i][focus_area_index]
                module_infos[i] = new_module
            else:
                aggregated_module_infos.append(module_infos[i - 1])
        aggregated_module_infos.append(module_infos[-1])
        return aggregated_module_infos


    def GET(self):
        '''
            This function is called when the '/modules' page (moduleListing.html) is loaded
            If user is not logged in, they are redirected to the login page.
        '''
        if not session.validate_session():
            raise web.seeother('/login')
        else:
            module_infos = model.get_all_modules_and_focus()
            aggregated_modules = self.aggregate_modules_for_focus(module_infos)
            return RENDER.moduleListing(aggregated_modules)


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
            outcome = model.delete_module(module_code)
            return Outcome().POST("delete_module", outcome, module_code)

        except AttributeError:
            raise web.seeother(self.URL_THIS_PAGE)
