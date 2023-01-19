import unittest
from src.main import DataConstructor


class TestNodeCreation(unittest.TestCase):

    def setUp(self):
        self.constructor = DataConstructor()


    def test_set_node_data_success(self):
        data = ('user', '/api/v1/username/role')
        output = self.constructor.set_node_data(data)
        self.assertTrue(isinstance(output, dict))
        
    def test_set_node_data_failure(self):
        data = ('user', '/api/v1')
        self.assertRaises(ValueError, self.constructor.set_node_data, data)
