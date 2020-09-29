from typing import Callable

from spotidex.models.spotifyAuth import SpotifyAuth
from spotidex.views.subviews import *


class EntryVM:
    
    def __init__(self):
        
        self.__callback = SpotifyAuth.get_instance().currently_playing
        self.__current_song_data = None
        self.__previous_song_data = None
        self.__matching_song_data = False
    
    @property
    def current_song_data(self) -> dict:
        return self.__current_song_data
    
    @property
    def previous_song_data(self) -> dict:
        return self.__previous_song_data
    
    @property
    def matching_song_data(self) -> bool:
        return self.__matching_song_data
    
    @property
    def sub_views(self) -> List[BaseSubView]:
        return [RawInfoSubView(), ClassicalInfoSubView()]
    
    @property
    def main_view(self) -> BaseSubView:
        return ClassicalInfoSubView()
    

    
    def refresh_data(self, write_func: Callable) -> None:
        
        self.__previous_song_data = self.__current_song_data
        self.__current_song_data = None
        self.__matching_song_data = False
        
        write_func("Refreshing...")
        
        self.__current_song_data = self.__callback().information
        if not self.current_song_data or not self.previous_song_data:
            self.__matching_song_data = self.current_song_data == self.previous_song_data
        else:
            current_id = self.__current_song_data["basic_info"]["id"]
            prev_id = self.__previous_song_data["basic_info"]["id"]
            self.__matching_song_data = current_id == prev_id
            
        write_func("Updated.")
