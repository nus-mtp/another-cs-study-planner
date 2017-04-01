# To manually configure all this data with your local postgres
# This file needs not be committed.
database_name = 'postgres'    # change this to the name of your database. By default we use 'postgres'.
user_name = 'postgres'        # change this to the username of your database user. By default we use 'postgres'.
password = '12345678'         # change this to the password of your database user, if required.
host_name = 'localhost'
port = '5432'                 # change this to the port number that is used by PostgreSQL on your machine.

def get_database_name():
	return database_name

def get_user_name():
	return user_name

def get_password():
	return password

def get_host_name():
	return host_name

def get_port():
	return port
