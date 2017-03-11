'''
    This module contains the handler to get the students affected by module
    page
'''
from app import RENDER, SESSION
import web
from components import model

class StudentsAffectedByModule(object):
    '''
        call the page with passed in code,  ay-sem, and name.
    '''
    def GET(self):
        '''
            gets the page with code and ay-sem
        '''
        if SESSION['id'] != web.ACCOUNT_LOGIN_SUCCESSFUL:
            raise web.seeother('/login')
        input_data = web.input()
        module_code = input_data.code
        ay_sem = input_data.aysem
        student_list = model.get_list_students_take_module(module_code, ay_sem)
        return RENDER.studentsAffectedByModule(module_code, ay_sem, student_list)
