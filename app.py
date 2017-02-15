'''
    This module creates an application instance with a configured URL router.
'''


from components import database_adapter, model
from components.handlers import *
import web


'''
    These mappings define to which class the application will direct
    user requests to. Each mapping is in the form:

        'URL regex' --> 'Class name'

    For example, if a user requests for a page in the application
    using the URL '/modules', it will be handled by the 'Modules' class.
'''
URLS = (
    '/', 'modules.Index',
    '/modules', 'modules.Modules',
    '/moduleMountingFixed', 'modules.Fixed',
    '/moduleMountingTentative', 'modules.Tentative',
    '/viewModule', 'modules.ViewMod',
    '/flagAsRemoved/(.*)', 'modules.FlagAsRemoved',
    '/flagAsActive/(.*)', 'modules.FlagAsActive',
    '/deleteModule/(.*)', 'modules.DeleteMod',
    '/individualModuleInfo', 'modules.IndividualModule'
)


'''
    This defines the directory where the application should access
    to render its webpage templates.

    In this case, this tells the application that it should access the
    'templates' directory and use the 'base.html' as the base template
    for all other pages.
'''
RENDER = web.template.render('templates', base='base')


'''
    This creates the application instance with the defined
    URL routing mappings, and global variables that are obtained using
    globals().
'''
APP = web.application(URLS, globals())


if __name__ == '__main__':
    APP.run()
