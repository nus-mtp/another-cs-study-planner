'''
    Run this file with "python dbclean.py" at the command prompt
    in order to automatic clean the database by dropping all
    existing tables, followed by repopulating all tables
    with the necessary data in the database.
'''

import components.database_adapter
import psycopg2

print "connecting to the database..."

CONNECTION = components.database_adapter.connect_db()
DB_CURSOR = CONNECTION.cursor()

print "Connected!"
print "Attempting to drop database..."

file_to_clean_database = open('utils/databaseClean.sql', 'r')
lines_to_clean_database = file_to_clean_database.readlines()[0]
sql_list = lines_to_clean_database.split(";\r")

for sql_drop_table_line in sql_list:
    print sql_drop_table_line
    if sql_drop_table_line == "":
        continue
    try:
        DB_CURSOR.execute(sql_drop_table_line)
        CONNECTION.commit()
    except psycopg2.Error:
        CONNECTION.rollback()
file_to_clean_database.close()

print "All tables dropped"
print "Repopulating database..."

components.database_adapter.repopulate_database(CONNECTION)

print "Completed!"
