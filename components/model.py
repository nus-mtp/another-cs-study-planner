'''
    model.py
    Handles queries to the database
'''

import hashlib
import components.database_adapter # database_adaptor.py handles the connection to database
import psycopg2
from psycopg2.extensions import AsIs

## Connects to the postgres database
CONNECTION = components.database_adapter.connect_db()
DB_CURSOR = CONNECTION.cursor()

INDEX_FIRST_ELEM = 0
INDEX_SECOND_ELEM = 1
LENGTH_EMPTY = 0

def get_all_modules():
    '''
        Get the module code, name, description, and MCs of all modules
    '''
    sql_command = "SELECT * FROM module ORDER BY code"
    DB_CURSOR.execute(sql_command)
    return DB_CURSOR.fetchall()


def get_module(code):
    '''
        Get the module code, name, description, MCs and status of a single module
    '''
    sql_command = "SELECT * FROM module WHERE code=%s"
    DB_CURSOR.execute(sql_command, (code,))
    return DB_CURSOR.fetchone()


def is_existing_module(code):
    '''
        Returns true if specified module code exists in the database,
        returns false otherwise.
    '''
    sql_command = "SELECT COUNT(*) FROM module WHERE code=%s"
    DB_CURSOR.execute(sql_command, (code,))
    number_module = DB_CURSOR.fetchone()[0]

    return number_module > 0


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


def get_next_ay(ay):
    '''
        Return the AY that comes after the given AY
    '''
    ay = ay.split(' ')[1].split('/')
    return 'AY ' + str(int(ay[0])+1) + '/' + str(int(ay[1])+1)


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


def store_original_module_info(code, name, description, module_credits):
    '''
        Store the original name, description and MC of a module
        so that 1. Can track which module has been modified, 2. Can reset module to original state
        If original info already exists in table, the original info will NOT be overwritten
        (the prmary key constraint will prevent that)
    '''
    sql_command = "INSERT INTO moduleBackup VALUES (%s,%s,%s,%s)"
    try:
        DB_CURSOR.execute(sql_command, (code, name, description, module_credits))
        CONNECTION.commit()
    except psycopg2.IntegrityError:        # duplicate key error
        CONNECTION.rollback()
        return False
    return True


def get_original_module_info(code):
    '''
        Get the original info of a module from module backup
    '''
    sql_command = "SELECT * FROM moduleBackup WHERE code=%s"
    DB_CURSOR.execute(sql_command, (code, ))
    return DB_CURSOR.fetchone()


def remove_original_module_info(code):
    '''
        Remove the original info of the module from module backup
        (when the original module info has been restored)
    '''
    sql_command = "DELETE FROM moduleBackup WHERE code=%s"
    DB_CURSOR.execute(sql_command, (code, ))
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


def get_module_name(code):
    '''
        Retrieves the module name of a module given its module code.
    '''
    sql_command = "SELECT name FROM module WHERE code=%s"
    DB_CURSOR.execute(sql_command, (code,))

    return DB_CURSOR.fetchone()[0]


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
            real_quota = get_quota_in_aysem(ay_sem, aysem_quota_merged_list)

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


def get_quota_in_aysem(ay_sem, aysem_quota_merged_list):
    '''
        This is a helper function.
        Retrieves the correct quota from ay_sem listed inside
        aysem_quota_merged_list parameter.
    '''
    for aysem_quota_pair in aysem_quota_merged_list:
        aysem_in_pair = aysem_quota_pair[0]
        if ay_sem == aysem_in_pair:
            quota_in_pair = aysem_quota_pair[1]

            return quota_in_pair

    return None # quota not found in list


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
    final_table = append_missing_year_of_study(table_with_non_zero_students)

    # Sort the table based on year
    final_table.sort(key=lambda row: row[INDEX_FIRST_ELEM])

    return final_table


def append_missing_year_of_study(initial_table):
    '''
        Helper function to append missing years of study to the
        given initial table.
        initial_table given in lists of (year, number of students)
        pair.
        e.g. If year 5 is missing from table, appends (5,0) to table
        and returns the table
    '''
    MAX_POSSIBLE_YEAR = 6
    for index in range(0, MAX_POSSIBLE_YEAR):
        year = index + 1
        year_exists_in_table = False

        for year_count_pair in initial_table:
            req_year = year_count_pair[0]
            if req_year == year:
                year_exists_in_table = True
                break

        if not year_exists_in_table:
            initial_table.append((year, 0))

    return initial_table


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
                "GROUP BY sp1.moduleCode, m1.name, sp2.moduleCode, m2.name, sp1.acadYearAndSem " + \
                "ORDER BY COUNT(*) DESC"

    DB_CURSOR.execute(sql_command, (code,))

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


