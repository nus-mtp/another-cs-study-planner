import os
import psycopg2
import urlparse

try:
	import local_database_data
except ImportError:
	print ("local_database_data.py file is missing from components folder.")
	print ("Please create it manually")
	local_database_data = None

def connect_db(is_for_deployment):
	connection = None

	if (is_for_deployment):
		# Specifying the postgres SQL and the database for Heroku
		urlparse.uses_netloc.append("postgres")
		url = urlparse.urlparse(os.environ["DATABASE_URL"])

	    # Attempts to connect to the database and returns a connection object.
		connection = psycopg2.connect(
			database = url.path[1:],
			user = url.username,
			password = url.password,
			host = url.hostname,
			port = url.port
		)
	else:
		# Connects to the local postgres database
		connection = psycopg2.connect(
			database = local_database_data.get_database_name(),
			user = local_database_data.get_user_name(),
			password = local_database_data.get_password(),
			host = local_database_data.get_host_name(),
			port = local_database_data.get_port()
		)

	return connection