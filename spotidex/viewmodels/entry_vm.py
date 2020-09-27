from typing import Callable

from spotidex.models.spotifyAuth import SpotifyAuth
from spotidex.views.subviews import *


class EntryVM:
    
    def __init__(self):
        
        self.__callback = SpotifyAuth.get_instance().currently_playing
        self.__current_song_data = None
        self.__last_refresh_request = None
    
    @property
    def last_refresh_request(self) -> dict:
        return self.__last_refresh_request
    
    @property
    def sub_views(self) -> List[BaseSubView]:
        return [BaseSubView("View 1"), BaseSubView("View 2")]
    
    @property
    def main_view(self) -> BaseSubView:
        return ClassicalInfoSubView()
    
    def refresh_data(self, write_func: Callable) -> None:
        new_song_data = self.__callback().information
        if new_song_data != self.__current_song_data:
            self.__current_song_data = new_song_data
            self.__last_refresh_request = new_song_data
        else:
            self.__last_refresh_request = None
        
        write_func("Updated.")
