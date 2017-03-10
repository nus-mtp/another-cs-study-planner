'''
    test_module_taken_prior_backend.py
    Contains test cases related to the backend functions of
    modules taken prior to other modules
'''
from nose.tools import assert_equal, assert_true, assert_false
from components import model


class TestCode(object):
    '''
        This class runs the test cases related to modules taken prior to other modules
    '''
    def __init__(self):
        self.current_ay = model.get_current_ay()
        self.next_ay = self.get_next_ay(self.current_ay)


    def get_next_ay(self, ay):
        '''
            Return the AY that comes after the given AY
        '''
        ay = ay.split(' ')[1].split('/')
        return 'AY ' + str(int(ay[0])+1) + '/' + str(int(ay[1])+1)


    def setUp(self):
        '''
            Add dummy modules, mountings and student planners into database
        '''
        # Dummy modules
        model.add_module('PT1001', 'Dummy Module 1',
                         "Dummy Module 1", 1, 'Active')
        model.add_module('PT1002', 'Dummy Module 2',
                         "Dummy Module 2", 2, 'Active')
        model.add_module('PT1003', 'Dummy Module 3',
                         "Dummy Module 3", 3, 'Active')
        model.add_module('PT1004', 'Dummy Module 4',
                         "Dummy Module 4", 4, 'Active')

        model.add_fixed_mounting('PT1001', self.current_ay+' Sem 1', 10)
        model.add_fixed_mounting('PT1002', self.current_ay+' Sem 2', 20)

        model.add_tenta_mounting('PT1001', self.next_ay+' Sem 1', 10)
        model.add_tenta_mounting('PT1002', self.next_ay+' Sem 2', 20)
        model.add_tenta_mounting('PT1003', self.next_ay+' Sem 1', 30)
        model.add_tenta_mounting('PT1003', self.next_ay+' Sem 2', 35)
        model.add_tenta_mounting('PT1004', self.next_ay+' Sem 2', 40)

        model.add_student_plan('D1000000A', True, 'PT1001', self.current_ay+' Sem 1')
        model.add_student_plan('D1000000A', True, 'PT1002', self.current_ay+' Sem 2')
        model.add_student_plan('D2000000A', True, 'PT1001', self.current_ay+' Sem 1')
        model.add_student_plan('D2000000A', False, 'PT1002', self.current_ay+' Sem 2')
        model.add_student_plan('D1000000A', False, 'PT1003', self.next_ay+' Sem 1')
        model.add_student_plan('D3000000A', False, 'PT1001', self.current_ay+' Sem 1')
        model.add_student_plan('D3000000A', False, 'PT1004', self.next_ay+' Sem 2')


    def tearDown(self):
        '''
            Clean up the database after all test cases are ran
        '''
        model.delete_student_plan('D1000000A', 'PT1001', self.current_ay+' Sem 1')
        model.delete_student_plan('D1000000A', 'PT1002', self.current_ay+' Sem 2')
        model.delete_student_plan('D2000000A', 'PT1001', self.current_ay+' Sem 1')
        model.delete_student_plan('D2000000A', 'PT1002', self.current_ay+' Sem 2')
        model.delete_student_plan('D1000000A', 'PT1003', self.next_ay+' Sem 1')
        model.delete_student_plan('D3000000A', 'PT1001', self.current_ay+' Sem 1')
        model.delete_student_plan('D3000000A', 'PT1004', self.next_ay+' Sem 2')

        model.delete_tenta_mounting('PT1001', self.next_ay+' Sem 1')
        model.delete_tenta_mounting('PT1002', self.next_ay+' Sem 2')
        model.delete_tenta_mounting('PT1003', self.next_ay+' Sem 1')
        model.delete_tenta_mounting('PT1003', self.next_ay+' Sem 2')
        model.delete_tenta_mounting('PT1004', self.next_ay+' Sem 2')

        model.delete_fixed_mounting('PT1001', self.current_ay+' Sem 1')
        model.delete_fixed_mounting('PT1002', self.current_ay+' Sem 2')

        model.delete_module('PT1001')
        model.delete_module('PT1002')
        model.delete_module('PT1003')
        model.delete_module('PT1004')


    def test_taken_prior_to(self):
        '''
            Test that when a module is taken prior to another module by a student,
            it will be counted in the table
        '''
        # Two students took PT1001 prior to PT1002
        test_module_A = "PT1001"
        test_module_B = "PT1002"
        test_module_A_taken_in = self.current_ay+' Sem 1'
        test_module_B_taken_in = self.current_ay+' Sem 2'

        module_pairs = model.get_modA_taken_prior_to_modB()
        is_in_table = False
        student_count = -1
        for module_pair in module_pairs:
            module_A = module_pair[0]
            module_B = module_pair[1]
            module_A_taken_in = module_pair[2]
            module_B_taken_in = module_pair[3]
            if module_A == test_module_A and module_B == test_module_B and (
            module_A_taken_in == test_module_A_taken_in) and (
            module_B_taken_in == test_module_B_taken_in):
                is_in_table = True
                student_count = module_pair[4]
                break

        assert_true(is_in_table)
        assert_equal(student_count, 2)

        # One student took PT1001 prior to PT1003
        test_module_A = "PT1001"
        test_module_B = "PT1003"
        test_module_A_taken_in = self.current_ay+' Sem 1'
        test_module_B_taken_in = self.next_ay+' Sem 1'

        module_pairs = model.get_modA_taken_prior_to_modB()
        is_in_table = False
        student_count = -1
        for module_pair in module_pairs:
            module_A = module_pair[0]
            module_B = module_pair[1]
            module_A_taken_in = module_pair[2]
            module_B_taken_in = module_pair[3]
            if module_A == test_module_A and module_B == test_module_B and (
            module_A_taken_in == test_module_A_taken_in) and (
            module_B_taken_in == test_module_B_taken_in):
                is_in_table = True
                student_count = module_pair[4]
                break

        assert_true(is_in_table)
        assert_equal(student_count, 1)


    def test_not_taken_prior_to(self):
        '''
            Test that when a module is NOT taken prior to another module by any student,
            it will NOT be counted in the table
        '''
        # No student took PT1002 prior to PT1001
        test_module_A = "PT1002"
        test_module_B = "PT1001"

        module_pairs = model.get_modA_taken_prior_to_modB()
        is_in_table = False
        student_count = -1
        for module_pair in module_pairs:
            module_A = module_pair[0]
            module_B = module_pair[1]
            module_A_taken_in = module_pair[2]
            module_B_taken_in = module_pair[3]
            if module_A == test_module_A and module_B == test_module_B:
                is_in_table = True
                break

        assert_false(is_in_table)

        # No student took PT1003 prior to PT1001
        test_module_A = "PT1003"
        test_module_B = "PT1001"

        module_pairs = model.get_modA_taken_prior_to_modB()
        is_in_table = False
        student_count = -1
        for module_pair in module_pairs:
            module_A = module_pair[0]
            module_B = module_pair[1]
            module_A_taken_in = module_pair[2]
            module_B_taken_in = module_pair[3]
            if module_A == test_module_A and module_B == test_module_B:
                is_in_table = True
                break

        assert_false(is_in_table)


    def test_plan_to_take_prior_to(self):
        '''
            Test that when a module is PLANNED to be taken prior to another module,
            but has yet to be taken, it will NOT be counted in the table 
        '''
        # No student took PT1001 prior to PT1004
        # One student planned to do so, but has yet to take PT1001
        test_module_A = "PT1001"
        test_module_B = "PT1004"

        module_pairs = model.get_modA_taken_prior_to_modB()
        is_in_table = False
        student_count = -1
        for module_pair in module_pairs:
            module_A = module_pair[0]
            module_B = module_pair[1]
            module_A_taken_in = module_pair[2]
            module_B_taken_in = module_pair[3]
            if module_A == test_module_A and module_B == test_module_B:
                is_in_table = True
                break

        assert_false(is_in_table)