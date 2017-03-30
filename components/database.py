'''
    database.py
    Contains functions that directly communicate with or manipulate the database
'''

import hashlib

## Prevent model.py from being imported twice
from sys import modules
try:
    from components import model
except ImportError:
    model = modules['components.model']

import components.database_adapter # database_adaptor.py handles the connection to database
import psycopg2
from psycopg2.extensions import AsIs

## Connects to the postgres database
CONNECTION = components.database_adapter.connect_db()
DB_CURSOR = CONNECTION.cursor()

INDEX_FIRST_ELEM = 0
INDEX_SECOND_ELEM = 1
LENGTH_EMPTY = 0


######################################################################################
# Functions that query general module information
######################################################################################

def get_all_modules():
    '''
        Get the module code, name, description, and MCs of all modules
    '''
    sql_command = "SELECT * FROM module ORDER BY code"
    DB_CURSOR.execute(sql_command)
    return DB_CURSOR.fetchall()


def get_all_modules_and_focus():
    '''
        Get the module code, name, description, MCs,
        and focus areas of all modules
    '''
    sql_command = "SELECT m.*, b.focusArea " +\
                    "FROM module m " +\
                    "LEFT JOIN belongstofocus b " +\
                    "ON m.code = b.ModuleCode " +\
                    "ORDER BY m.code"
    DB_CURSOR.execute(sql_command)
    return DB_CURSOR.fetchall()


def get_module(code):
    '''
        Get the module code, name, description, MCs and status of a single module
    '''
    sql_command = "SELECT * FROM module WHERE code=%s"
    DB_CURSOR.execute(sql_command, (code,))
    return DB_CURSOR.fetchone()


def get_module_name(code):
    '''
        Retrieves the module name of a module given its module code.
    '''
    sql_command = "SELECT name FROM module WHERE code=%s"
    DB_CURSOR.execute(sql_command, (code,))

    return DB_CURSOR.fetchone()[0]


def is_existing_module(code):
    '''
        Returns true if specified module code exists in the database,
        returns false otherwise.
    '''
    sql_command = "SELECT COUNT(*) FROM module WHERE code=%s"
    DB_CURSOR.execute(sql_command, (code,))
    number_module = DB_CURSOR.fetchone()[0]

    return number_module > 0


def get_original_module_info(code):
    '''
        Get the original info of a module from module backup
    '''
    sql_command = "SELECT * FROM moduleBackup WHERE code=%s"
    DB_CURSOR.execute(sql_command, (code, ))
    return DB_CURSOR.fetchone()


def get_new_modules():
    '''
        Get the module code, name, description and MCs of modules with status 'New'
    '''
    sql_command = "SELECT * FROM module WHERE status='New'"
    DB_CURSOR.execute(sql_command)
    return DB_CURSOR.fetchall()


######################################################################################
# Functions that add/modify/delete general module information
######################################################################################

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


def delete_module(code):
    '''
        Delete a newly added module from the module table
        if and only if no (tentative) mountings refer to it.
    '''
    try:
        # Delete backup of module info
        sql_command = "DELETE FROM moduleBackup WHERE code=%s"
        DB_CURSOR.execute(sql_command, (code,))
        # Delete the module
        sql_command = "DELETE FROM module WHERE code=%s"
        DB_CURSOR.execute(sql_command, (code,))
        CONNECTION.commit()

    except psycopg2.Error:  # If module has mounting, module deletion will fail
        CONNECTION.rollback()
        return False

    return True


def store_original_module_info(code, name, description, module_credits):
    '''
        Store the original name, description and MC of a module
        so that 1. Can track which module has been modified, 2. Can reset module to original state
        If original info already exists in table, the original info will NOT be overwritten
        (the primary key constraint will prevent that)
    '''
    sql_command = "INSERT INTO moduleBackup VALUES (%s,%s,%s,%s)"
    try:
        DB_CURSOR.execute(sql_command, (code, name, description, module_credits))
        CONNECTION.commit()
    except psycopg2.IntegrityError:        # duplicate key error
        CONNECTION.rollback()
        return False
    return True


def remove_original_module_info(code):
    '''
        Remove the original info of the module from module backup
        (when the original module info has been restored)
    '''
    sql_command = "DELETE FROM moduleBackup WHERE code=%s"
    DB_CURSOR.execute(sql_command, (code, ))
    CONNECTION.commit()


######################################################################################
# Functions that query mounting and/or quota information
######################################################################################

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
                  "AND M2.acadYearAndSem LIKE %s" + \
                  "ORDER BY m2.moduleCode, m2.acadYearAndSem"
    processed_ay = selected_ay + "%"

    DB_CURSOR.execute(sql_command, (processed_ay,))
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


def get_mounting_of_target_fixed_ay_sem(code, ay_sem):
    '''
        Get the mounting status of a module in a target fixed AY/Sem
    '''
    sql_command = "SELECT COUNT(*) FROM moduleMounted " +\
                  "WHERE moduleCode=%s AND acadYearAndSem=%s"
    DB_CURSOR.execute(sql_command, (code, ay_sem))
    result = DB_CURSOR.fetchone()
    return result[0] == 1    # True == Mounted, False == Not Mounted


