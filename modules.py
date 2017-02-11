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
    '/modules', 'Modules',
    '/moduleMountingFixed', 'Fixed',
    '/moduleMountingTentative', 'Tentative',
    '/viewModule', 'ViewMod',
    '/flagAsRemoved/(.*)', 'FlagAsRemoved',
    '/flagAsActive/(.*)', 'FlagAsActive',
    '/deleteModule/(.*)', 'DeleteMod',
    '/individualModuleInfo?(.*)', 'IndividualModule'
    # (.*) represents the POST data
)

## This line tells web.py that the html files to be rendered are found in the 'templates' folder
## base.html is like the skeleton of all the other html files
render = web.template.render('templates', base='base')


## This class handles the Add Module form and the displaying of list of modules
class Index:
    ## Creates the 'Add Module' form that will appear on the webpage
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
        moduleInfos = model.getAllModules()
        form = self.form()
        return render.index(moduleInfos, form)

    ## This function is called when the 'Add Module' form is submitted
    def POST(self):
        ## if form input is invalid, reload the page (warning message will be shown besides invalid field)
        form = self.form()
        if not form.validates():
            modules = model.getAllModules()
            return render.index(modules, form)

        ## else add module to db and refresh page
        model.addModule(form.d.code, form.d.name, form.d.description, form.d.mc)
        raise web.seeother('/')  # load index.html again

## This class redirects to index.html
class Modules:
    def POST(self):
        raise web.seeother('/')


## This class handles the displaying of the fixed module mountings
class Fixed:
    def GET(self):
        mountedModuleInfos = model.getAllFixedMountedModules()
        return render.moduleMountingFixed(mountedModuleInfos)

    def POST(self):
        raise web.seeother('/moduleMountingFixed')
    

## This class handles the displaying of the tentative module mountings
class Tentative:
    def GET(self):
        mountedModuleInfos = model.getAllTentativeMountedModules()
        return render.moduleMountingTentative(mountedModuleInfos)

    def POST(self):
        raise web.seeother('/moduleMountingTentative')

## This class handles the viewing of a single module
class ViewMod:
    def GET(self):
        inputData = web.input()
        moduleCode = inputData.code
        moduleInfo = model.getModule(moduleCode)
        fixedMountingAndQuota = model.getFixedMountingAndQuota(moduleCode)
        tentativeMountingAndQuota = model.getTentativeMountingAndQuota(moduleCode)
        return render.viewModule(moduleInfo, fixedMountingAndQuota, tentativeMountingAndQuota)
    
## This class handles the desplay on a single module mounting
class IndividualModule:
    def GET(code, ay):
        print(code)
        print(ay)
        inputData = web.input()
        moduleCode = inputData.code
        moduleInfo = model.getModule(moduleCode)
        targetAY = inputData.targetAY
        return render.individualModuleInfo(moduleInfo, targetAY)
    
    def POST(self):
        print(code)
        print(ay)
        print("hello")
        """inputData = web.input()
        moduleCode = inputData.code
        moduleInfo = model.getModule(coduleCode)
        targetAY = inputData.targetAY"""
        raise web.seeother('/individualModuleInfo?code=' + code + '&targetAY=' + ay)

## This class handles the flagging of a module as 'To Be Removed'
class FlagAsRemoved:
    def POST(self, moduleCode):
        model.flagModuleAsRemoved(moduleCode)
        raise web.seeother('/') 


## This class handles the flagging of a module as 'Active'
class FlagAsActive:
    def POST(self, moduleCode):
        model.flagModuleAsActive(moduleCode)
        raise web.seeother('/') 


## This class handles the deletion of module
class DeleteMod:
    def POST(self, moduleCode):  # moduleCode is obtained from the end of the URL
        model.deleteModule(moduleCode)
        raise web.seeother('/')


## Run the app
app = web.application(urls, globals())
if __name__ == '__main__':
    app.run()