def get_list_students_take_module(code, aysem):
    '''
        Retrieves the list of students who take specified module at specified aysem.

        Returns a table of lists. Each list represents a student and it contains
        (matric number, year of study, focus area 1, focus area 2)
    '''

    sql_command = "SELECT sp.studentid, s.year, tfa.focusarea1, tfa.focusarea2 " + \
                "FROM studentPlans sp, student s, takesFocusArea tfa " + \
                "WHERE sp.moduleCode = %s AND sp.acadYearAndSem = %s " + \
                "AND sp.studentid = s.nusnetid AND " + \
                "sp.studentid = tfa.nusnetid"

    DB_CURSOR.execute(sql_command, (code, aysem))

    current_list_of_students = DB_CURSOR.fetchall()

    return replace_null_with_dash(current_list_of_students)


def replace_null_with_dash(table):
    '''
        Changes all the NULL values found in the table to '-'
        This function supports a 2D table.
    '''
    table = convert_to_list(table)

    for row in table:
        row_length = len(row)
        for col in range(row_length):
            if row[col] is None:
                row[col] = '-'

    return table


def convert_to_list(table):
    '''
        Converts a list of tuples to a list of lists.
    '''
    converted_table = list()

    for row in table:
        conveted_list = list(row)
        converted_table.append(conveted_list)

    return converted_table


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


def add_student_plan(student_id, is_taken, module_code, ay_sem):
    '''
        Add a student plan into the database
    '''
    sql_command = 'INSERT INTO studentPlans VALUES(%s, %s, %s, %s);'
    DB_CURSOR.execute(sql_command, (student_id, is_taken, module_code, ay_sem))
    CONNECTION.commit()


def delete_student_plan(student_id, module_code, ay_sem):
    '''
        Delete a student plan from the database
    '''
    sql_command = "DELETE FROM studentPlans WHERE studentId = %s " +\
                  "AND moduleCode = %s AND acadYearAndSem = %s;"
    DB_CURSOR.execute(sql_command, (student_id, module_code, ay_sem))
    CONNECTION.commit()


def get_number_of_students_taking_module(module_code, ay_sem):
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


def add_prerequisite(module_code, prereq_code, index):
    '''
        Insert a prerequisite into the prerequisite table.
        Returns true if successful, false if duplicate primary key detected
    '''
    sql_command = "INSERT INTO prerequisite VALUES (%s,%s,%s)"
    try:
        DB_CURSOR.execute(sql_command, (module_code, prereq_code, index))
        CONNECTION.commit()
    except psycopg2.IntegrityError:        # duplicate key error
        CONNECTION.rollback()
        return False
    return True


def get_prerequisite(module_code):
    '''
        Get a prerequisite from the prerequisite table.
    '''
    sql_command = "SELECT index, prerequisiteModuleCode FROM prerequisite WHERE moduleCode = %s"
    DB_CURSOR.execute(sql_command, (module_code,))
    return DB_CURSOR.fetchall()


def get_prerequisite_as_string(module_code):
    '''
        Returns a string of pre-requisites of specified module_code
    '''
    prerequisites = get_prerequisite(module_code)
    prereq_list = convert_to_list(prerequisites)

    # sort list of lists based on index (which is the first elem of each row)
    prereq_list.sort(key=lambda row: row[INDEX_FIRST_ELEM])

    prereq_string = convert_list_of_prereqs_to_string(prereq_list)

    return prereq_string


