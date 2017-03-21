'''
    This module contains the handler to get the students affected by module
    page
'''
from app import RENDER
import web
from components import model, session

class StudentsAffectedByModule(object):
    '''
        call the page with passed in code,  ay-sem, and name.
    '''
    def GET(self):
        '''
            gets the page with code and ay-sem
        '''
        if not session.validate_session():
            raise web.seeother('/login')

        input_data = web.input()

        try:
            module_code = input_data.code
        except AttributeError:
            error = RENDER.notfound('Module code is not specified')
            raise web.notfound(error)
        module_exist = model.is_existing_module(module_code)
        if not module_exist:
            error = RENDER.notfound('Invalid module code "' + module_code + '"')
            raise web.notfound(error)

        try:
            ay_sem = input_data.aysem
        except AttributeError:
            error = RENDER.notfound('AY-Semester is not specified')
            raise web.notfound(error)
        is_aysem_valid = model.is_aysem_in_system(ay_sem)
        if not is_aysem_valid:
            error = RENDER.notfound('Invalid AY-Semester "' + ay_sem + '"')
            raise web.notfound(error)

        student_list = model.get_list_students_take_module(module_code, ay_sem)
        return RENDER.studentsAffectedByModule(module_code, ay_sem, student_list)