def get_mounting_of_target_tenta_ay_sem(code, ay_sem):
    '''
        Get the mounting status of a module in a target tentative AY/Sem
    '''
    sql_command = "SELECT COUNT(*) FROM moduleMountTentative " +\
                  "WHERE moduleCode=%s AND acadYearAndSem=%s"
    DB_CURSOR.execute(sql_command, (code, ay_sem))
    result = DB_CURSOR.fetchone()
    return result[0] == 1    # True == Mounted, False == Not Mounted


def get_quota_of_target_fixed_ay_sem(code, ay_sem):
    '''
        Get the quota of a mod in a target fixed AY/Sem (if any)
    '''
    sql_command = "SELECT quota FROM moduleMounted " +\
                  "WHERE moduleCode=%s AND acadYearAndSem=%s"
    DB_CURSOR.execute(sql_command, (code, ay_sem))
    result = DB_CURSOR.fetchone()
    if result is not None:
        return result[0]
    else:
        return False


def get_quota_of_target_tenta_ay_sem(code, ay_sem):
    '''
        Get the quota of a mod in a target tentative AY/Sem (if any)
    '''
    sql_command = "SELECT quota FROM moduleMountTentative " +\
                  "WHERE moduleCode=%s AND acadYearAndSem=%s"
    DB_CURSOR.execute(sql_command, (code, ay_sem))
    result = DB_CURSOR.fetchone()
    if result is not None:
        return result[0]
    else:
        return False


def get_mod_specified_class_size(given_aysem, quota_lower, quota_higher):
    '''
        Retrieves the list of modules with quota/class size in the
        specified AY-Semester if the quota falls within the given range
        of quota_lower <= retrieved module quota <= quota_higher
    '''
    sql_command = "SELECT mm.moduleCode, m.name, mm.quota " + \
                "FROM %(table)s mm, module m " + \
                "WHERE mm.acadYearAndSem = %(aysem)s " + \
                "AND mm.quota >= %(lower_range)s AND mm.quota <= %(higher_range)s " + \
                "AND mm.moduleCode = m.code"

    STRING_MODULE_MOUNTED = "moduleMounted"
    STRING_MODULE_MOUNT_TENTA = "moduleMountTentative"

    MAP_TABLE_TO_MODULE_MOUNTED = {
        "table": AsIs(STRING_MODULE_MOUNTED),
        "aysem": given_aysem,
        "lower_range": quota_lower,
        "higher_range": quota_higher
    }
    MAP_TABLE_TO_MODULE_MOUNT_TENTA = {
        "table": AsIs(STRING_MODULE_MOUNT_TENTA),
        "aysem": given_aysem,
        "lower_range": quota_lower,
        "higher_range": quota_higher
    }

    fixed_sems = get_all_fixed_ay_sems()
    tenta_sems = get_all_tenta_ay_sems()

    if model.is_aysem_in_list(given_aysem, fixed_sems):
        DB_CURSOR.execute(sql_command, MAP_TABLE_TO_MODULE_MOUNTED)
    elif model.is_aysem_in_list(given_aysem, tenta_sems):
        DB_CURSOR.execute(sql_command, MAP_TABLE_TO_MODULE_MOUNT_TENTA)
    else: # No such aysem found
        return list()

    required_list = DB_CURSOR.fetchall()
    processed_list = model.convert_to_list(required_list)

    return processed_list


######################################################################################
# Functions that add/modify/delete mounting and/or quota information
######################################################################################

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


def update_quota(code, ay_sem, quota):
    '''
        Update the quota of a module in a target tentative AY/Sem
    '''
    sql_command = "UPDATE moduleMountTentative SET quota=%s " +\
                  "WHERE moduleCode=%s AND acadYearAndSem=%s"
    try:
        DB_CURSOR.execute(sql_command, (quota, code, ay_sem))
        CONNECTION.commit()
    except psycopg2.Error:
        CONNECTION.rollback()
        return False
    return True


def delete_tenta_mounting(code, ay_sem):
    '''
        Delete a mounting from the tentative mounting table
    '''
    sql_command = "DELETE FROM moduleMountTentative WHERE moduleCode=%s AND acadYearAndSem=%s"
    try:
        DB_CURSOR.execute(sql_command, (code, ay_sem))
        CONNECTION.commit()
    except psycopg2.Error:
        CONNECTION.rollback()
        return False
    return True


######################################################################################
# Functions that query AY and semester information
######################################################################################

def get_current_ay():
    '''
        Get the current AY from the fixed mounting table.
        All fixed mountings should be from the same AY,
        so just get the AY from the first entry.
        Test case will ensure that all entries in fixed mountings have the same AY
    '''
    sql_command = "SELECT LEFT(acadYearAndSem, 8) FROM moduleMounted LIMIT(1)"
    DB_CURSOR.execute(sql_command)
    return DB_CURSOR.fetchone()[0]


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


######################################################################################
# Functions that query information related to students demand for a module
######################################################################################

def get_number_students_planning(code):
    '''
        Get the number of students planning to take a mounted module
    '''
    sql_command = "SELECT COUNT(*), acadYearAndSem FROM studentPlans WHERE " +\
                  "moduleCode=%s GROUP BY acadYearAndSem ORDER BY acadYearAndSem"
    DB_CURSOR.execute(sql_command, (code, ))
    return DB_CURSOR.fetchall()


