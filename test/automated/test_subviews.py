import unittest
from spotidex.views.subviews import *


class TestSubviews(unittest.TestCase):
    """
    These test are mostly to ensure that graphics are rendered
    when the data is valid and that no exceptions are thrown at
    any point (critical to make sure that the program doesn't
    crash).
    """
    
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
        self.testing_matrix = [ComposerWikiSubView, WorkWikiSubView, ClassicalInfoSubView, RawInfoSubView, RecommendedSubView]
    
    def test_get_data_section(self):
        result = BaseSubView._get_data_section(self.data, "test")
        self.assertIsNotNone(result, "data should return when given correct key")
        result = BaseSubView._get_data_section(self.data, "wrong")
        self.assertIsNone(result, "None should be return when incorrect key given.")
        result = BaseSubView._get_data_section(self.data, "test2", ["mango"])
        self.assertIsNotNone(result, "data should return when key and attribute present")
        result = BaseSubView._get_data_section(self.data, "test", ["peach"])
        self.assertIsNone(result, "Missing attribute should yield None")
        result = BaseSubView._get_data_section(result, "test2", ["mango", "banana"])
        self.assertIsNone(result, "data should still return None with partial attribute match")
    
    def test_subviews_handle_none(self):
        for view in self.testing_matrix:
            view = view()
            view.update_widget(None)
