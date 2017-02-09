########
## model.py
## Handles queries to the database
########

import web
import psycopg2

## Connects to the postgres database
connection = psycopg2.connect(
	database='postgres',
	user='postgres',
	password='12345678',
	host='localhost',
	port='5433'
)
db_cursor = connection.cursor()

## Select all modules from the module table (order by code)
def getAllModules():
	sql_command = "SELECT * FROM module ORDER BY code"
	db_cursor.execute(sql_command)
	return db_cursor.fetchall()
    #return db.select('module', order='code')

## Retrieve the info of a single module
def viewModule(code):
	sql_command = "SELECT * FROM module WHERE code=%s"
	db_cursor.execute(sql_command, (code,))
	return db_cursor.fetchone()
    #return db.select('module', where="code=$code", vars=locals())

## Insert a new module into the module table
def addModule(code, name, description, mc):
	sql_command = "INSERT INTO module (code, name, description, mc)" +  \
		" VALUES (%s,%s,%s,%s)"
	db_cursor.execute(sql_command, (code, name, description, mc))
	connection.commit()
    #db.insert('module', code=code, name=name, description=description, mc=mc)

## Delete a module from the module table
def deleteModule(code):
	# Delete the foreign key reference first.
	sql_command = "DELETE FROM modulemounted WHERE modulecode=%s"
	db_cursor.execute(sql_command, (code,))

	# Perform the normal delete.
	sql_command = "DELETE FROM module WHERE code=%s"
	db_cursor.execute(sql_command, (code,))
	connection.commit()
    #db.delete('module', where="code=$code", vars=locals())