def get_number_of_students_taking_module_in_ay_sem(module_code, ay_sem):
    '''
        Retrieves the number of students who have taken or are taking the module
        in the target AY-Sem
    '''
    sql_command = "SELECT COUNT(*) " + \
                  "FROM studentPlans sp " + \
                  "WHERE sp.moduleCode = %s " + \
                  "AND sp.acadYearAndSem = %s " + \
                  "ORDER BY COUNT(*) DESC"

    DB_CURSOR.execute(sql_command, (module_code, ay_sem))

    return DB_CURSOR.fetchone()[0]


def get_list_students_take_module(code, aysem):
    '''
        Retrieves the list of students who take specified module at specified aysem.

        Returns a table of lists. Each list represents a student and it contains
        (matric number, year of study, focus area 1, focus area 2)
    '''

    sql_command_1 = "SELECT sp.studentid, s.year, tfa.focusarea1, tfa.focusarea2 " + \
                    "FROM studentPlans sp, student s, takesFocusArea tfa " + \
                    "WHERE sp.moduleCode = %s AND sp.acadYearAndSem = %s " + \
                    "AND sp.studentid = s.nusnetid AND " + \
                    "sp.studentid = tfa.nusnetid"

    sql_command_2 = "SELECT sp2.studentid, s2.year " + \
                    "FROM studentPlans sp2, student s2 " + \
                    "WHERE sp2.moduleCode = %s AND sp2.acadYearAndSem = %s " + \
                    "AND sp2.studentid = s2.nusnetid " +\
                    "AND sp2.studentid NOT IN ( " +\
                        "SELECT sp.studentid " + \
                        "FROM studentPlans sp, student s, takesFocusArea tfa " + \
                        "WHERE sp.moduleCode = %s AND sp.acadYearAndSem = %s " + \
                        "AND sp.studentid = s.nusnetid AND " + \
                        "sp.studentid = tfa.nusnetid" + \
                    ")"

    DB_CURSOR.execute(sql_command_1, (code, aysem))
    current_list_of_students = DB_CURSOR.fetchall()

    DB_CURSOR.execute(sql_command_2, (code, aysem, code, aysem))
    list_of_students_taking_with_no_focus_areas = DB_CURSOR.fetchall()
    for student in list_of_students_taking_with_no_focus_areas:
        current_list_of_students.append([student[0], student[1], "-", "-"])

    return model.replace_null_with_dash(current_list_of_students)


def get_oversub_mod():
    '''
        Retrieves a list of modules which are oversubscribed.
        Returns module code, module name, AY/Sem, quota, number students interested
        i.e. has more students interested than the quota
    '''
    list_of_oversub_with_info = []
    list_all_mod_info = get_all_modules()

    for module_info in list_all_mod_info:
        mod_code = module_info[0]

        aysem_quota_fixed_list = get_fixed_mounting_and_quota(mod_code)
        aysem_quota_tenta_list = get_tenta_mounting_and_quota(mod_code)
        aysem_quota_merged_list = aysem_quota_fixed_list + \
                                aysem_quota_tenta_list

        num_student_plan_aysem_list = get_number_students_planning(mod_code)
        for num_plan_aysem_pair in num_student_plan_aysem_list:
            num_student_planning = num_plan_aysem_pair[0]
            ay_sem = num_plan_aysem_pair[1]
            real_quota = model.get_quota_in_aysem(ay_sem, aysem_quota_merged_list)

            # ensures that quota will be a number which is not None
            if real_quota is None:
                quota = 0
                real_quota = '?'
            else:
                quota = real_quota

            if num_student_planning > quota:
                module_name = get_module_name(mod_code)
                oversub_info = (mod_code, module_name, ay_sem,
                                real_quota, num_student_planning)
                list_of_oversub_with_info.append(oversub_info)

    return list_of_oversub_with_info


######################################################################################
# Functions that query general student enrollment information
######################################################################################

def get_all_focus_areas():
    '''
        Get all distinct focus areas
    '''
    sql_command = "SELECT DISTINCT name FROM focusarea"
    DB_CURSOR.execute(sql_command)
    return DB_CURSOR.fetchall()


def get_num_students_by_yr_study():
    '''
        Retrieves the number of students at each year of study as a table
        Each row will contain (year, number of students) pair.
        e.g. [(1, 4), (2, 3)] means four year 1 students
        and two year 3 students
    '''
    sql_command = "SELECT year, COUNT(*) FROM student GROUP BY year" + \
                  " ORDER BY year"
    DB_CURSOR.execute(sql_command)

    table_with_non_zero_students = DB_CURSOR.fetchall()
    final_table = model.append_missing_year_of_study(table_with_non_zero_students)

    # Sort the table based on year
    final_table.sort(key=lambda row: row[INDEX_FIRST_ELEM])

    return final_table


def get_num_students_by_focus_area_non_zero():
    '''
        Retrieves the number of students for each focus area as a table,
        if no student is taking that focus area, that row will not be
        returned.
        Each row will contain (focus area, number of students) pair.
        See: get_num_students_by_focus_areas() for more details.
    '''
    sql_command = "SELECT f.name, COUNT(*) FROM focusarea f, takesfocusarea t" + \
                  " WHERE f.name = t.focusarea1 OR f.name = t.focusarea2 GROUP BY f.name"
    DB_CURSOR.execute(sql_command)

    return DB_CURSOR.fetchall()


def get_focus_areas_with_no_students_taking():
    '''
        Retrieves a list of focus areas with no students taking.
    '''
    sql_command = "SELECT f2.name FROM focusarea f2 WHERE NOT EXISTS(" + \
                  "SELECT f.name FROM focusarea f, takesfocusarea t " + \
                  "WHERE (f.name = t.focusarea1 OR f.name = t.focusarea2) " + \
                  "AND f2.name = f.name GROUP BY f.name)"
    DB_CURSOR.execute(sql_command)

    return DB_CURSOR.fetchall()


