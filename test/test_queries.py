from paste.fixture import TestApp
from nose.tools import *
from components import model
import os
import psycopg2

# HOW TO RUN NOSE TESTS
# 1. Make sure you are in cs-modify main directory
# 2. Make sure the path "C:\Python27\Scripts" is added in your environment variables
# 3. Enter in cmd: "nosetests test/"
# 4. Nose will run all the tests inside the test/ folder

class TestCode():
    def __init__(self):
        self.moduleTableColumnCount = 2
    
    def test_query_year_of_study(self):
        name_year_pair = model.get_num_students_by_yr_study(self.testModuleCode)

        assert_equal(self.moduleTableColumnCount, len(moduleInfo))
        assert_equal(self.testModuleCode, moduleInfo[0])
        assert_equal(self.testModuleName, moduleInfo[1])
        assert_in(self.testModuleDesc, moduleInfo[2])
        assert_equal(self.testModuleMC, moduleInfo[3])
        assert_equal(self.testModuleStatus, moduleInfo[4].rstrip()) 