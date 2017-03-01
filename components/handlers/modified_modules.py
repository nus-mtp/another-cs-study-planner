'''
    This module contains the handler for web requests pertaining to
    retrieiving modules that have been modified.
'''


from app import RENDER, SESSION
import web
from components import model


class Modified(object):
    '''
        This class contains the implementations of the GET and POST requests.
        It retrieves a list of modified modules and determine which attributes
        have been modified.
    '''
    def GET(self):
        '''
            Renders the modified modules page if users requested
            for the page through the GET method.
        '''
        if SESSION['id'] != web.ACCOUNT_LOGIN_SUCCESSFUL:
            raise web.seeother('/login')

        modified_modules = model.get_modules_with_modified_quota()
        modified_modules = [list(module) for module in modified_modules]
        for module in modified_modules:
            current_quota = module[3]
            modified_quota = module[4]
            if current_quota is None:
                quota_difference = modified_quota
            elif modified_quota is None:
                quota_difference = -current_quota
            else:
                quota_difference = modified_quota - current_quota
            module.append(quota_difference)

        return RENDER.moduleModified_stub(modified_modules)


    def POST(self):
        '''
            Directs users to the page for tentative module mountings.

            This method is invoked when users click on the button
            to navigate to the tentative module mountings, that is
            present in other valid pages.
        '''
        raise web.seeother('/moduleMountingTentative')