def get_number_students_without_focus_area():
    '''
        Retrieves the number of students who have not indicated their focus
        area.
    '''
    sql_command = "SELECT COUNT(*) FROM takesfocusarea WHERE " + \
                  "focusarea1 IS NULL AND focusarea2 IS NULL"
    DB_CURSOR.execute(sql_command)

    return DB_CURSOR.fetchone()


def get_num_students_by_focus_areas():
    '''
        Retrieves the number of students for each focus area as a table
        Each row will contain (focus area, number of students) pair
        e.g. [(AI, 4), (Database, 3)] means four students taking AI as
        focus area and three students taking database as focus area.
        Note: A student taking double focus on AI and Database will be
        reflected once for AI and once for database (i.e. double counting)
    '''
    table_with_non_zero_students = get_num_students_by_focus_area_non_zero()
    table_with_zero_students = get_focus_areas_with_no_students_taking()

    temp_table = table_with_non_zero_students

    # Loops through all focus areas with no students taking and add them to
    # the table with (focus area, number of students) pair.
    for focus_area_name in table_with_zero_students:
        temp_table.append((focus_area_name[INDEX_FIRST_ELEM], 0))

    # Sort the table based on focus area
    temp_table.sort(key=lambda row: row[INDEX_FIRST_ELEM])

    # Build the final table with info of students without focus area.
    num_students_without_focus = \
    get_number_students_without_focus_area()[INDEX_FIRST_ELEM]

    temp_table.insert(INDEX_FIRST_ELEM,
                      ("Have Not Indicated", num_students_without_focus))
    final_table = temp_table

    return final_table


######################################################################################
# Functions that add/modify/delete student or student plans
######################################################################################

def add_student(student_id, year_of_study):
    '''
        Add a student into the database
    '''
    sql_command = "INSERT INTO student VALUES(%s, %s)"
    DB_CURSOR.execute(sql_command, (student_id, year_of_study))
    CONNECTION.commit()


def delete_student(student_id):
    '''
        Delete a student from the database
    '''
    sql_command = "DELETE FROM student WHERE nusnetid = %s"
    DB_CURSOR.execute(sql_command, (student_id,))
    CONNECTION.commit()


def add_student_plan(student_id, is_taken, module_code, ay_sem):
    '''
        Add a student plan into the database
    '''
    sql_command = "INSERT INTO studentPlans VALUES(%s, %s, %s, %s)"
    DB_CURSOR.execute(sql_command, (student_id, is_taken, module_code, ay_sem))
    CONNECTION.commit()


def delete_student_plan(student_id, module_code, ay_sem):
    '''
        Delete a student plan from the database
    '''
    sql_command = "DELETE FROM studentPlans WHERE studentId=%s " +\
                  "AND moduleCode=%s AND acadYearAndSem=%s"
    DB_CURSOR.execute(sql_command, (student_id, module_code, ay_sem))
    CONNECTION.commit()


def delete_all_plans_of_student(student_id):
    '''
        Delete all plans by a student from the database
    '''
    sql_command = "DELETE FROM studentPlans WHERE studentId = %s"
    DB_CURSOR.execute(sql_command, (student_id,))
    CONNECTION.commit()


def add_student_focus_area(student_id, focus_area_1, focus_area_2):
    '''
        Add a student's focus area(s) into the database
    '''
    sql_command = "INSERT INTO takesFocusArea VALUES(%s, %s, %s)"
    DB_CURSOR.execute(sql_command, (student_id, focus_area_1, focus_area_2))
    CONNECTION.commit()


def delete_student_focus_area(student_id):
    '''
        Delete a student's focus area(s) from the database
    '''
    sql_command = "DELETE FROM takesFocusArea  WHERE nusnetid = %s"
    DB_CURSOR.execute(sql_command, (student_id,))
    CONNECTION.commit()


######################################################################################
# Functions that retrieve information of modules that are modified
######################################################################################

def get_modules_with_modified_details():
    '''
        Get all modules whose details (name/description/MC) has been modified.
        Return the module's code, old name, old description, old MC,
        current name, current description, and current MC
    '''
    sql_command = "SELECT m1.code, m1.name, m1.description, m1.mc, " +\
                  "m2.name, m2.description, m2.mc " +\
                  "FROM moduleBackup m1, module m2 " +\
                  "WHERE m1.code = m2.code " +\
                  "ORDER BY code ASC"
    DB_CURSOR.execute(sql_command)
    return DB_CURSOR.fetchall()


def get_modules_with_modified_quota():
    '''
        Find modules whose quota in target AY/Sem is different from quota in current AY/Sem
        and return the module code, module name, current AY/Sem, current AY/Sem's quota,
        target AY/Sem, and target AY/Sem's quota
    '''
    sql_command = "SELECT m1.moduleCode, m3.name, m1.acadYearAndSem, m2.acadYearAndSem, " +\
                  "m1.quota, m2.quota " +\
                  "FROM moduleMounted m1, moduleMountTentative m2, module m3 " +\
                  "WHERE m1.moduleCode = m2.moduleCode " +\
                  "AND RIGHT(m1.acadYearAndSem, 1) = RIGHT(m2.acadYearAndSem, 1) " +\
                  "AND (" +\
                  "    m1.quota != m2.quota " +\
                  "    OR (m1.quota IS NULL AND m2.quota IS NOT NULL) " +\
                  "    OR (m2.quota IS NULL AND m1.quota IS NOT NULL) " +\
                  ") " +\
                  "AND m1.moduleCode = m3.code " +\
                  "ORDER BY m1.moduleCode, m1.acadYearAndSem, m2.acadYearAndSem"
    DB_CURSOR.execute(sql_command)
    return DB_CURSOR.fetchall()


