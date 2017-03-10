'''
    This module creates an application instance with a configured URL router.
'''


import web


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
    '/deleteModule/(.*)', 'components.handlers.module_listing.DeleteMod',
    '/editModule', 'components.handlers.module_edit.EditModuleInfo',
    '/editMounting', 'components.handlers.module_edit.EditMountingInfo',
    '/individualModuleInfo', 'components.handlers.module_view_in_ay_sem.IndividualModule',
    '/oversubscribedModules', 'components.handlers.oversub_mod.OversubModule',
    '/login', 'components.handlers.login.Login',
    '/verifyLogin', 'components.handlers.login.verifyLogin',
    '/studentEnrollment', 'components.handlers.student_enrollment.StudentEnrollmentQuery',
    '/modifiedModules', 'components.handlers.modified_modules.Modified',
    '/restoreModule', 'components.handlers.module_restore.RestoreModule',
    '/overlappingModules', 'components.handlers.overlapping_modules.OverlappingModules',
    '/outcome', 'components.handlers.outcome.Outcome',
    '/modulesTakenPriorToAnother', 'components.handlers.take_module_prior_to_another.TakePriorTo'
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


'''
    Variables for handling accounts page.
'''
web.ACCOUNT_CREATED_SUCCESSFUL = 1
web.ACCOUNT_CREATED_UNSUCCESSFUL = -1
web.ACCOUNT_LOGIN_SUCCESSFUL = 2
web.ACCOUNT_LOGIN_UNSUCCESSFUL = -2

web.config.session_parameters['ignore_expiry'] = False

SESSION = web.session.Session(APP, web.session.DiskStore('sessions'),
                              initializer={'id': None})._initializer


if __name__ == '__main__':
    APP.run()
