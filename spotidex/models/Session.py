from typing import List, Optional, Tuple

from .spotifyTrack import SpotifyTrack


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
    
    def get_previous(self) -> Tuple[str, Optional[SpotifyTrack]]:
        return self.__retrieve_track(self.__index - 1)
    
    def get_next(self) -> Tuple[str, Optional[SpotifyTrack]]:
        return self.__retrieve_track(self.__index + 1)
    
    def __retrieve_track(self, index) -> Tuple[str, Optional[SpotifyTrack]]:
        
        if not self.__tracks:
            return "No tracks played yet.", None
        
        if 0 <= index < len(self.__tracks):
            self.__index = index
            return f"At track {index + 1} of {len(self.__tracks)}", self.__tracks[index]
        elif index < 0:
            return "Reached start of playback session", None
        else:
            return "Reached most recent track.", None
    
    def add_track(self, track: SpotifyTrack) -> None:
        
        for index, t in enumerate(self.__tracks):
            if t == track:
                self.__tracks[index] = track
        
        self.__tracks.append(track)
        self.__index = len(self.__tracks) - 1