######################################################################################
# Functions that query information involving module relations
######################################################################################

def get_mod_taken_together_with(code):
    '''
        Retrieves the list of modules taken together with the specified
        module code in the same semester.

        Returns a table of lists. Each list contains
        (specified module code, specified module name,
        module taken together's code, module taken together's name,
        aySem, number of students)

        e.g. [(CS1010, Programming Methodology, CS1231,
        Discrete Structures, AY 16/17 Sem 1, 5)] means there are 5 students
        taking CS1010 and CS1231 together in AY 16/17 Sem 1.
    '''

    sql_command = "SELECT sp1.moduleCode, m1.name, sp2.moduleCode, m2.name" + \
                  ", sp1.acadYearAndSem, COUNT(*) " + \
                  "FROM studentPlans sp1, studentPlans sp2, module m1, module m2 " + \
                  "WHERE sp1.moduleCode = %s AND " + \
                  "sp2.moduleCode <> sp1.moduleCode AND " + \
                  "sp1.studentId = sp2.studentId AND " + \
                  "sp1.acadYearAndSem = sp2.acadYearAndSem " + \
                  "AND m1.code = sp1.moduleCode AND m2.code = sp2.moduleCode " + \
                  "GROUP BY sp1.moduleCode, m1.name, sp2.moduleCode, m2.name, " + \
                  "sp1.acadYearAndSem " + \
                  "ORDER BY COUNT(*) DESC"

    DB_CURSOR.execute(sql_command, (code,))

    return DB_CURSOR.fetchall()


def get_mod_taken_together_with_mod_and_aysem(code, aysem):
    '''
        Retrieves the list of modules taken together with the specified
        module code in the specified semester.

        Returns a table of lists. Each list contains
        (specified module code, specified module name,
        module taken together's code, module taken together's name,
        number of students)

        e.g. [(CS1010, Programming Methodology, CS1231,
        Discrete Structures, 5)] means there are 5 students
        taking CS1010 and CS1231 together in the specified AY-Semester.
    '''

    sql_command = "SELECT sp1.moduleCode, m1.name, sp2.moduleCode, m2.name" + \
                  ", COUNT(*) " + \
                  "FROM studentPlans sp1, studentPlans sp2, module m1, module m2 " + \
                  "WHERE sp1.moduleCode = %s AND " + \
                  "sp2.moduleCode <> sp1.moduleCode AND " + \
                  "sp1.studentId = sp2.studentId AND " + \
                  "sp1.acadYearAndSem = sp2.acadYearAndSem AND " + \
                  "sp1.acadYearAndSem = %s " + \
                  "AND m1.code = sp1.moduleCode AND m2.code = sp2.moduleCode " + \
                  "GROUP BY sp1.moduleCode, m1.name, sp2.moduleCode, m2.name " + \
                  "ORDER BY COUNT(*) DESC"

    DB_CURSOR.execute(sql_command, (code, aysem))

    return DB_CURSOR.fetchall()


def get_all_mods_taken_together():
    '''
        Retrieves the list of all modules taken together in the same semester.

        Returns a table of lists. Each list contains
        (module 1 code, module 1 name, module 2 code, module 2 name, aySem, number of students)
        where module 1 and module 2 are the 2 mods taken together
        in the same semester.

        e.g. [(CS1010, Programming Methodology, CS1231,
        Discrete Structures, AY 16/17 Sem 1, 5)] means there are 5 students
        taking CS1010 and CS1231 together in AY 16/17 Sem 1.
    '''

    sql_command = "SELECT sp1.moduleCode, m1.name, sp2.moduleCode, m2.name," + \
                  " sp1.acadYearAndSem, COUNT(*) " + \
                  "FROM studentPlans sp1, studentPlans sp2, module m1, module m2 " + \
                  "WHERE sp1.moduleCode < sp2.moduleCode AND " + \
                  "sp1.studentId = sp2.studentId AND " + \
                  "sp1.acadYearAndSem = sp2.acadYearAndSem AND " + \
                  "m1.code = sp1.moduleCode AND m2.code = sp2.moduleCode " + \
                  "GROUP BY sp1.moduleCode, m1.name, sp2.moduleCode, m2.name, " + \
                  "sp1.acadYearAndSem ORDER BY COUNT(*) DESC"

    DB_CURSOR.execute(sql_command)

    return DB_CURSOR.fetchall()


