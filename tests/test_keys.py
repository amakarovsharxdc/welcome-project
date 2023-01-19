import unittest
from src.main import DataConstructor, NonValidRootKey

class TestNestedDictCreation(unittest.TestCase):

    def setUp(self):
        self.constructor = DataConstructor()


    def test_key_success(self):
        test_data = {'user':{}}
        self.constructor.output = test_data
        self.constructor.set_output_root_key('user')

    def test_key_failure(self):
        test_data = {'user':{}}
        self.constructor.output = test_data
        self.assertRaises(NonValidRootKey, self.constructor.set_output_root_key, 'role')