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
        web.header('X-Frame-Options', 'SAMEORIGIN')
        web.header('X-Content-Type-Options', 'nosniff')
        web.header('X-XSS-Protection', '1')
        if not session.validate_session():
            raise web.seeother('/login')

        input_data = model.validate_input(web.input(), ["code", "aysem"])
        module_code = input_data.code
        ay_sem = input_data.aysem

        student_list = model.get_list_students_take_module(module_code, ay_sem)
        return RENDER.studentsAffectedByModule(module_code, ay_sem, student_list)
