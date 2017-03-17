'''
test_module_specified_class_size_backend.py
Contains test cases for module with specified class size query functions.
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
        This class runs the test cases for module with specified class size query functions.
    '''
    def __init__(self):
        self.test_aysem_1 = "AY 16/17 Sem 1"
        self.test_quota_lower_1 = 0
        self.test_quota_higher_1 = 40
        self.test_aysem_2 = "AY 17/18 Sem 2"
        self.test_quota_lower_2 = 170
        self.test_quota_higher_2 = 240


    def test_query_modules_specified_class_size_aysem_in_fixed(self):
        '''
            Tests querying modules with specified class size, where
            aysem is found in fixed mounting.
        '''
        list_of_modules = \
            model.get_mod_specified_class_size(self.test_aysem_1, self.test_quota_lower_1,
                                               self.test_quota_higher_1)

        required_list = [["CS6101", 0], ["MM1001", 10], ["FMC1206", 15], ["CS2309", 20],
                         ["MM1002", 20], ["CS6203", 30], ["CS6880", 30], ["CS2220", 30],
                         ["CS6231", 40], ["CS3205", 40], ["MM1004", 40]]

        assert_equal(len(list_of_modules), len(required_list))
        assert_equal(sorted(list_of_modules), sorted(required_list))


    def test_query_modules_specified_class_size_aysem_in_tenta(self):
        '''
            Tests querying modules with specified class size, where
            aysem is found in tentative mounting
        '''
        list_of_modules = \
            model.get_mod_specified_class_size(self.test_aysem_2, self.test_quota_lower_2,
                                               self.test_quota_higher_2)

        required_list = [["CS2106", 180], ["CS2103", 180], ["CS2107", 200],
                         ["CS1010S", 200]]

        assert_equal(len(list_of_modules), len(required_list))
        assert_equal(sorted(list_of_modules), sorted(required_list))
