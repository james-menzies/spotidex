import unittest
from spotidex.views.subviews import *

class TestSubviews(unittest.TestCase):
    
    def setUp(self):
        self.data = {
            "test": {
                "apple": 1,
                "banana": 2,
            },
            "test2": {
                "mango": 4,
                "peach": 3
            }
        }
    
    def test_get_data_section(self):
        
        result = BaseSubView._get_data_section(self.data, "test")
        self.assertIsNotNone(result, "data should return when given correct key")
        result = BaseSubView._get_data_section(self.data, "wrong")
        self.assertIsNone(result, "None should be return when incorrect key given.")
        result = BaseSubView._get_data_section(self.data, "test2", ["mango"])
        self.assertIsNotNone(result, "data should return when key and attribute present")
        
        
        
        