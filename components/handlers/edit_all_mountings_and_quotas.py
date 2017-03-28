'''
    This module contains the handler for web requests pertaining to the
    'Edit All Mountings and Quotas' page
'''


from app import RENDER
import web
from components import model, session
from components.handlers.tentative_module_mountings import Tentative


class EditAll(object):
    '''
        This class contains the implementations of the GET and POST requests.
        for the 'Edit All Mountings and Quotas' page
    '''
    def replace_empty_quota_with_symbols(self, mounting_plan):
        '''
            Replace all quota values with '-' (if not mounted)
            or '?' (if mounted)
        '''
        mounting_plan = model.convert_to_list(mounting_plan)
        for subplan in mounting_plan:
            sem1_quota = subplan[4]
            if sem1_quota is None:
                sem1_mounting = subplan[2]
                if sem1_mounting == 1:
                    subplan[4] = '?'
                else:
                    subplan[4] = '-'
            sem2_quota = subplan[5]
            if sem2_quota is None:
                sem2_mounting = subplan[3]
                if sem2_mounting == 1:
                    subplan[5] = '?'
                else:
                    subplan[5] = '-'
        return mounting_plan


    def GET(self):
        '''
            Renders the 'Edit All Mountings and Quotas' page if users requested
            for the page through the GET method.
        '''
        if not session.validate_session():
            raise web.seeother('/login')

        # Currently, tentative mounting will be shown for the next AY
        selected_ay = model.get_next_ay(model.get_current_ay())

        tenta_mounting_handler = Tentative()
        tenta_mounting_handler.populate_module_code_and_name()
        tenta_mounting_handler.populate_mounting_values(selected_ay)
        full_mounting_plan = tenta_mounting_handler.full_mounting_plan
        full_mounting_plan = self.replace_empty_quota_with_symbols(full_mounting_plan)

        return RENDER.editAll(selected_ay, full_mounting_plan)