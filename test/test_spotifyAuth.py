import unittest
from spotidex.spotifyAuth import SpotifyAuth

class test_example(unittest.TestCase):

    def setUp(self):
        SpotifyAuth._SpotifyAuth__instance = None
        SpotifyAuth._SpotifyAuth__cache_path = "invalid/file/path"
    
    def test_user_exists_valid_cache(self):
        SpotifyAuth._SpotifyAuth__cache_path = "test/resources/valid_cache"
        auth = SpotifyAuth.get_instance()        
        self.assertEqual("redbrickhut", auth.current_user, "user redbrickhut should be logged in")

    def test_no_cache_no_current_user(self):
        auth = SpotifyAuth.get_instance()
        self.assertIsNone(auth.current_user, "no cache should mean that there is no current user")

    def test_invalid_cache_fails(self):
        SpotifyAuth._SpotifyAuth__cache_path = "test/resources/invalid_cache"
        auth = SpotifyAuth.get_instance()
        # TODO write remainder        

