'''
test_get_academic_year_and_sem.py
Contains test cases for getting the correct AY-Semester, given the date.
'''
from nose.tools import assert_equal
from components import model

# HOW TO RUN NOSE TESTS
# 1. Make sure you are in cs-modify main directory
# 2. Make sure the path "C:\Python27\Scripts" is added in your environment variables
# 3. Enter in cmd: "nosetests test/"
# 4. Nose will run all the tests inside the test/ folder

class TestCode(object):
    '''
        This class runs the test cases for getting the correct AY-Semester, given the date.
    '''
    def __init__(self):
        self.test_january = 1
        self.test_year = 2015
        self.required_aysem_jan_15 = "AY 14/15 Sem 2"
        self.test_july = 7
        self.required_aysem_jul_15 = "AY 14/15 Sem 2"
        self.test_august = 8
        self.required_aysem_aug_15 = "AY 15/16 Sem 1"
        self.test_december = 12
        self.required_aysem_dec_15 = "AY 15/16 Sem 1"


    def test_get_aysem_given_date_january(self):
        '''
            Tests getting the correct AY-Semester, given the January date.
        '''
        ay_semester = model.get_ay_sem(self.test_year, self.test_january)
        required_ay_semester = self.required_aysem_jan_15

        assert_equal(ay_semester, required_ay_semester)


    def test_get_aysem_given_date_july(self):
        '''
            Tests getting the correct AY-Semester, given the July date.
        '''
        ay_semester = model.get_ay_sem(self.test_year, self.test_july)
        required_ay_semester = self.required_aysem_jul_15

        assert_equal(ay_semester, required_ay_semester)


    def test_get_aysem_given_date_august(self):
        '''
            Tests getting the correct AY-Semester, given the August date.
        '''
        ay_semester = model.get_ay_sem(self.test_year, self.test_august)
        required_ay_semester = self.required_aysem_aug_15

        assert_equal(ay_semester, required_ay_semester)


    def test_get_aysem_given_date_december(self):
        '''
            Tests getting the correct AY-Semester, given the December date.
        '''
        ay_semester = model.get_ay_sem(self.test_year, self.test_december)
        required_ay_semester = self.required_aysem_dec_15

        assert_equal(ay_semester, required_ay_semester)
