'''
    check_string.py
    checks if a string matches a pattern
'''
import re
from components.handlers.outcome import Outcome

def check_code(code_str):
    #check if code_str matches code pattern
    '''
        Args:
        param (str): string representing code

        Return:
        bool: if the code string matches the correct pattern
    '''
    pattern = re.compile('^[A-Za-z]{2,3}[0-9]{4}[A-Za-z]{0,2}$')
    return bool(pattern.match(code_str))


def check_name(name_str):
    '''
        Args:
        param (str): string representing the name

        Return:
        bool: if the name is a valid name
    '''
    pattern = re.compile('^[a-zA-Z0-9\s-]*$')
    return bool(pattern.match(name_str))

def check_mcs(mc_str):
    '''
        Args
        param (str): string representing the mc

        Return:
        bool: if the mc is from 0 to 12 inclusive
    '''
    pattern = re.compile('^[0-9][0-2]{0,1}$')
    return bool(pattern.match(str(mc_str)))


def outcome_invalid():
    '''
        Return:
        Outcome page: returns the outcome page when an invalid input is detected
    '''
    return Outcome().POST("invalid_input", None, None)

def is_alpha_numeric(my_str):
    '''
        Args
        param (str): str representing the user id

        Return:
        bool: true if id is alpha numeric
    '''
    pattern = re.compile('^[0-9a-zA-Z]{0,20}$')
    return bool(pattern.match(str(my_str)))