def get_modA_taken_prior_to_modB():
    '''
        Retrieves the list of pairs of modules where there is at least 1 student
        who took module A prior to taking module B.

        By 'took', it means that the 'isTaken' attribute is set to True.

        By 'taking', it means that the 'isTaken' attribute can be set to True or False,
        but the student plan for that module must exist.

        By 'prior', it means that the AY-sem that module A is taken in comes before
        the AY-sem that module B is taken in or planned to be taken to.

        Return module A's code, module A's name, AY-Sem that module A is taken in,
        module B's code, module B's name, AY-Sem that module B is taken in,
        and the number of students who took module A and B in the specified AY-Sems.
    '''
    sql_command = "SELECT sp1.moduleCode, m1.name, sp1.acadYearAndSem, " +\
                  "sp2.moduleCode, m2.name, sp2.acadYearAndSem, COUNT(*) " + \
                  "FROM studentPlans sp1, studentPlans sp2, module m1, module m2 " + \
                  "WHERE sp2.moduleCode <> sp1.moduleCode " + \
                  "AND sp1.studentId = sp2.studentId " + \
                  "AND sp1.acadYearAndSem < sp2.acadYearAndSem " + \
                  "AND sp1.isTaken = True " + \
                  "AND m1.code = sp1.moduleCode " + \
                  "AND m2.code = sp2.moduleCode " + \
                  "GROUP BY sp1.moduleCode, sp2.moduleCode, " +\
                  "sp1.acadYearAndSem, sp2.acadYearAndSem, " + \
                  "m1.name, m2.name " + \
                  "ORDER BY COUNT(*) DESC"

    DB_CURSOR.execute(sql_command)

    return DB_CURSOR.fetchall()


def get_number_of_students_who_took_modA_prior_to_modB(module_A, module_B, module_B_ay_sem):
    '''
        Retrieves the number of students who took module A some time before
        taking module B in a target AY-Sem.

        Meaning, the student has already taken module A, in an AY-Sem that is prior to
        the target AY-Sem that the student is going to take module B in.

        Return the AY-Sem that module A is taken in,
        and the number of students who took module A and B in the specified AY-Sems.
    '''
    sql_command = "SELECT sp1.acadYearAndSem, COUNT(*) " + \
                  "FROM studentPlans sp1, studentPlans sp2 " + \
                  "WHERE sp1.moduleCode = %s " + \
                  "AND sp2.moduleCode = %s " + \
                  "AND sp1.studentId = sp2.studentId " + \
                  "AND sp2.acadYearAndSem = %s " + \
                  "AND sp1.acadYearAndSem < sp2.acadYearAndSem " + \
                  "AND sp1.isTaken = True " + \
                  "GROUP BY sp1.acadYearAndSem " + \
                  "ORDER BY COUNT(*) DESC"

    DB_CURSOR.execute(sql_command, (module_A, module_B, module_B_ay_sem))

    return DB_CURSOR.fetchall()


def get_mod_before_intern(ay_sem):
    '''
        Retrieves a list of modules which is taken by students prior to
        their internship in specified ay_sem.

        Returns a table of lists, each list contains
        (module code, module name, number of students who took)
        where ('CS1010', 'Programming Methodology', 3) means
        3 students have taken CS1010 before their internship on
        specified ay_sem
    '''
    sql_command = "SELECT sp.moduleCode, m.name, COUNT(*) " + \
                  "FROM studentPlans sp, module m " + \
                  "WHERE sp.moduleCode = m.code " + \
                  "AND sp.acadYearAndSem < %s " + \
                  "AND sp.moduleCode <> 'CP3200' AND sp.moduleCode <> 'CP3202' " + \
                  "AND sp.moduleCode <> 'CP3880' " + \
                  "AND EXISTS (" + \
                  "SELECT * FROM studentPlans sp2 " + \
                  "WHERE sp2.acadYearAndSem = %s " + \
                  "AND sp2.studentid = sp.studentid " + \
                  "AND (sp2.moduleCode = 'CP3200' OR sp2.moduleCode = 'CP3202' " + \
                  "OR sp2.moduleCode = 'CP3880')) " + \
                  "GROUP BY sp.moduleCode, m.name"

    DB_CURSOR.execute(sql_command, (ay_sem, ay_sem))

    return DB_CURSOR.fetchall()


def get_mods_no_one_take(aysem):
    '''
        Retrieves the list of all modules which no student take together
        in the specified semester.

        Returns a table of lists. Each list contains
        (module 1 code, module 1 name, module 2 code, module 2 name)
        where module 1 and module 2 are the 2 mods no one takes together
        in the specified semester.

        e.g. [(CS1010, Programming Methodology, CS1231, Discrete Structures)] means
        there are no students taking CS1010 and CS1231 together in specified aysem.
    '''

    sql_command = "SELECT mm1.moduleCode, m1.name, mm2.moduleCode, m2.name " + \
                  "FROM %(table)s mm1, %(table)s mm2, module m1, module m2 WHERE " + \
                  "mm1.moduleCode < mm2.moduleCode AND m1.code = mm1.moduleCode " + \
                  "AND m2.code = mm2.moduleCode AND " + \
                  "mm1.acadYearAndSem = %(aysem)s AND " + \
                  "mm1.acadYearAndSem = mm2.acadYearAndSem AND NOT EXISTS (" + \
                  "SELECT * FROM studentPlans sp1, studentPlans sp2 WHERE " + \
                  "sp1.studentid = sp2.studentid AND sp1.acadYearAndSem = sp2.acadYearAndSem " + \
                  "AND sp1.acadYearAndSem = mm1.acadYearAndSem AND " + \
                  "sp1.moduleCode = mm1.moduleCode AND sp2.moduleCode = mm2.moduleCode)"

    STRING_MODULE_MOUNTED = "moduleMounted"
    STRING_MODULE_MOUNT_TENTA = "moduleMountTentative"

    MAP_TABLE_TO_MODULE_MOUNTED = {
        "table": AsIs(STRING_MODULE_MOUNTED),
        "aysem": aysem
    }
    MAP_TABLE_TO_MODULE_MOUNT_TENTA = {
        "table": AsIs(STRING_MODULE_MOUNT_TENTA),
        "aysem": aysem
    }

    fixed_sems = get_all_fixed_ay_sems()
    tenta_sems = get_all_tenta_ay_sems()

    if model.is_aysem_in_list(aysem, fixed_sems):
        DB_CURSOR.execute(sql_command, MAP_TABLE_TO_MODULE_MOUNTED)
    elif model.is_aysem_in_list(aysem, tenta_sems):
        DB_CURSOR.execute(sql_command, MAP_TABLE_TO_MODULE_MOUNT_TENTA)
    else: # No such aysem found
        return list()

    required_list = DB_CURSOR.fetchall()

    return required_list


