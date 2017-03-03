'''
	This module contains the handler for web requests pertaining to
	the restoration of a module's information to original state
'''


from app import RENDER, SESSION
import web
from components import model


class RestoreModule(object):
	'''
		This class handles the restoration of module info
	'''
	def POST(self, *test_data):
		'''
			Handles the restoration of module info
		'''
		if test_data:
			data = test_data[0]
		else:
			data = web.input()

		restore_type = data.restoreType
		module_code = data.code
		ay_sem = data.aySem
		quota = data.quota
		if quota == "?":
			quota = None

		if restore_type == "quota":
			outcome = model.update_quota(module_code, ay_sem, quota)
			if outcome is True:
				outcome = True  # Todo: show message

			if not test_data:
				raise web.seeother('/modifiedModules?modifyType=quota')
