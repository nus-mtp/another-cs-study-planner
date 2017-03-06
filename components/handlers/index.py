'''
    This module contains the handler for web requests pertaining to
    the home page.
'''

from app import RENDER, SESSION
import web
from components import model


class Index(object):
    '''
        This class handles the 'Add Module' form and the displaying of list of modules
    '''
    def __init__(self):
        self.form = self.create_form()
        print("Current session ID is: " + web.ctx.session.session_id)


    def GET(self):
        '''
            This function is called when the '/' page (index.html) is loaded
            If user is not logged in, they are redirected to the login page.
        '''
        #if SESSION._initializer['id'] != web.ACCOUNT_LOGIN_SUCCESSFUL:
        #if self.user_session._initializer.get("id") != web.ACCOUNT_LOGIN_SUCCESSFUL:
        if web.cookies().get('user') is None:
            raise web.seeother('/login')
        else:
            module_infos = model.get_all_modules()
            form = self.form()
            if web.ctx.session._initializer.get('displayErrorMessage') is True:
                web.ctx.session._initializer['displayErrorMessage'] = False
            else:
                web.ctx.session._initializer['keyError'] = False

            return RENDER.index(module_infos, form, web.ctx.session._initializer.get('keyError'))


    def POST(self):
        '''
            This function is called when the 'Add Module' form is submitted
            if form input is invalid, reload the page and shows error message besides field
        '''
        form = self.form()
        if not form.validates():
            modules = model.get_all_modules()
            return RENDER.index(modules, form, web.ctx.session._initializer.get('keyError'))

        # else add module to db and refresh page
        outcome = model.add_module(form.d.code, form.d.name, form.d.description, form.d.mc, 'New')
        if outcome is False:
            web.ctx.session._initializer['keyError'] = True
            web.ctx.session._initializer['displayErrorMessage'] = True
        raise web.seeother('/')        # load index.html again


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
