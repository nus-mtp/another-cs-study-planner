'''
    This module contains the handler for web requests pertaining to
    full modules listing.
'''


from app import RENDER, SESSION
import web
from components import model


class Modules(object):
    '''
        This class handles the 'Add Module' form and the displaying of list of modules
    '''
    URL_THIS_PAGE = '/modules'

    def __init__(self):
        self.form = self.create_form()


    def GET(self):
        '''
            This function is called when the '/' page (index.html) is loaded
            If user is not logged in, they are redirected to the login page.
        '''
        if SESSION['id'] != web.ACCOUNT_LOGIN_SUCCESSFUL:
            raise web.seeother('/login')
        else:
            module_infos = model.get_all_modules()
            form = self.form()
            if SESSION['displayErrorMessage'] is True:
                SESSION['displayErrorMessage'] = False
            else:
                SESSION['keyError'] = False

            return RENDER.moduleListing(module_infos, form, SESSION['keyError'])


    def POST(self):
        '''
            This function is called when the 'Add Module' form is submitted
            if form input is invalid, reload the page and shows error message besides field.
            This function might also be called from button links from other pages.
        '''

        # Detects if this function is called from button links from another page.
        referrer_page = web.ctx.env.get('HTTP_REFERER', self.URL_THIS_PAGE)
        parts = referrer_page.split("/")
        referrer_page_shortform = "/" + parts[len(parts) - 1]
        # If referred from another page, direct to this page straight away.
        if referrer_page_shortform != self.URL_THIS_PAGE:
            raise web.seeother(self.URL_THIS_PAGE)

        # When 'Add Module' form is submitted
        form = self.form()
        # If module add is unsuccessful
        if not form.validates():
            modules = model.get_all_modules()
            return RENDER.moduleListing(modules, form, SESSION['keyError'])

        # else add module to db and refresh page
        outcome = model.add_module(form.d.code, form.d.name, form.d.description, form.d.mc, 'New')
        if outcome is False:
            SESSION['keyError'] = True
            SESSION['displayErrorMessage'] = True
        raise web.seeother(self.URL_THIS_PAGE)        # load index.html again


    def create_form(self):
        ''' Creates the 'Add Module' form that will appear on the webpage '''
        code_validation_alphanumeric = web.form.regexp(
            r"^\w+$", 'Module code should be alphanumeric.')

        name_validation_alphanumeric = web.form.regexp(
            r"^[\w\s]+$", 'Module name should be alphanumeric.')

        validation_numeric_only = web.form.regexp(
            r"^\d+$", 'Number of MCs should be a number.')

        module_code_textbox = web.form.Textbox('code',
                                               web.form.notnull,
                                               code_validation_alphanumeric,
                                               post="<br><br>",
                                               description="Code")

        module_name_textbox = web.form.Textbox('name',
                                               web.form.notnull,
                                               name_validation_alphanumeric,
                                               post="<br><br>",
                                               description="Name")

        module_description_textarea = web.form.Textarea('description',
                                                        web.form.notnull,
                                                        rows="5",
                                                        cols="55",
                                                        post="<br><br>",
                                                        description="Description")

        module_mcs = web.form.Textbox('mc',
                                      web.form.notnull,
                                      validation_numeric_only,
                                      post="<br><br>",
                                      description="MCs")

        module_form_submit_button = web.form.Button('Add Module',
                                                    class_="btn btn-primary")

        form = web.form.Form(module_code_textbox,
                             module_name_textbox,
                             module_description_textarea,
                             module_mcs,
                             module_form_submit_button)
        return form



class FlagAsRemoved(object):
    '''
        This class handles the flagging of a module as 'To Be Removed'
    '''
    URL_THIS_PAGE = '/modules'

    def GET(self):
        ''' Redirect '''
        raise web.seeother(self.URL_THIS_PAGE)


    def POST(self, module_code):
        ''' Flag module as removed '''
        model.flag_module_as_removed(module_code)
        raise web.seeother(self.URL_THIS_PAGE)



class DeleteMod(object):
    '''
        This class handles the deletion of module
    '''
    URL_THIS_PAGE = '/modules'

    def GET(self):
        ''' Redirect '''
        raise web.seeother(self.URL_THIS_PAGE)


    def POST(self, module_code):        # module_code is obtained from the end of the URL
        ''' Delete the module '''
        model.delete_module(module_code)
        raise web.seeother(self.URL_THIS_PAGE)