######################################################################################
# Functions that query prerequisite or preclusion information
######################################################################################

def get_prerequisite(module_code):
    '''
        Get a prerequisite from the prerequisite table.
    '''
    sql_command = "SELECT index, prerequisiteModuleCode FROM prerequisite WHERE moduleCode = %s"
    DB_CURSOR.execute(sql_command, (module_code,))
    return DB_CURSOR.fetchall()


def get_preclusion(module_code):
    '''
        Get all preclusions of module_code from the precludes table.
    '''
    sql_command = "SELECT precludedByModuleCode FROM precludes WHERE moduleCode = %s"
    DB_CURSOR.execute(sql_command, (module_code,))
    return DB_CURSOR.fetchall()


######################################################################################
# Functions that add/modify/delete prerequisite or preclusion information
######################################################################################

def add_prerequisite(module_code, prereq_code, index, to_commit=True):
    '''
        Insert a prerequisite into the prerequisite table.
        Returns true if successful, false if duplicate primary key detected
    '''
    sql_command = "INSERT INTO prerequisite VALUES (%s,%s,%s)"
    try:
        DB_CURSOR.execute(sql_command, (module_code, prereq_code, index))
        if to_commit:
            CONNECTION.commit()
    except psycopg2.IntegrityError:        # duplicate key error
        CONNECTION.rollback()
        return False
    return True


def delete_prerequisite(module_code, prereq_code):
    '''
        Delete a prerequisite from the prerequisite table.
        Returns true if successful.
    '''
    sql_command = "DELETE FROM prerequisite WHERE moduleCode = %s " +\
                  "AND prerequisiteModuleCode = %s"
    try:
        DB_CURSOR.execute(sql_command, (module_code, prereq_code))
        CONNECTION.commit()
    except psycopg2.IntegrityError:
        CONNECTION.rollback()
        return False
    return True


def delete_all_prerequisite(module_code, to_commit=True):
    '''
        Deletes all prerequisites of the given module_code from the
        prerequisite table.
        Returns true if this operation is successful,
        returns false otherwise.
    '''
    sql_command = "DELETE FROM prerequisite WHERE moduleCode = %s "
    try:
        DB_CURSOR.execute(sql_command, (module_code,))
        if to_commit:
            CONNECTION.commit()
    except psycopg2.IntegrityError:
        CONNECTION.rollback()
        return False
    return True


def edit_prerequisite(module_code, prereq_units):
    '''
        Changes the prerequisites of given module_code into a new
        set of prerequisites found in prereq_units.
        Returns true if successful, false otherwise.
    '''
    outcome = delete_all_prerequisite(module_code, False)
    if not outcome:
        CONNECTION.rollback()
        return False

    # Repopulate the prereqs
    if len(prereq_units) != LENGTH_EMPTY:
        index = INDEX_FIRST_ELEM
        module_list = {}

        for unit in prereq_units:
            for module in unit:
                if module_list.has_key(module):
                    CONNECTION.rollback()
                    return False
                else:
                    outcome = add_prerequisite(module_code, module, index, False)
                    if not outcome:
                        CONNECTION.rollback()
                        return False
                    module_list[module] = True
            index += 1

        try:
            CONNECTION.commit()
        except psycopg2.IntegrityError:
            CONNECTION.rollback()
            return False

    return True


def add_preclusion(module_code, preclude_code):
    '''
        Insert a preclusion into the precludes table.
        Returns true if successful, false if duplicate primary key detected or
        when module precludes itself (i.e. module_code == preclude_code) or
        when invalid module/preclude code is given.
    '''
    if module_code == preclude_code:
        return False

    if not is_existing_module(module_code) or not is_existing_module(preclude_code):
        return False

    sql_command = "INSERT INTO precludes VALUES (%s,%s)"
    try:
        DB_CURSOR.execute(sql_command, (module_code, preclude_code))
        DB_CURSOR.execute(sql_command, (preclude_code, module_code))
        CONNECTION.commit()
    except psycopg2.IntegrityError:        # duplicate key error
        CONNECTION.rollback()
        return False
    return True


def delete_preclusion(module_code, prereq_code):
    '''
        Delete a preclusion from the precludes table.
        Returns true if successful, false otherwise.
    '''
    sql_command = "DELETE FROM precludes WHERE moduleCode = %s " +\
                  "AND precludedByModuleCode = %s"
    try:
        DB_CURSOR.execute(sql_command, (module_code, prereq_code))
        DB_CURSOR.execute(sql_command, (prereq_code, module_code))
        CONNECTION.commit()
    except psycopg2.IntegrityError:
        CONNECTION.rollback()
        return False
    return True


