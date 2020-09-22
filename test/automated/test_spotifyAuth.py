import unittest
import os
from spotidex.spotifyAuth import SpotifyAuth #pylint: disable=import-error
from shutil import copyfile
from spotipy import Spotify

class PassingEndpoint:
    """
    An endpoint which unconditionally simulates
    a valid login attempt.
    """

    def current_user(self):
        return {
            "display_name": "sample_user"
        }

class FailingEndpoint:
    """
    This class will legitmately try to reach Spotify with
    an invalid token, then will abort any subsequent attempts.
    """

    def __init__(self, endpoint : Spotify):
        self.first_attempt = True
        self.endpoint = endpoint
    
    def current_user(self):

        if self.first_attempt:
            self.first_attempt = False
            return self.endpoint.current_user()
        else:
            # simulates cancelled action
            raise KeyboardInterrupt()


class test_example(unittest.TestCase):

    def setUp(self):
        SpotifyAuth._SpotifyAuth__instance = None
        SpotifyAuth._SpotifyAuth__cache_path = ""
        

    def test_user_exists_valid_cache(self):
        SpotifyAuth._SpotifyAuth__cache_path = "test/resources/valid_cache"
        auth = SpotifyAuth.get_instance()        
        self.assertEqual("redbrickhut", auth.current_user, "user redbrickhut should be logged in")


    def test_simulate_correct_login(self):
        cache_path = "test/resources/simulated_cache"
        SpotifyAuth._SpotifyAuth__cache_path = cache_path

        with open(cache_path, "w+") as cache_file:
            cache_file.write("{}")

        auth = SpotifyAuth.get_instance()
        self.assertIsNone(auth.current_user, "no cache should mean that there is no current user")
        auth._SpotifyAuth__endpoint = PassingEndpoint()
        self.assertEqual(True, auth.establish_connection(), "Connection should be established with mock endpoint")
        self.assertEqual("sample_user", auth.current_user, "User should match one provided by mock endpoint ")

        os.remove("test/resources/simulated_cache")


    def test_invalid_cache_fails(self):
        cache_path = "test/resources/invalid_cache"
        cache_backup_path = "test/resources/_invalid_cache"
        copyfile(cache_path, cache_backup_path)

        SpotifyAuth._SpotifyAuth__cache_path = cache_path
        auth = SpotifyAuth.get_instance()
        auth._SpotifyAuth__endpoint = FailingEndpoint(auth._SpotifyAuth__endpoint)
        self.assertFalse(auth.establish_connection(), "user should not be connected")
        self.assertFalse(os.path.exists("test/resources/invalid_cache"), "invalid cache should be removed.")
        os.rename(cache_backup_path, cache_path)
