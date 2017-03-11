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
		web.setcookie('user', '', expires=-1)
		web.setcookie('session_id', '', expires=-1)
		raise web.seeother('/login')