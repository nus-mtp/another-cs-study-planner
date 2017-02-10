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

## Get the module code, name, description, and MCs of all modules
def getAllModules():
	sql_command = "SELECT * FROM module ORDER BY code"
	db_cursor.execute(sql_command)
	return db_cursor.fetchall()

## Get the module code, name, description and MCs of a single module
def getModule(code):
	sql_command = "SELECT * FROM module WHERE code=%s"
	db_cursor.execute(sql_command, (code,))
	return db_cursor.fetchone()

## Get the module code, name, AY/Sem and quota of all fixed mounted modules
def getAllFixedMountedModules():
	sql_command = "SELECT m2.moduleCode, m1.name, m2.acadYearAndSem, m2.quota FROM module m1, moduleMounted m2 WHERE m2.moduleCode = m1.code ORDER BY m2.moduleCode, m2.acadYearAndSem"
	db_cursor.execute(sql_command)
	return db_cursor.fetchall()

## Get the module code, name, AY/Sem and quota of all tentative mounted modules
def getAllTentativeMountedModules():
	sql_command = "SELECT m2.moduleCode, m1.name, m2.acadYearAndSem, m2.quota FROM module m1, moduleMountTentative m2 WHERE m2.moduleCode = m1.code ORDER BY m2.moduleCode, m2.acadYearAndSem"
	db_cursor.execute(sql_command)
	return db_cursor.fetchall()

## Get the fixed AY/Sem and quota of a mounted module
def getFixedMountingAndQuota(code):
	sql_command = "SELECT acadYearAndSem, quota FROM moduleMounted WHERE moduleCode=%s ORDER BY acadYearAndSem"
	db_cursor.execute(sql_command, (code, ))
	return db_cursor.fetchall()

## Get the tentative AY/Sem and quota of a mounted module
def getTentativeMountingAndQuota(code):
	sql_command = "SELECT acadYearAndSem, quota FROM moduleMountTentative WHERE moduleCode=%s ORDER BY acadYearAndSem"
	db_cursor.execute(sql_command, (code, ))
	return db_cursor.fetchall()

## Insert a new module into the module table
def addModule(code, name, description, mc):
	sql_command = "INSERT INTO module VALUES (%s,%s,%s,%s,'New')"
	db_cursor.execute(sql_command, (code, name, description, mc))
	connection.commit()

## Change the status of a module to 'To Be Removed'
def flagModuleAsRemoved(code):
	sql_command = "UPDATE module SET status='To Be Removed' WHERE code=%s"
	db_cursor.execute(sql_command, (code, ))
	connection.commit()

## Change the status of a module to 'Active'
def flagModuleAsActive(code):
	sql_command = "UPDATE module SET status='Active' WHERE code=%s"
	db_cursor.execute(sql_command, (code, ))
	connection.commit()

## Delete a module from the module table
def deleteModule(code):
	# Delete the foreign key reference first.
	sql_command = "DELETE FROM modulemounted WHERE modulecode=%s"
	db_cursor.execute(sql_command, (code,))

	# Perform the normal delete.
	sql_command = "DELETE FROM module WHERE code=%s"
	db_cursor.execute(sql_command, (code,))
	connection.commit()