def delete_all_preclusions(module_code, to_commit=True):
    '''
        Deletes all preclusions of the given module_code from the
        precludes table.
        Returns true if this operation is successful,
        returns false otherwise.
    '''
    sql_command = "DELETE FROM precludes WHERE moduleCode = %s " + \
                "OR precludedByModuleCode = %s"
    try:
        DB_CURSOR.execute(sql_command, (module_code, module_code))
        if to_commit:
            CONNECTION.commit()
    except psycopg2.IntegrityError:
        CONNECTION.rollback()
        return False
    return True


######################################################################################
# Functions that are related to starred modules
######################################################################################

def star_module(module_code, staff_id):
    '''
        Insert a module into the starred table.
    '''
    sql_command = "INSERT INTO starred VALUES (%s,%s)"
    try:
        DB_CURSOR.execute(sql_command, (module_code, staff_id))
        CONNECTION.commit()
    except psycopg2.Error:
        CONNECTION.rollback()


def unstar_module(module_code, staff_id):
    '''
        Remove a module from the starred table.
    '''
    sql_command = "DELETE FROM starred WHERE moduleCode = %s AND staffId = %s"
    try:
        DB_CURSOR.execute(sql_command, (module_code, staff_id))
        CONNECTION.commit()
    except psycopg2.Error:
        CONNECTION.rollback()
    CONNECTION.commit()


def get_starred_modules(staff_id):
    '''
        Get all module info of all starred modules.
    '''
    sql_command = "SELECT m.* FROM module m, starred s WHERE s.staffId = %s " +\
                "AND m.code = s.modulecode"
    DB_CURSOR.execute(sql_command, (staff_id,))
    return DB_CURSOR.fetchall()


def is_module_starred(module_code, staff_id):
    '''
        Check if a module is starred by the user.
    '''
    sql_command = "SELECT * FROM starred WHERE moduleCode = %s AND staffId = %s"
    DB_CURSOR.execute(sql_command, (module_code, staff_id))
    starred = DB_CURSOR.fetchall()
    if not starred:
        return False
    else:
        return True


######################################################################################
# Functions that are related to managing user (admin) accounts and the login system
######################################################################################

def add_admin(username, salt, hashed_pass):
    '''
        Register an admin into the database.
        Note: to change last argument to false once
        activation done
    '''
    try:
        sql_command = "INSERT INTO admin VALUES (%s, %s, %s, FALSE, TRUE)"
        DB_CURSOR.execute(sql_command, (username, salt, hashed_pass))
        CONNECTION.commit()
    except psycopg2.DataError: #if username too long
        CONNECTION.rollback()


def is_userid_taken(userid):
    '''
        Retrieves all account ids for testing if a user id supplied
        during account creation
    '''
    sql_command = "SELECT staffid FROM admin WHERE staffID=%s"
    DB_CURSOR.execute(sql_command, (userid,))

    result = DB_CURSOR.fetchall()
    return len(result) != 0


def delete_admin(username):
    '''
        Delete an admin from the database.
    '''
    # Delete the foreign key references first.
    sql_command = "DELETE FROM starred WHERE staffID=%s"
    DB_CURSOR.execute(sql_command, (username,))
    sql_command = "DELETE FROM sessions WHERE staffid=%s"
    DB_CURSOR.execute(sql_command, (username, ))

    sql_command = "DELETE FROM admin WHERE staffID=%s"
    DB_CURSOR.execute(sql_command, (username,))
    CONNECTION.commit()


def validate_admin(username, unhashed_pass):
    '''
        Check if a provided admin-password pair is valid.
    '''
    sql_command = "SELECT salt, password FROM admin WHERE staffID=%s"
    DB_CURSOR.execute(sql_command, (username,))
    admin = DB_CURSOR.fetchall()
    if not admin:
        return False
    else:
        hashed_pass = hashlib.sha512(unhashed_pass + admin[0][0]).hexdigest()
        is_valid = (admin[0][1] == hashed_pass)
        return is_valid


def add_session(username, session_salt):
    '''
        Register a session into the database, overwriting
        existing sessions by same user
    '''
    # Delete existing session, if any
    sql_command = "DELETE FROM sessions WHERE staffid=%s"
    DB_CURSOR.execute(sql_command, (username,))

    sql_command = "INSERT INTO sessions VALUES (%s, %s)"
    DB_CURSOR.execute(sql_command, (username, session_salt))
    CONNECTION.commit()


def validate_session(username, session_id):
    '''
        Check if a provided session-id is valid.
    '''
    sql_command = "SELECT sessionSalt FROM sessions WHERE staffID=%s"
    DB_CURSOR.execute(sql_command, (username,))
    session = DB_CURSOR.fetchall()
    if not session:
        return False
    else:
        hashed_id = hashlib.sha512(username + session[0][0]).hexdigest()
        is_valid = (session_id == hashed_id)
        return is_valid


def clean_old_sessions(date_to_delete):
    '''
        Delete all sessions dating before specified date
    '''
    sql_command = "DELETE FROM sessions WHERE date < %s;"
    try:
        DB_CURSOR.execute(sql_command, (date_to_delete,))
        CONNECTION.commit()
    except psycopg2.Error:
        CONNECTION.rollback()
        return False
    return True
