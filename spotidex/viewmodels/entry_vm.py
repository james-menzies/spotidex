import time
from threading import Lock, Thread
from typing import Callable

from spotidex.models.spotifyAuth import SpotifyAuth
from spotidex.views.subviews import *


class EntryVM:
    
    def __init__(self):
        
        self.__callback = SpotifyAuth.get_instance().currently_playing
        self.__current_song_data = None
        self.__previous_song_data = None
        self.__matching_song_data = False
        self.__refresh_lock: Lock = Lock()
        self.__auto_lock: Lock = Lock()
        self.__automatic_refresh: bool = False
        self.__refresh_loop_running: bool = False
    
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
    
    def toggle_automatic_refresh(self, write_func: Callable) -> None:
        
        self.__auto_lock.acquire()
        self.__automatic_refresh = not self.__automatic_refresh
        if self.__automatic_refresh and not self.__refresh_loop_running:
            self.__refresh_loop_running = True
            thread: Thread = Thread(target=self.refresh_loop, args=(write_func,))
            thread.start()
            
        self.__auto_lock.release()
    
    def refresh_loop(self, write_func: Callable) -> None:
        
        self.__auto_lock.acquire()
        while self.__automatic_refresh:
            
            self.__auto_lock.release()
            
            self.refresh_data(write_func)
            time.sleep(30)
            self.__auto_lock.acquire()
        self.__refresh_loop_running = False
        self.__refresh_lock.release()
    
    def refresh_data(self, write_func: Callable) -> None:
        self.__refresh_lock.acquire()
        
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
        self.__refresh_lock.release()
