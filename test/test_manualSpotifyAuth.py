import unittest
from spotidex.spotifyAuth import SpotifyAuth

class ManualAuthorization(unittest.TestCase):

    def test_manual_attempt(self):

        auth = SpotifyAuth.get_instance()
        connected = auth.establish_connection()
        if connected:
            self.assertTrue(auth.current_user)