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
        return [BaseSubView("""
        View 1
        "On the other hand, we denounce with righteous indignation and dislike men who are so beguiled and demoralized by the charms of pleasure of the moment, so blinded by desire, that they cannot foresee the pain and trouble that are bound to ensue; and equal blame belongs to those who fail in their duty through weakness of will, which is the same as saying through shrinking from toil and pain. These cases are perfectly simple and easy to distinguish. In a free hour, when our power of choice is untrammelled and when nothing prevents our being able to do what we like best, every pleasure is to be welcomed and every pain avoided. But in certain circumstances and owing to the claims of duty or the obligations of business it will frequently occur that pleasures have to be repudiated and annoyances accepted. The wise man therefore always holds in these matters to this principle of selection: he rejects pleasures to secure other greater pleasures, or else he endures pains to avoid worse pains."
        
        "On the other hand, we denounce with righteous indignation and dislike men who are so beguiled and demoralized by the charms of pleasure of the moment, so blinded by desire, that they cannot foresee the pain and trouble that are bound to ensue; and equal blame belongs to those who fail in their duty through weakness of will, which is the same as saying through shrinking from toil and pain. These cases are perfectly simple and easy to distinguish. In a free hour, when our power of choice is untrammelled and when nothing prevents our being able to do what we like best, every pleasure is to be welcomed and every pain avoided. But in certain circumstances and owing to the claims of duty or the obligations of business it will frequently occur that pleasures have to be repudiated and annoyances accepted. The wise man therefore always holds in these matters to this principle of selection: he rejects pleasures to secure other greater pleasures, or else he endures pains to avoid worse pains."
        
        "On the other hand, we denounce with righteous indignation and dislike men who are so beguiled and demoralized by the charms of pleasure of the moment, so blinded by desire, that they cannot foresee the pain and trouble that are bound to ensue; and equal blame belongs to those who fail in their duty through weakness of will, which is the same as saying through shrinking from toil and pain. These cases are perfectly simple and easy to distinguish. In a free hour, when our power of choice is untrammelled and when nothing prevents our being able to do what we like best, every pleasure is to be welcomed and every pain avoided. But in certain circumstances and owing to the claims of duty or the obligations of business it will frequently occur that pleasures have to be repudiated and annoyances accepted. The wise man therefore always holds in these matters to this principle of selection: he rejects pleasures to secure other greater pleasures, or else he endures pains to avoid worse pains."
        """), BaseSubView("View 2")]
    
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
