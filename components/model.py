########
## model.py
## Handles queries to the database
########

import web

## Connects to the postgres database
db = web.database(dbn='postgres', db='postgres', user='postgres', pw='super', port='5433')

## Select all modules from the module table (order by code)
def getAllModules():
    return db.select('module', order='code')

## Retrieve the info of a single module
def viewModule(code):
    return db.select('module', where="code=$code", vars=locals())

## Insert a new module into the module table
def addModule(code, name, description, mc):
    db.insert('module', code=code, name=name, description=description, mc=mc)

## Delete a module from the module table
def deleteModule(code):
    db.delete('module', where="code=$code", vars=locals())
