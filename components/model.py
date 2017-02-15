'''
    model.py
    Handles queries to the database
'''

import components.database_adapter # database_adaptor.py handles the connection to database

## Connects to the postgres database
CONNECTION = components.database_adapter.connect_db()
DB_CURSOR = CONNECTION.cursor()


def get_all_modules():
    '''
        Get the module code, name, description, and MCs of all modules
    '''
    sql_command = "SELECT * FROM module ORDER BY code"
    DB_CURSOR.execute(sql_command)
    return DB_CURSOR.fetchall()


def get_module(code):
    '''
        Get the module code, name, description and MCs of a single module
    '''
    sql_command = "SELECT * FROM module WHERE code=%s"
    DB_CURSOR.execute(sql_command, (code,))
    return DB_CURSOR.fetchone()


def get_all_fixed_mounted_modules():
    '''
        Get the module code, name, AY/Sem and quota of all fixed mounted modules
    '''
    sql_command = "SELECT m2.moduleCode, m1.name, m2.acadYearAndSem, m2.quota " +\
                    "FROM module m1, moduleMounted m2 WHERE m2.moduleCode = m1.code " +\
                    "ORDER BY m2.moduleCode, m2.acadYearAndSem"
    DB_CURSOR.execute(sql_command)
    return DB_CURSOR.fetchall()


def get_all_tenta_mounted_modules():
    '''
        Get the module code, name, AY/Sem and quota of all tentative mounted modules
    '''
    sql_command = "SELECT m2.moduleCode, m1.name, m2.acadYearAndSem, m2.quota " +\
                    "FROM module m1, moduleMountTentative m2 WHERE m2.moduleCode = m1.code " +\
                    "ORDER BY m2.moduleCode, m2.acadYearAndSem"
    DB_CURSOR.execute(sql_command)
    return DB_CURSOR.fetchall()


def get_fixed_mounting_and_quota(code):
    '''
        Get the fixed AY/Sem and quota of a mounted module
    '''
    sql_command = "SELECT acadYearAndSem, quota FROM moduleMounted " +\
                    "WHERE moduleCode=%s ORDER BY acadYearAndSem"
    DB_CURSOR.execute(sql_command, (code, ))
    return DB_CURSOR.fetchall()


def get_tenta_mounting_and_quota(code):
    '''
        Get the tentative AY/Sem and quota of a mounted module
    '''
    sql_command = "SELECT acadYearAndSem, quota FROM moduleMountTentative " +\
                    "WHERE moduleCode=%s ORDER BY acadYearAndSem"
    DB_CURSOR.execute(sql_command, (code, ))
    return DB_CURSOR.fetchall()


def get_number_students_planning(code):
    '''
        Get the number of students planning to take a mounted module
    '''
    sql_command = "SELECT COUNT(*), acadYearAndSem FROM studentPlans WHERE " +\
                    "moduleCode=%s GROUP BY acadYearAndSem ORDER BY acadYearAndSem"
    DB_CURSOR.execute(sql_command, (code, ))
    return DB_CURSOR.fetchall()


def add_module(code, name, description, module_credits):
    '''
        Insert a new module into the module table
    '''
    sql_command = "INSERT INTO module VALUES (%s,%s,%s,%s,'New')"
    DB_CURSOR.execute(sql_command, (code, name, description, module_credits))
    CONNECTION.commit()


def flag_module_as_removed(code):
    '''
        Change the status of a module to 'To Be Removed'
    '''
    sql_command = "UPDATE module SET status='To Be Removed' WHERE code=%s"
    DB_CURSOR.execute(sql_command, (code, ))
    CONNECTION.commit()


def flag_module_as_active(code):
    '''
        Change the status of a module to 'Active'
    '''
    sql_command = "UPDATE module SET status='Active' WHERE code=%s"
    DB_CURSOR.execute(sql_command, (code, ))
    CONNECTION.commit()


def delete_module(code):
    '''
        Delete a module from the module table
    '''
    # Delete the foreign key reference first.
    sql_command = "DELETE FROM modulemounted WHERE modulecode=%s"
    DB_CURSOR.execute(sql_command, (code,))

    # Perform the normal delete.
    sql_command = "DELETE FROM module WHERE code=%s"
    DB_CURSOR.execute(sql_command, (code,))
    CONNECTION.commit()


def add_admin(username, hashed_pass):
    '''
        Register an admin into the database.
        Note: to change last argument to false once
        activation done
    '''
    sql_command = "INSERT INTO admin VALUES (%s, %s, FALSE, TRUE)"
    DB_CURSOR.execute(sql_command, (username, hashed_pass))
    CONNECTION.commit()


def delete_admin(username):
    '''
        Delete an admin from the database.
    '''
    # Delete the foreign key references first.
    sql_command = "DELETE FROM starred WHERE staffID=%s"
    DB_CURSOR.execute(sql_command, (username,))

    sql_command = "DELETE FROM admin WHERE staffID=%s"
    DB_CURSOR.execute(sql_command, (username,))
    CONNECTION.commit()


def validate_admin(username, hashed_pass):
    '''
        Check if a provided admin-password pair is valid.
    '''
    sql_command = "SELECT password FROM admin WHERE staffID=%s"
    DB_CURSOR.execute(sql_command, (username,))
    admin = DB_CURSOR.fetchall()
    if not admin:
        return False
    else:
        is_valid = (admin[0][0] == hashed_pass)
        return is_valid
