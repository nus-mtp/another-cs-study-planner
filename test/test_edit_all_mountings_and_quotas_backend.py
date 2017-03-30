'''
    test_edit_all_mountings_and_quotas_backend.py test the backend functions of
    Edit All Mountings and Quotas
'''
from nose.tools import assert_equal, assert_false
from components import model
from components.handlers.edit_all_mountings_and_quotas import EditAll


class TestCode(object):
    '''
        This class runs the test cases to test Edit All Mountings and Quotas backend functions
    '''
    def __init__(self):
        self.edit_all_handler = EditAll()
        self.current_ay = model.get_current_ay()
        self.next_ay = model.get_next_ay(self.current_ay)


    def setUp(self):
        '''
            Add dummy modules and mountings into database
        '''
        # Dummy modules
        self.DUMMY_MODULE_CODE_1 = 'BB1001'
        self.DUMMY_MODULE_CODE_2 = 'BB1002'
        self.DUMMY_MODULE_CODE_3 = 'BB1003'
        model.add_module(self.DUMMY_MODULE_CODE_1, 'Dummy Module 1',
                         "Dummy Module", 1, 'Active')
        model.add_module(self.DUMMY_MODULE_CODE_2, 'Dummy Module 2',
                         "Dummy Module", 2, 'Active')
        model.add_module(self.DUMMY_MODULE_CODE_3, 'Dummy Module 3',
                         "Dummy Module", 3, 'Active')

        # Dummy mountings
        self.DUMMY_QUOTA_0 = None
        self.DUMMY_QUOTA_1 = 10
        self.DUMMY_QUOTA_2 = 20
        self.DUMMY_QUOTA_3 = 30
        model.add_fixed_mounting(self.DUMMY_MODULE_CODE_1,
                                 self.current_ay+' Sem 1', self.DUMMY_QUOTA_1)
        model.add_tenta_mounting(self.DUMMY_MODULE_CODE_1,
                                 self.next_ay+' Sem 1', self.DUMMY_QUOTA_1)
        model.add_fixed_mounting(self.DUMMY_MODULE_CODE_2,
                                 self.current_ay+' Sem 2', self.DUMMY_QUOTA_2)
        model.add_tenta_mounting(self.DUMMY_MODULE_CODE_2,
                                 self.next_ay+' Sem 2', self.DUMMY_QUOTA_2)
        model.add_fixed_mounting(self.DUMMY_MODULE_CODE_3,
                                 self.current_ay+' Sem 1', self.DUMMY_QUOTA_3)
        model.add_tenta_mounting(self.DUMMY_MODULE_CODE_3,
                                 self.next_ay+' Sem 1', self.DUMMY_QUOTA_3)
        model.add_fixed_mounting(self.DUMMY_MODULE_CODE_3,
                                 self.current_ay+' Sem 2', self.DUMMY_QUOTA_0)
        model.add_tenta_mounting(self.DUMMY_MODULE_CODE_3,
                                 self.next_ay+' Sem 2', self.DUMMY_QUOTA_0)


    def tearDown(self):
        '''
            Clean up the database after all test cases are ran
        '''
        model.delete_all_fixed_mountings(self.DUMMY_MODULE_CODE_1)
        model.delete_all_tenta_mountings(self.DUMMY_MODULE_CODE_1)
        model.delete_all_fixed_mountings(self.DUMMY_MODULE_CODE_2)
        model.delete_all_tenta_mountings(self.DUMMY_MODULE_CODE_2)
        model.delete_all_fixed_mountings(self.DUMMY_MODULE_CODE_3)
        model.delete_all_tenta_mountings(self.DUMMY_MODULE_CODE_3)

        model.delete_module(self.DUMMY_MODULE_CODE_1)
        model.delete_module(self.DUMMY_MODULE_CODE_2)
        model.delete_module(self.DUMMY_MODULE_CODE_3)


    def test_edit_single_module_quota(self):
        '''
            Test that Edit All function can edit a single module's quota
        '''
        test_module_code = self.DUMMY_MODULE_CODE_1
        test_mounting = True
        test_quota = 100

        # Modifiy Sem 1 quota
        test_data = {}
        test_data[test_module_code+'_isEdited'] = "True"
        test_data[test_module_code+'_Sem1Mounting'] = test_mounting
        test_data[test_module_code+'_Sem1Quota'] = test_quota  #modified

        self.edit_all_handler.POST(test_data)

        mounting = model.get_mounting_of_target_tenta_ay_sem(test_module_code,
                                                             self.next_ay+" Sem 1")
        quota = model.get_quota_of_target_tenta_ay_sem(test_module_code,
                                                       self.next_ay+" Sem 1")
        assert_equal(mounting, test_mounting)
        assert_equal(quota, test_quota)

        model.update_quota(test_module_code, self.next_ay+" Sem 1", self.DUMMY_QUOTA_1)

        # Modify Sem 2 quota
        test_module_code = self.DUMMY_MODULE_CODE_2
        test_mounting = True
        test_quota = 200

        test_data = {}
        test_data[test_module_code+'_isEdited'] = "True"
        test_data[test_module_code+'_Sem2Mounting'] = test_mounting
        test_data[test_module_code+'_Sem2Quota'] = test_quota  #modified

        self.edit_all_handler.POST(test_data)

        mounting = model.get_mounting_of_target_tenta_ay_sem(test_module_code,
                                                             self.next_ay+" Sem 2")
        quota = model.get_quota_of_target_tenta_ay_sem(test_module_code,
                                                       self.next_ay+" Sem 2")
        assert_equal(mounting, test_mounting)
        assert_equal(quota, test_quota)

        model.update_quota(test_module_code, self.next_ay+" Sem 2", self.DUMMY_QUOTA_2)


    def test_edit_single_module_multiple_quotas(self):
        '''
            Test that Edit All function can edit a single module's multiple quotas
        '''
        test_module_code = self.DUMMY_MODULE_CODE_3
        test_mounting_1 = True
        test_mounting_2 = True
        test_quota_1 = None
        test_quota_2 = 300

        # Modify Sem 1 and 2 quotas
        test_data = {}
        test_data[test_module_code+'_isEdited'] = "True"
        test_data[test_module_code+'_Sem1Mounting'] = test_mounting_1
        #test_data[test_module_code+'_Sem1Quota'] = test_quota_1   #modified to empty
        test_data[test_module_code+'_Sem2Mounting'] = test_mounting_2
        test_data[test_module_code+'_Sem2Quota'] = test_quota_2    #modified

        self.edit_all_handler.POST(test_data)

        mounting = model.get_mounting_of_target_tenta_ay_sem(test_module_code,
                                                             self.next_ay+" Sem 1")
        quota = model.get_quota_of_target_tenta_ay_sem(test_module_code,
                                                       self.next_ay+" Sem 1")
        assert_equal(mounting, test_mounting_1)
        assert_equal(quota, test_quota_1)

        mounting = model.get_mounting_of_target_tenta_ay_sem(test_module_code,
                                                             self.next_ay+" Sem 2")
        quota = model.get_quota_of_target_tenta_ay_sem(test_module_code,
                                                       self.next_ay+" Sem 2")
        assert_equal(mounting, test_mounting_2)
        assert_equal(quota, test_quota_2)

        model.update_quota(test_module_code, self.next_ay+" Sem 1", self.DUMMY_QUOTA_3)
        model.update_quota(test_module_code, self.next_ay+" Sem 2", self.DUMMY_QUOTA_0)


    def test_edit_multiple_modules_quotas(self):
        '''
            Test that Edit All function can edit multiple modules' quota(s)
        '''
        test_data = {}

        # Modify Dummy Module 1's quota
        test_mod_1_code = self.DUMMY_MODULE_CODE_1
        test_mod_1_mounting = True
        test_mod_1_quota = 100
        test_data[test_mod_1_code+'_isEdited'] = "True"
        test_data[test_mod_1_code+'_Sem1Mounting'] = test_mod_1_mounting
        test_data[test_mod_1_code+'_Sem1Quota'] = test_mod_1_quota

        # Modify Dummy Module 2's quota
        test_mod_2_code = self.DUMMY_MODULE_CODE_2
        test_mod_2_mounting = True
        test_mod_2_quota = 200
        test_data[test_mod_2_code+'_isEdited'] = "True"
        test_data[test_mod_2_code+'_Sem2Mounting'] = test_mod_2_mounting
        test_data[test_mod_2_code+'_Sem2Quota'] = test_mod_2_quota

        self.edit_all_handler.POST(test_data)

        mounting = model.get_mounting_of_target_tenta_ay_sem(test_mod_1_code,
                                                             self.next_ay+" Sem 1")
        quota = model.get_quota_of_target_tenta_ay_sem(test_mod_1_code,
                                                       self.next_ay+" Sem 1")
        assert_equal(mounting, test_mod_1_mounting)
        assert_equal(quota, test_mod_1_quota)

        mounting = model.get_mounting_of_target_tenta_ay_sem(test_mod_2_code,
                                                             self.next_ay+" Sem 2")
        quota = model.get_quota_of_target_tenta_ay_sem(test_mod_2_code,
                                                       self.next_ay+" Sem 2")
        assert_equal(mounting, test_mod_2_mounting)
        assert_equal(quota, test_mod_2_quota)

        model.update_quota(test_mod_1_code, self.next_ay+" Sem 1", self.DUMMY_QUOTA_1)
        model.update_quota(test_mod_2_code, self.next_ay+" Sem 2", self.DUMMY_QUOTA_2)


    def test_edit_single_module_mounting(self):
        '''
            Test that Edit All function can edit a single module's mounting
        '''
        test_module_code = self.DUMMY_MODULE_CODE_1
        test_mounting = False   #unmounted
        test_quota = False   #quota will be false because unmounted

        # Unmount from Sem 1
        test_data = {}
        test_data[test_module_code+'_isEdited'] = "True"
        #test_data[test_module_code+'_Sem1Mounting'] = test_mounting   #modified to false
        test_data[test_module_code+'_Sem1Quota'] = test_quota

        self.edit_all_handler.POST(test_data)

        mounting = model.get_mounting_of_target_tenta_ay_sem(test_module_code,
                                                             self.next_ay+" Sem 1")
        quota = model.get_quota_of_target_tenta_ay_sem(test_module_code,
                                                       self.next_ay+" Sem 1")
        assert_equal(mounting, test_mounting)
        assert_equal(quota, test_quota)

        model.add_tenta_mounting(test_module_code, self.next_ay+" Sem 1", self.DUMMY_QUOTA_1)

        # Mount in Sem 2
        test_module_code = self.DUMMY_MODULE_CODE_2
        test_mounting = True
        test_quota = 200

        test_data = {}
        test_data[test_module_code+'_isEdited'] = "True"
        test_data[test_module_code+'_Sem2Mounting'] = True   #modified to true
        test_data[test_module_code+'_Sem2Quota'] = test_quota  #modified

        self.edit_all_handler.POST(test_data)

        mounting = model.get_mounting_of_target_tenta_ay_sem(test_module_code,
                                                             self.next_ay+" Sem 2")
        quota = model.get_quota_of_target_tenta_ay_sem(test_module_code,
                                                       self.next_ay+" Sem 2")
        assert_equal(mounting, test_mounting)
        assert_equal(quota, test_quota)

        model.delete_tenta_mounting(test_module_code, self.next_ay+" Sem 2")


    def test_edit_single_module_multiple_mountings(self):
        '''
            Test that Edit All function can edit a single module's multiple mounting
        '''
        # Unmount from Sem 1, and mount in Sem 2
        test_module_code = self.DUMMY_MODULE_CODE_1
        test_mounting_1 = False   #unmounted
        test_quota_1 = False   #quota will be false because unmounted
        test_mounting_2 = True   #mounted
        test_quota_2 = 200   #quota added

        test_data = {}
        test_data[test_module_code+'_isEdited'] = "True"
        #test_data[test_module_code+'_Sem1Mounting'] = test_mounting   #modified to false
        test_data[test_module_code+'_Sem1Quota'] = test_quota_1
        test_data[test_module_code+'_Sem2Mounting'] = test_mounting_2   #modified to true
        test_data[test_module_code+'_Sem2Quota'] = test_quota_2

        self.edit_all_handler.POST(test_data)

        mounting = model.get_mounting_of_target_tenta_ay_sem(test_module_code,
                                                             self.next_ay+" Sem 1")
        quota = model.get_quota_of_target_tenta_ay_sem(test_module_code,
                                                       self.next_ay+" Sem 1")
        assert_equal(mounting, test_mounting_1)
        assert_equal(quota, test_quota_1)

        mounting = model.get_mounting_of_target_tenta_ay_sem(test_module_code,
                                                             self.next_ay+" Sem 2")
        quota = model.get_quota_of_target_tenta_ay_sem(test_module_code,
                                                       self.next_ay+" Sem 2")
        assert_equal(mounting, test_mounting_2)
        assert_equal(quota, test_quota_2)

        model.add_tenta_mounting(test_module_code, self.next_ay+" Sem 1",
                                 self.DUMMY_QUOTA_1)
        model.delete_tenta_mounting(test_module_code, self.next_ay+" Sem 2")


    def test_edit_multiple_modules_mountings(self):
        '''
            Test that Edit All function can edit multiple modules' mounting(s)
        '''
        test_data = {}

        # Dummy Module 1: Mount in Sem 2
        test_mod_1_code = self.DUMMY_MODULE_CODE_1
        test_mod_1_mounting = True   #mounted
        test_mod_1_quota = 200   #quota added

        test_data[test_mod_1_code+'_isEdited'] = "True"
        test_data[test_mod_1_code+'_Sem2Mounting'] = test_mod_1_mounting   #modified to true
        test_data[test_mod_1_code+'_Sem2Quota'] = test_mod_1_quota

        # Dummy Module 3: Unmount from both sems
        test_mod_2_code = self.DUMMY_MODULE_CODE_3
        test_mod_2_mounting_1 = False   #unmounted
        test_mod_2_quota_1 = False   #quota will be false because unmounted
        test_mod_2_mounting_2 = False   #unmounted
        test_mod_2_quota_2 = False   #quota will be false because unmounted

        test_data[test_mod_2_code+'_isEdited'] = "True"
         #test_data[test_module_code+'_Sem1Mounting'] = test_mounting_1   #modified to false
        test_data[test_mod_2_code+'_Sem1Quota'] = test_mod_2_quota_1
        #test_data[test_module_code+'_Sem2Mounting'] = test_mounting_2   #modified to false
        test_data[test_mod_2_code+'_Sem2Quota'] = test_mod_2_quota_2

        self.edit_all_handler.POST(test_data)

        mounting = model.get_mounting_of_target_tenta_ay_sem(test_mod_1_code,
                                                             self.next_ay+" Sem 2")
        quota = model.get_quota_of_target_tenta_ay_sem(test_mod_1_code,
                                                       self.next_ay+" Sem 2")
        assert_equal(mounting, test_mod_1_mounting)
        assert_equal(quota, test_mod_1_quota)

        mounting = model.get_mounting_of_target_tenta_ay_sem(test_mod_2_code,
                                                             self.next_ay+" Sem 1")
        quota = model.get_quota_of_target_tenta_ay_sem(test_mod_2_code,
                                                       self.next_ay+" Sem 1")
        assert_equal(mounting, test_mod_2_mounting_1)
        assert_equal(quota, test_mod_2_quota_1)

        mounting = model.get_mounting_of_target_tenta_ay_sem(test_mod_2_code,
                                                             self.next_ay+" Sem 2")
        quota = model.get_quota_of_target_tenta_ay_sem(test_mod_2_code,
                                                       self.next_ay+" Sem 2")
        assert_equal(mounting, test_mod_2_mounting_2)
        assert_equal(quota, test_mod_2_quota_2)

        model.delete_tenta_mounting(test_mod_1_code, self.next_ay+" Sem 2")
        model.add_tenta_mounting(test_mod_2_code, self.next_ay+" Sem 1", self.DUMMY_QUOTA_3)
        model.add_tenta_mounting(test_mod_2_code, self.next_ay+" Sem 2", self.DUMMY_QUOTA_0)


    def test_invalid_quota(self):
        '''
            Test that backend validation can catch invalid quota
        '''
        # Quota is string (invalid)
        test_module_code = self.DUMMY_MODULE_CODE_1
        test_mounting = True
        test_quota = 'aaa'

        test_data = {}
        test_data[test_module_code+'_isEdited'] = "True"
        test_data[test_module_code+'_Sem1Mounting'] = test_mounting
        test_data[test_module_code+'_Sem1Quota'] = test_quota

        outcome = self.edit_all_handler.POST(test_data)
        assert_false(outcome)

        # Quota is negative number (invalid)
        test_quota = -1

        test_data = {}
        test_data[test_module_code+'_isEdited'] = "True"
        test_data[test_module_code+'_Sem1Mounting'] = test_mounting
        test_data[test_module_code+'_Sem1Quota'] = test_quota

        outcome = self.edit_all_handler.POST(test_data)
        assert_false(outcome)
