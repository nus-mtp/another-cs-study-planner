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


def get_oversub_mod():
    '''
        Retrieves a list of modules which are oversubscribed.
        Returns module, AY/Sem, quota, number students interested
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
            quota = get_quota_in_aysem(ay_sem, aysem_quota_merged_list)

            if (quota == None):
                quota = 0

            if (num_student_planning > quota):
                oversub_info = (mod_code, ay_sem, quota, num_student_planning)
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
        if (ay_sem == aysem_in_pair):
            quota_in_pair = aysem_quota_pair[1]

            return quota_in_pair

    return None # quota not found in list
