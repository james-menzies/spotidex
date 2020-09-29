from typing import List, Optional, Tuple

from models.spotifyTrack import SpotifyTrack


class Session:
    __instance = None
    
    @staticmethod
    def get_instance():
        if not Session.__instance:
            Session.__instance = Session()
        return Session.__instance
    
    def __init__(self):
        if Session.__instance:
            raise ValueError("There can only be one instance of Session")
        
        self.__tracks: List[SpotifyTrack] = []
        self.__index = None
    
    def get_previous(self) -> Optional[SpotifyTrack]:
        return self.__retrieve_track(self.__index - 1)
    
    def get_next(self) -> Optional[SpotifyTrack]:
        return self.__retrieve_track(self.__index + 1)
    
    def __retrieve_track(self, index):
        
        if not self.__tracks:
            return None
        
        if 0 <= index < len(self.__tracks):
            self.__index = index
            return self.__tracks[index]
        else:
            return None
    
    def add_track(self, track: SpotifyTrack) -> None:
        
        for index, t in enumerate(self.__tracks):
            if t == track:
                self.__tracks[index] = track
        
        self.__tracks.append(track)
