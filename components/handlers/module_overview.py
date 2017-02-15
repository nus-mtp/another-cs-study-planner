'''
    This module contains the handler for web requests pertaining to
    a module's information overview.
'''


import web


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
