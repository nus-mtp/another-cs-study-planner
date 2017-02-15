'''
    modules.py
    Handles the displaying of web pages and the GET/POST actions
'''


import web        # web.py (the framework that we are using)
from components import model        # model.py (the other python file that handles our database)

# This is the URL structure, which lists the pages in our webapp.
# Each line represents a page.
# The first string is the URL extension.
# The 2nd string is the class that will be invoked when the page is loaded.
URLS = (
    '/', 'Index',
    '/modules', 'Modules',
    '/moduleMountingFixed', 'Fixed',
    '/moduleMountingTentative', 'Tentative',
    '/viewModule', 'ViewMod',
    '/flagAsRemoved/(.*)', 'FlagAsRemoved',
    '/flagAsActive/(.*)', 'FlagAsActive',
    '/deleteModule/(.*)', 'DeleteMod',
    '/individualModuleInfo', 'IndividualModule',
    '/login', 'components.login.Login'
    # (.*) represents the POST data
)


# This line tells web.py that the html files to be rendered are found in the 'templates' folder
# base.html is like the skeleton of all the other html files
RENDER = web.template.render('templates', base='base')


class Index(object):
    '''
        This class handles the 'Add Module' form and the displaying of list of modules
    '''
    def __init__(self):
        self.form = self.create_form()


    def GET(self):
        ''' This function is called when the '/' page (index.html) is loaded '''
        module_infos = model.get_all_modules()
        form = self.form()
        return RENDER.index(module_infos, form)


    def POST(self):
        '''
            This function is called when the 'Add Module' form is submitted
            if form input is invalid, reload the page and shows error message besides field
        '''
        form = self.form()
        if not form.validates():
            modules = model.get_all_modules()
            return RENDER.index(modules, form)

        # else add module to db and refresh page
        model.add_module(form.d.code, form.d.name, form.d.description, form.d.mc)
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


class Modules(object):
    '''
        This class redirects to index.html
    '''
    def GET(self):
        ''' Redirect '''
        raise web.seeother('/')


    def POST(self):
        ''' Redirect '''
        raise web.seeother('/')


class Fixed(object):
    '''
        This class handles the displaying of the fixed module mountings
    '''
    def GET(self):
        ''' Display list of fixed module mountigs '''
        mounted_module_infos = model.get_all_fixed_mounted_modules()
        return RENDER.moduleMountingFixed(mounted_module_infos)


    def POST(self):
        ''' Redirect '''
        raise web.seeother('/moduleMountingFixed')


class Tentative(object):
    '''
        This class handles the displaying of the tenta module mountings
    '''
    def GET(self):
        ''' Display list of tenta module mountigs '''
        mounted_module_infos = model.get_all_tenta_mounted_modules()
        return RENDER.moduleMountingTentative(mounted_module_infos)


    def POST(self):
        ''' Redirect '''
        raise web.seeother('/moduleMountingTentative')



class ViewMod(object):
    '''
        This class handles the display of a single module
    '''
    def GET(self):
        ''' Retrieve and render all the info of a module '''
        input_data = web.input()
        module_code = input_data.code
        module_info = model.get_module(module_code)
        fixed_mounting_and_quota = model.get_fixed_mounting_and_quota(module_code)
        tenta_mounting_and_quota = model.get_tenta_mounting_and_quota(module_code)
        number_of_student_planning = model.get_number_students_planning(module_code)
        return RENDER.viewModule(module_info, fixed_mounting_and_quota,
                                 tenta_mounting_and_quota, number_of_student_planning)


    def POST(self):
        ''' Redirect '''
        raise web.seeother('/')


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


class FlagAsRemoved(object):
    '''
        This class handles the flagging of a module as 'To Be Removed'
    '''
    def GET(self):
        ''' Redirect '''
        raise web.seeother('/')


    def POST(self, module_code):
        ''' Flag module as removed '''
        model.flag_module_as_removed(module_code)
        raise web.seeother('/')


class FlagAsActive(object):
    '''
        This class handles the flagging of a module as 'Active'
    '''
    def GET(self):
        ''' Redirect '''
        raise web.seeother('/')


    def POST(self, module_code):
        ''' Flag module as active '''
        model.flag_module_as_active(module_code)
        raise web.seeother('/')


class DeleteMod(object):
    '''
        This class handles the deletion of module
    '''
    def GET(self):
        ''' Redirect '''
        raise web.seeother('/')


    def POST(self, module_code):        # module_code is obtained from the end of the URL
        ''' Delete the module '''
        model.delete_module(module_code)
        raise web.seeother('/')



# Run the app
APP = web.application(URLS, globals())
if __name__ == '__main__':
    APP.run()
