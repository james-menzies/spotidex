import unittest
import os
from spotidex.models.spotifyAuth import SpotifyAuth 


class ManualAuthorization(unittest.TestCase):

    cache_path = "test/resources/manual_test_cache"

    def setUp(self):
        SpotifyAuth._SpotifyAuth__instance = None
        SpotifyAuth._SpotifyAuth__cache_path = self.cache_path

    def test_manual_attempt(self):

        auth = SpotifyAuth.get_instance()
        connected = auth.establish_connection()
        if connected:
            self.assertTrue(auth.current_user, "Current user should be available on successful connection.")
            self.assertTrue(self.user_still_logged_in(), "User should still be logged in on subsequent program launch.")
        else:
            self.assertTrue(auth.current_user, "Current user should equal None when connection unsuccessful.")
        
    def user_still_logged_in(self):
        self.setUp()
        auth = SpotifyAuth.get_instance()
        return auth.current_user
    
    def tearDown(self):
        if os.path.exists(self.cache_path):
            os.remove(self.cache_path)
