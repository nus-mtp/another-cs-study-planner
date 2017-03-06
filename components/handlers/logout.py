'''
	This module contains the handler for logging out of the system.
'''

from app import RENDER
import web
from components import model

class Logout(object):


	def POST(self):
		'''
			This function destroys all cookies related to user session.
		'''
		web.ctx.session._initializer['loginStatus'] = web.ACCOUNT_LOGGED_OUT
		web.ctx.session.kill()
		web.setcookie('user', '', expires=-1)
		raise web.seeother('/login')