import unittest
import json

from spotidex.models.spotifyTrack import SpotifyTrack


class TestSpotifyTrack(unittest.TestCase):
    
    def setUp(self):
        self.blank1 = SpotifyTrack("")
        self.blank2 = SpotifyTrack("")
        with open("test/resources/test_tracks.txt") as raw_data:
            self.equal1 = SpotifyTrack("")
            self.equal1._SpotifyTrack__information = json.loads(raw_data.readline().strip())
            self.equal2 = SpotifyTrack("")
            self.equal2._SpotifyTrack__information = json.loads(raw_data.readline().strip())
            self.non_equal = SpotifyTrack("")
            self.non_equal._SpotifyTrack__information = json.loads(raw_data.readline().strip())
        
            
            # self.equal_2 = SpotifyTrack(json.loads(raw_data.readline().strip()))
            # self.non_equal = SpotifyTrack(json.loads(raw_data.readline().strip()))
    
    def test_equals(self):
        self.assertEqual(self.blank1, self.blank2, "Two Spotify Tracks with empty information should be equal.")
        self.assertNotEqual(self.blank1, self.equal1, "blank should not equal normal track")
        self.assertEqual(self.equal1, self.equal2, "Two Spotify Tracks with same ID should be equal")
        self.assertNotEqual(self.equal2, self.non_equal, "Spotify with differing IDs are not equal")
