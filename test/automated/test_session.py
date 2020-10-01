import unittest

from spotidex.models.session import Session


class TestStub:
    pass

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
    
    def test_session_traversal(self):
        
        self.session.add_track(3)
        self.session.add_track(2)
        self.session.add_track(5)
        self.assertEqual(3, self.session.current_index, "After one addition, current index should equal one")
        self.assertEqual(self.session.get_previous(), 2, "First previous retrieval [ 3, [2], 5 ]")
        self.session.get_previous()
        self.assertEqual(self.session.get_previous(), None, "After hitting beginning of session should return None")
        self.assertEqual(self.session.get_next(), 2, "Testing get next")
        self.session.add_track(10)
        self.assertEqual(self.session.current_index, 4, "After adding another track, should snap to most current.")
    
    def test_duplicate_addition(self):
        
        stub = TestStub()
        stub.information = None
        
        self.session.add_track(2)
        self.session.add_track(1)
        self.session.add_track(2)
        self.assertEqual(3, self.session.current_index, "non consecutive duplicates are added")
        self.session.add_track(2)
        self.assertEqual(3, self.session.current_index, "consecutive duplicate not added")
        
        