def convert_list_of_prereqs_to_string(prereq_list):
    '''
        Converts given list of lists (prereq_list) into string form of prereqs.
        Pre-condition: Given list must have the rows' first index sorted.
        Example: [['0', 'CS1010'], ['0', 'CS1231'], ['1', 'CS2105']] will yield
        the string (CS1010 or CS1231) and CS2105.
        Same index elements have an "OR" relationship, different index elements
        have an "AND" relationship.
    '''
    number_of_prereq = len(prereq_list)
    if number_of_prereq == LENGTH_EMPTY:
        return ""

    required_string = ""
    temp_list_for_or = list()
    previous_index = None
    for prereq_with_index in prereq_list:
        current_index = prereq_with_index[INDEX_FIRST_ELEM]
        current_prereq = prereq_with_index[INDEX_SECOND_ELEM]

        if previous_index is None:
            previous_index = current_index
            temp_list_for_or.append(current_prereq)
        else:
            if previous_index == current_index:
                temp_list_for_or.append(current_prereq)
            else:
                prereq_of_or_string = convert_list_prereq_to_or_string(temp_list_for_or)
                required_string = process_and_relation_prereq(required_string,
                                                              prereq_of_or_string)
                previous_index = current_index
                temp_list_for_or = [current_prereq]

    if len(required_string) == LENGTH_EMPTY:
        # there is no 'and' relation
        prereq_of_or_string = convert_list_prereq_to_or_string(temp_list_for_or,
                                                               False)
        required_string = prereq_of_or_string
    else:
        # there is 'and' relation to process
        prereq_of_or_string = convert_list_prereq_to_or_string(temp_list_for_or)
        required_string = process_and_relation_prereq(required_string,
                                                      prereq_of_or_string)

    return required_string


def convert_list_prereq_to_or_string(temp_list, to_add_brackets=True):
    '''
        Converts all elements in temp_list to a string separated by "or"
    '''
    number_of_prereq = len(temp_list)
    if number_of_prereq == 1:
        return temp_list[INDEX_FIRST_ELEM]
    else:
        # more than 1 prereq
        required_string = " or ".join(temp_list)

        if to_add_brackets:
            required_string_with_brackets = "(" + required_string + ")"

            return required_string_with_brackets
        else:
            return required_string


def process_and_relation_prereq(existing_string, prereq_of_or_string):
    '''
        Appends the prereq_of_or_string into existing_string by building
        "and" relations between existing prereqs in existing_string
        with those in prereq_of_or_string
    '''
    existing_string_length = len(existing_string)

    if existing_string_length == LENGTH_EMPTY:
        return prereq_of_or_string
    else:
        and_string = " and "
        required_string = existing_string + and_string + prereq_of_or_string

        return required_string


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


def get_preclusion(module_code):
    '''
        Get all preclusions of module_code from the precludes table.
    '''
    sql_command = "SELECT precludedByModuleCode FROM precludes WHERE moduleCode = %s"
    DB_CURSOR.execute(sql_command, (module_code,))
    return DB_CURSOR.fetchall()


def get_preclusion_as_string(module_code):
    '''
        Returns a string of preclusions of specified module_code
    '''
    preclusions = get_preclusion(module_code)
    preclude_list = convert_to_list(preclusions)
    processed_list = [preclude[INDEX_FIRST_ELEM] for preclude in preclude_list]

    preclude_string = ", ".join(processed_list)

    return preclude_string


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

    if is_aysem_in_list(aysem, fixed_sems):
        DB_CURSOR.execute(sql_command, MAP_TABLE_TO_MODULE_MOUNTED)
    elif is_aysem_in_list(aysem, tenta_sems):
        DB_CURSOR.execute(sql_command, MAP_TABLE_TO_MODULE_MOUNT_TENTA)
    else: # No such aysem found
        return list()

    required_list = DB_CURSOR.fetchall()

    return required_list


def is_aysem_in_list(given_aysem, given_list):
    '''
        Returns true if given_aysem is found inside given_list.
        Example:
        given_list is a list of [('AY 16/17 Sem 1',), ('AY 16/17 Sem 2',)] structure.
    '''
    for aysem_tuple in given_list:
        retrieved_aysem = aysem_tuple[0]
        if given_aysem == retrieved_aysem:
            return True

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

    if is_aysem_in_list(given_aysem, fixed_sems):
        DB_CURSOR.execute(sql_command, MAP_TABLE_TO_MODULE_MOUNTED)
    elif is_aysem_in_list(given_aysem, tenta_sems):
        DB_CURSOR.execute(sql_command, MAP_TABLE_TO_MODULE_MOUNT_TENTA)
    else: # No such aysem found
        return list()

    required_list = DB_CURSOR.fetchall()
    processed_list = convert_to_list(required_list)

    return processed_list


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
