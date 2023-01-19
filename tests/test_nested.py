import unittest
from src.main import DataConstructor




class TestNestedDictCreation(unittest.TestCase):

    def setUp(self):
        self.constructor = DataConstructor()

    def test_set_nested_success(self):
        data = ['user', 'firstname', 'lastname']
        nested = self.constructor.set_nested_child(data)
        self.assertTrue(isinstance(nested, dict))

    def test_set_nested_failure(self):
        data = ['user']
        nested = self.constructor.set_nested_child(data)
        self.assertTrue(isinstance(nested, str))
        
    def test_get_nested_child(self):
        data = {'user':{'firstname':'Bob'}}
        output = self.constructor.get_last_nested_child(data)
        self.assertEqual(output[-1], {'firstname':'Bob'})


if __name__ == '__main__':
    unittest.main()