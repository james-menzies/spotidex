from typing import List, Optional, Tuple, Protocol, TypeVar

from .spotifyTrack import SpotifyTrack

T = TypeVar('T')


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
        
        self.__tracks: List[T] = []
        self.__current_index = -1
    
    @property
    def current_index(self):
        return self.__current_index + 1  # human readable
    
    def get_previous(self) -> Tuple[str, Optional[T]]:
        return self.__retrieve_track(self.__current_index - 1)
    
    def get_next(self) -> Tuple[str, Optional[T]]:
        return self.__retrieve_track(self.__current_index + 1)
    
    def __retrieve_track(self, index) -> Optional[T]:
        
        if not self.__tracks:
            return None
        
        if 0 <= index < len(self.__tracks):
            self.__current_index = index
            return self.current_index
        elif index < 0:
            return None
        else:
            return None
    
    def add_track(self, track: T) -> None:
        
        for index, t in enumerate(self.__tracks):
            if t == track:
                self.__tracks[index] = track
        if not self.__tracks or not self.__tracks[-1] == track:
            self.__tracks.append(track)
        self.__current_index = len(self.__tracks) - 1
