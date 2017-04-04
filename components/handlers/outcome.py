'''
    This module contains the handler for displaying the outcome of a form submission
    (E.g. adding/editing/restoring a module)
'''

from app import RENDER


class Outcome(object):
    '''
        This class handles the display of a form submission's outcome
    '''
    def POST(self, *received_data):
        '''
            POST method will check the type of action executed by the user,
            and display the corresponding message based on the execution's outcome.
        '''
        if received_data is not None:
            data = received_data
            action = data[0]
            outcome = data[1]
            module_code = data[2]

            outcome_message = None
            redirect_page = None

            if action == "add_module":
                if outcome is True:
                    outcome_message = "Module " + module_code + " has been added successfully!"
                    redirect_page = "/viewModule?code="+module_code
                else:
                    if module_code is None:
                        outcome_message = "Error: failed to add module!"
                    else:
                        outcome_message = "Error: " + module_code + " is an existing module!"
                    redirect_page = "/modules"
            elif action == "edit_module":
                if outcome is True:
                    outcome_message = "Module " + module_code + " has been edited successfully!"
                    redirect_page = "/viewModule?code="+module_code
                else:
                    outcome_message = "Error: Failed to edit module."
                    if module_code is None:
                        redirect_page = "/modules"
                    else:
                        redirect_page = "/viewModule?code="+module_code
            elif action == "invalid_input":
                outcome_message = "Invalid input for module name/code/MCs/description"
                redirect_page = "/"

            elif action == "edit_mounting":
                ay_sem = data[3]
                if outcome is True:
                    outcome_message = "Module " + module_code + " has been edited successfully!"
                    redirect_page = "individualModuleInfo?code="+module_code+"&aysem="+\
                                    ay_sem.replace(' ', '+').replace('/', '%2F')
                else:
                    outcome_message = "Error: Failed to edit module."
                    if module_code is None or ay_sem is None:
                        redirect_page = "/modules"
                    else:
                        redirect_page = "individualModuleInfo?code="+module_code+"&aysem="+\
                                        ay_sem.replace(' ', '+').replace('/', '%2F')

            elif action == "edit_all_mountings_and_quotas":
                if outcome is True:
                    outcome_message = "Modules have been edited successfully!"
                else:
                    outcome_message = "Error: Failed to edit modules."
                redirect_page = "/editAll"

            elif action == "restore_module":
                if outcome is True:
                    outcome_message = "Module " + module_code + " has been restored successfully!"
                    redirect_page = "/viewModule?code="+module_code
                else:
                    outcome_message = "Error: Failed to restore module."
                    redirect_page = "/modifiedModules"

            elif action == "delete_module":
                if outcome is True:
                    outcome_message = "Module " + module_code + " has been deleted successfully!"
                    redirect_page = "/deleteModule"
                else:
                    outcome_message = "Error: Failed to delete module. "
                    redirect_page = "/deleteModule"
                    if module_code is not None:
                        if outcome == "has_mounting":
                            outcome_message += "Module " + module_code + " has " +\
                                               "mountings that refer to it. " +\
                                               "Please remove all mountings before deleting " +\
                                               "the module."
                            redirect_page = "/viewModule?code=" + module_code
                        elif outcome == "is_starred":
                            outcome_message += "Module " + module_code + " is a starred module. " +\
                                               "Please unstar the module before deleting " +\
                                               "the module."
                            redirect_page = "/viewModule?code=" + module_code

            elif action == "create_user":
                if outcome is True:
                    outcome_message = "Your account has been created successfully. " +\
                                      "Please proceed to login."
                    redirect_page = "/login"
                else:
                    outcome_message = "The username has been taken. " +\
                                      "Please register with a different username."
                    redirect_page = "/register"

            elif action == "login_user":
                outcome_message = "Login credentials are empty or incorrect. " +\
                                  "Please try again."
                redirect_page = "/login"

            elif action == "module_taken_prior":
                outcome_message = "Error: Module code " + module_code + " does not exist! "
                redirect_page = "/moduleTakenPriorToOthers"

            elif action == "non-overlapping-mods":
                outcome_message = "The AY-Semester you specified does not exist!"
                redirect_page = "/nonOverlappingModules"

            elif action == "mods-specific-size-aysem":
                outcome_message = "The AY-Semester you specified does not exist!"
                redirect_page = "/moduleSpecificSize"

            elif action == "mods-specific-size-range":
                outcome_message = "You have specified an invalid range!"
                redirect_page = "/moduleSpecificSize"

            elif action == "mods-before-internship":
                outcome_message = "The AY-Semester you specified does not exist!"
                redirect_page = "/moduleTakenPriorToInternship"

            elif action == "migrate-database":
                if outcome is True:
                    outcome_message = "The database has been successfully migrated to the new AY."
                else:
                    outcome_message = "The database migration could not be performed. " +\
                                      "Please contact the system administrator."
                redirect_page = "/"

            elif action == "back-to-listing":
                outcome_message = "The module you want to view has been deleted by another user!"
                redirect_page = "/"
            else:
                outcome_message = "unknown error has occured with action " + action

            return RENDER.outcome(outcome_message, redirect_page)
