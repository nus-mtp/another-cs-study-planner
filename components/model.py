'''
    model.py
    Handles queries to the database
'''

import components.database_adapter # database_adaptor.py handles the connection to database
import psycopg2


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


def get_all_tenta_mounted_modules_of_selected_ay(selected_ay):
    '''
        Get the module code, name, AY/Sem and quota of all tenta mounted mods of a selected AY
    '''
    sql_command = "SELECT m2.moduleCode, m1.name, m2.acadYearAndSem, m2.quota " +\
                  "FROM module m1, moduleMountTentative m2 WHERE m2.moduleCode = m1.code " +\
                  "AND M2.acadYearAndSem LIKE '" + selected_ay + "%' " +\
                  "ORDER BY m2.moduleCode, m2.acadYearAndSem"
    DB_CURSOR.execute(sql_command)
    return DB_CURSOR.fetchall()


def get_first_fixed_mounting():
    '''
        Get the first mounting from the fixed mounting table
        This is used for reading the current AY
    '''
    sql_command = "SELECT acadYearAndSem FROM moduleMounted LIMIT(1)"
    DB_CURSOR.execute(sql_command)
    return DB_CURSOR.fetchone()


def get_all_fixed_ay_sems():
    '''
        Get all the distinct AY/Sem in the fixed mounting table
    '''
    sql_command = "SELECT DISTINCT acadYearAndSem FROM moduleMounted " +\
                  "ORDER BY acadYearAndSem ASC"
    DB_CURSOR.execute(sql_command)
    return DB_CURSOR.fetchall()


def get_all_tenta_ay_sems():
    '''
        Get all the distinct AY/Sem in the tentative mounting table
    '''
    sql_command = "SELECT DISTINCT acadYearAndSem FROM moduleMountTentative " +\
                  "ORDER BY acadYearAndSem ASC"
    DB_CURSOR.execute(sql_command)
    return DB_CURSOR.fetchall()


def get_fixed_mounting_and_quota(code):
    '''
        Get the fixed AY/Sem and quota of a mounted module
    '''
    sql_command = "SELECT acadYearAndSem, quota FROM moduleMounted " +\
                  "WHERE moduleCode=%s ORDER BY acadYearAndSem ASC"
    DB_CURSOR.execute(sql_command, (code, ))
    return DB_CURSOR.fetchall()


def get_tenta_mounting_and_quota(code):
    '''
        Get the tentative AY/Sem and quota of a mounted module
    '''
    sql_command = "SELECT acadYearAndSem, quota FROM moduleMountTentative " +\
                  "WHERE moduleCode=%s ORDER BY acadYearAndSem ASC"
    DB_CURSOR.execute(sql_command, (code, ))
    return DB_CURSOR.fetchall()


def get_quota_of_target_fixed_ay_sem(code, ay_sem):
    '''
        Get the quota of a mod in a target fixed AY/Sem (if any)
    '''
    sql_command = "SELECT quota FROM moduleMounted " +\
                  "WHERE moduleCode=%s AND acadYearAndSem=%s "
    DB_CURSOR.execute(sql_command, (code, ay_sem))
    return DB_CURSOR.fetchall()


def get_quota_of_target_tenta_ay_sem(code, ay_sem):
    '''
        Get the quota of a mod in a target tentative AY/Sem (if any)
    '''
    sql_command = "SELECT quota FROM moduleMountTentative " +\
                  "WHERE moduleCode=%s AND acadYearAndSem=%s "
    DB_CURSOR.execute(sql_command, (code, ay_sem))
    return DB_CURSOR.fetchall()


def get_number_students_planning(code):
    '''
        Get the number of students planning to take a mounted module
    '''
    sql_command = "SELECT COUNT(*), acadYearAndSem FROM studentPlans WHERE " +\
                    "moduleCode=%s GROUP BY acadYearAndSem ORDER BY acadYearAndSem"
    DB_CURSOR.execute(sql_command, (code, ))
    return DB_CURSOR.fetchall()


def add_module(code, name, description, module_credits, status):
    '''
        Insert a module into the module table.
        Returns true if successful, false if duplicate primary key detected
    '''
    sql_command = "INSERT INTO module VALUES (%s,%s,%s,%s,%s)"
    try:
        DB_CURSOR.execute(sql_command, (code, name, description, module_credits, status))
        CONNECTION.commit()
    except psycopg2.IntegrityError:        # duplicate key error
        CONNECTION.rollback()
        return False
    return True


def update_module(code, name, description, module_credits):
    '''
        Update a module with edited info
    '''
    sql_command = "UPDATE module SET name=%s, description=%s, mc=%s " +\
                  "WHERE code=%s"
    try:
        DB_CURSOR.execute(sql_command, (name, description, module_credits, code))
        CONNECTION.commit()
    except psycopg2.Error:
        CONNECTION.rollback()
        return False
    return True


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


def add_fixed_mounting(code, ay_sem, quota):
    '''
        Insert a new mounting into fixed mounting table
    '''
    try:
        sql_command = "INSERT INTO modulemounted VALUES (%s,%s,%s)"
        DB_CURSOR.execute(sql_command, (code, ay_sem, quota))
        CONNECTION.commit()
    except psycopg2.IntegrityError:        # duplicate key error
        CONNECTION.rollback()
        return False
    return True


def delete_fixed_mounting(code, ay_sem):
    '''
        Delete a mounting from the fixed mounting table
    '''
    sql_command = "DELETE FROM modulemounted WHERE moduleCode=%s AND acadYearAndSem=%s"
    DB_CURSOR.execute(sql_command, (code, ay_sem))
    CONNECTION.commit()


def add_tenta_mounting(code, ay_sem, quota):
    '''
        Insert a new mounting into tentative mounting table
    '''
    try:
        sql_command = "INSERT INTO moduleMountTentative VALUES (%s,%s,%s)"
        DB_CURSOR.execute(sql_command, (code, ay_sem, quota))
        CONNECTION.commit()
    except psycopg2.IntegrityError:        # duplicate key error
        CONNECTION.rollback()
        return False
    return True


def delete_tenta_mounting(code, ay_sem):
    '''
        Delete a mounting from the tentative mounting table
    '''
    sql_command = "DELETE FROM moduleMountTentative WHERE moduleCode=%s AND acadYearAndSem=%s"
    DB_CURSOR.execute(sql_command, (code, ay_sem))
    CONNECTION.commit()
