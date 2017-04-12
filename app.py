#!/usr/bin/env python

'''
    This module creates an application instance with a configured URL router.
'''


import web
from components import database

'''
    These mappings define to which class the application will direct
    user requests to. Each mapping is in the form:

        'URL regex' --> 'Class name'

    For example, if a user requests for a page in the application
    using the URL '/modules', it will be handled by the 'Modules' class.
'''
URLS = (
    '/', 'components.handlers.index.Index',
    '/modules', 'components.handlers.module_listing.Modules',
    '/moduleMountingFixed', 'components.handlers.fixed_module_mountings.Fixed',
    '/moduleMountingTentative', 'components.handlers.tentative_module_mountings.Tentative',
    '/viewModule', 'components.handlers.module_overview.ViewMod',
    '/flagAsRemoved/(.*)', 'components.handlers.module_listing.FlagAsRemoved',
    '/flagAsActive/(.*)', 'components.handlers.module_listing.FlagAsActive',
    '/deleteModule', 'components.handlers.delete_module.DeleteMod',
    '/editModule', 'components.handlers.module_edit.EditModuleInfo',
    '/editModulePrerequisites', 'components.handlers.module_edit_prerequisites.EditModulePrerequisites',
    '/editModulePreclusions', 'components.handlers.module_edit_preclusions.EditModulePreclusions',
    '/editMounting', 'components.handlers.module_edit.EditMountingInfo',
    '/individualModuleInfo', 'components.handlers.module_view_in_ay_sem.IndividualModule',
    '/oversubscribedModules', 'components.handlers.oversub_mod.OversubModule',
    '/login', 'components.handlers.login.Login',
    '/register', 'components.handlers.register.Register',
    '/logout', 'components.handlers.logout.Logout',
    '/studentEnrollment', 'components.handlers.student_enrollment.StudentEnrollmentQuery',
    '/modifiedModules', 'components.handlers.modified_modules.Modified',
    '/restoreModule', 'components.handlers.module_restore.RestoreModule',
    '/overlappingModules', 'components.handlers.overlapping_modules.OverlappingModules',
    '/outcome', 'components.handlers.outcome.Outcome',
    '/studentsAffectedByModule', 'components.handlers.students_affected_by_module.StudentsAffectedByModule',
    '/addModule', 'components.handlers.add_module_handler.AddModule',
    '/moduleTakenPriorToOthers', 'components.handlers.module_taken_prior_to_others.TakePriorTo',
    '/overlappingWithModule', 'components.handlers.overlapping_with_module.OverlappingWithModule',
    '/nonOverlappingModules', 'components.handlers.non_overlapping_modules.NonOverlappingModules',
    '/moduleSpecificSize', 'components.handlers.module_specific_size.ModuleSpecificSize',
    '/starModule', 'components.handlers.star_modules.StarModule',
    '/starredModules', 'components.handlers.star_modules.StarredModulesList',
    '/moduleTakenPriorToInternship', 'components.handlers.modules_taken_prior_to_internship.TakePriorInternship',
    '/migrateDatabase', 'components.handlers.database_migrate.DatabaseMigrate',
    '/editAll', 'components.handlers.edit_all_mountings_and_quotas.EditAll'
)


all_modules = None
RENDER = web.template.render('templates', base='base')

def set_template():
    '''
        all_modules: 
        A list of all modules, to be used for autocompleting module search

        RENDER: 
        Defines the directory where the application should access
        to render its webpage templates. 
        In this case, this tells the application that it should access the 'templates' directory 
        and use the 'base.html' as the base template for all other pages.
        Also set the global variables to be used across all templates.
    '''    
    global all_modules
    global RENDER

    all_modules = database.get_all_modules()
    RENDER._cache = {}
    RENDER._add_global(web, name="web")
    RENDER._add_global(all_modules, name="all_modules")

set_template()


'''
    Set debug mode
'''
web.config.debug = False


'''
    This creates the application instance with the defined
    URL routing mappings, and global variables that are obtained using
    globals().
'''
APP = web.application(URLS, globals())


def notfound():
    '''
        This function handles general '404 Not Found' error.
        When a non-existing URL is being accessed,
        this will render the 404 page with a general error message.

        For more specific errors in the URL (e.g. invalid/missing GET inputs),
        the rendering of 404 is handled by the validate_input method in model.py
    '''
    return web.notfound(str(RENDER.notfound(
        message="The page you specified with the URL does not exist.")))

APP.notfound = notfound


if __name__ == '__main__':
    APP.run()
