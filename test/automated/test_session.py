import unittest

from spotidex.models.session import Session


class TestSession(unittest.TestCase):
    
    def setUp(self):
        Session._Session__instance = None
        self.session = Session.get_instance()
    
    def test_empty_session(self):
        self.assertEqual(self.session.current_index, 0, "Index should always be zero on empty session.")
        result = self.session.get_next()
        self.assertIsNone(result, "Empty session should return None on get_next call")
        self.assertEqual(self.session.current_index, 0, "Index should always be zero on empty session.")
        result = self.session.get_previous()
        self.assertIsNone(result, "Empty session should return None on get_previous call")
        self.assertEqual(self.session.current_index, 0, "Index should always be zero on empty session.")
