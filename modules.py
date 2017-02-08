########
## modules.py
## Handles the displaying of web pages and the GET/POST actions
########

import web    # web.py (the framework that we are using)
from components import model  # model.py (the other python file that handles our database)


## This is the URL structure, which lists the pages in our webapp.
## Each line represents a page.
## The first string is the URL extension, the 2nd string is the class that will be invoked when the page is loaded
urls = (
    '/', 'Index',
    '/del/(.*)', 'Delete'  # (.*) represents the POST data
)

## This line tells web.py that the html files to be rendered are found in the 'templates' folder
## base.html is like the skeleton of all the other html files
render = web.template.render('templates', base='base')


## This class handles the Add Module form and the displaying of list of modules
class Index:
    ## Creates the Add Module form that will appear in index.html
    form = web.form.Form(
        web.form.Textbox('code', web.form.notnull, 
            description="Code"),
        web.form.Textbox('name', web.form.notnull, 
            description="Name"),
        web.form.Textbox('description', web.form.notnull, 
            description="Description"),
        web.form.Textbox('mc', web.form.notnull, 
            description="MCs"),
        web.form.Button('Add Module'),
    )

    ## This function is called when the '/' page (index.html) is loaded
    def GET(self):
        modules = model.getAllModules()     # Get list of modules from db 
        form = self.form()                  # Add Module form
        return render.index(modules, form)  # Pass the list of modules and Add Module form to index.html for rendering

    ## This function is called when Add Module form is submitted
    def POST(self):
        ## if form input is invalid, reload the page (warning message will be shown besides invalid field)
        form = self.form()
        if not form.validates():  
            modules = model.getModules()
            return render.index(modules, form)

        ## else add module to db and refresh page
        model.addModule(form.d.code, form.d.name, form.d.description, form.d.mc)
        raise web.seeother('/')

## This class handles the deletion of module
class Delete:
    def POST(self, moduleCode):  # moduleCode is obtained from the end of the URL
        model.deleteModule(moduleCode)
        raise web.seeother('/')


## Run the app
app = web.application(urls, globals())
if __name__ == '__main__':
    app.run()
