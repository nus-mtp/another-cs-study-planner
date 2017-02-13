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
        self.moduleTableColumnCount = 5
        self.testModuleCode = "CS2103T"
        self.testModuleName = "Software Engineering"
        self.testModuleDesc = "This module introduces the necessary conceptual and analytical tools for systematic and rigorous development of software systems."
        self.testModuleMC = 4
        self.testModuleStatus = "Active"

        self.mountingTableColumnCount = 3
        self.testModuleMountedCount = 2
        self.testModuleFixedMountedAySem1 = "AY 16/17 Sem 1"
        self.testModuleFixedMountedAySem2 = "AY 16/17 Sem 2"
        self.testModuleTentativeMountedAySem1 = "AY 17/18 Sem 1"
        self.testModuleTentativeMountedAySem2 = "AY 17/18 Sem 2"
        self.testModuleQuota1 = 190
        self.testModuleQuota2 = 160
    
    def test_getModule(self):
        moduleInfo = model.getModule(self.testModuleCode)
        assert_equal(self.moduleTableColumnCount, len(moduleInfo))
        assert_equal(self.testModuleCode, moduleInfo[0])
        assert_equal(self.testModuleName, moduleInfo[1])
        assert_in(self.testModuleDesc, moduleInfo[2])
        assert_equal(self.testModuleMC, moduleInfo[3])
        assert_equal(self.testModuleStatus, moduleInfo[4].rstrip())

    def test_getFixedMountingAndQuota(self):
        mountings = model.getFixedMountingAndQuota(self.testModuleCode)
        assert_equal(self.testModuleMountedCount, len(mountings))
        
        mountingAndQuota1 = mountings[0]
        assert_equal(self.testModuleFixedMountedAySem1, mountingAndQuota1[0])
        assert_equal(self.testModuleQuota1, mountingAndQuota1[1])
        
        mountingAndQuota2 = mountings[1]
        assert_equal(self.testModuleFixedMountedAySem2, mountingAndQuota2[0])
        assert_equal(self.testModuleQuota2, mountingAndQuota2[1])

    def test_getTentativeMountingAndQuota(self):
        mountings = model.getTentativeMountingAndQuota(self.testModuleCode)
        assert_equal(self.testModuleMountedCount, len(mountings))
        
        mountingAndQuota1 = mountings[0]
        assert_equal(self.testModuleTentativeMountedAySem1, mountingAndQuota1[0])
        assert_equal(self.testModuleQuota1, mountingAndQuota1[1])
        
        mountingAndQuota2 = mountings[1]
        assert_equal(self.testModuleTentativeMountedAySem2, mountingAndQuota2[0])
        assert_equal(self.testModuleQuota2, mountingAndQuota2[1])

    def test_addAndDeleteModule(self):
        model.addModule("AA1111", "Dummy Module", "Dummy Description", 1)
        moduleInfo = model.getModule("AA1111")
        assert_true(moduleInfo is not None)
        assert_equal("New", moduleInfo[4].rstrip())

        model.deleteModule("AA1111")
        moduleInfo = model.getModule("AA1111")
        assert_true(moduleInfo is None)

    def test_addModuleWithDuplicateCode(self):
        hasIntegrityError = False
        errorMessage = ""
        model.addModule("AA1111", "Dummy Module", "Dummy Description", 1)

        # Not duplicate code --> No error
        try:
            model.addModule("AA2222", "Dummy Module", "Dummy Description", 1)
        except psycopg2.IntegrityError as e:
            hasIntegrityError = True
        assert_false(hasIntegrityError)

        # Duplicate code --> Integrity error
        try:
            model.addModule("AA1111", "Dummy Module", "Dummy Description", 1)
        except psycopg2.IntegrityError as e:
            hasIntegrityError = True
            errorMessage = str(e.args)
        assert_true(hasIntegrityError)
        assert_in("duplicate key value", errorMessage)
        
        model.connection.rollback()
        model.deleteModule("AA1111")
        model.deleteModule("AA2222")
        
        
