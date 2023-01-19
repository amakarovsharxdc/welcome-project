import unittest
from src.main import DataConstructor, EmptyNode, EmptyNodes


class Testtest_DataConstructor(unittest.TestCase):

    def setUp(self):
        self.constructor = DataConstructor()

        self.example_input1 = [("GET", "/api/v1/cluster/metrics"),
                               ("POST", "/api/v1/cluster/{cluster}/plugins"),
                               ("POST", "/api/v1/cluster/{cluster}/plugins/{plugin}")]

        self.example_output1 = {'cluster':
                                {'metrics': 'GET',
                                 'plugins': 'POST'}
                                }

        self.example_input2 = [("GET", "/api/v1/cluster/freenodes/list"),
                               ("GET", "/api/v1/cluster/nodes"),
                               ("POST",
                                "/api/v1/cluster/{cluster}/plugins/{plugin}"),
                               ("POST", "/api/v1/cluster/{cluster}/plugins")]

        self.example_output2 = {'cluster':
                                {'metrics': 'GET',
                                 'plugins': 'POST',
                                 'freenodes': {'list': 'GET'},
                                 'nodes': 'GET'
                                 }
                                }

    def test_example1_success(self):
        output = self.constructor.construct(self.example_input1)
        self.assertDictEqual(output, self.example_output1)

    def test_example2_success(self):
        self.constructor.output = self.constructor.construct(
            self.example_input1)
        output2 = self.constructor.construct(self.example_input2)
        self.assertDictEqual(output2, self.example_output2)

    def test_example1_failure(self):
        test_data = [("GET", "/api/v1/cluster"),
                ("POST", "/api/v1/cluster/{cluster}"),
                ("POST", "/api/v1/cluster/{cluster}")]
        self.assertRaises(EmptyNodes,  self.constructor.construct, test_data)
       
