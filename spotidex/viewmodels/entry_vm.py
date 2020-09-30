import time
from threading import Lock, Thread
from typing import Callable

from spotidex.models.Session import Session
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
        self.__automatic_refresh: bool = True
        self.__refresh_killed: bool = False
    
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
        return [ComposerWikiSubView(), WorkWikiSubView(), RecommendedSubView(), RawInfoSubView()]
    
    @property
    def main_view(self) -> BaseSubView:
        return ClassicalInfoSubView()
    
    def toggle_automatic_refresh(self) -> bool:
        self.__auto_lock.acquire()
        self.__automatic_refresh = not self.__automatic_refresh
        final = self.__automatic_refresh
        self.__auto_lock.release()
        return final
    
    def kill_refresh(self):
        self.__auto_lock.acquire()
        self.__refresh_killed = True
        self.__auto_lock.release()
    
    def next(self, write_func: Callable):
        self.prev_or_next(write_func)
    
    def previous(self, write_func: Callable):
        self.prev_or_next(write_func, get_next=False)
    
    def prev_or_next(self, write_func: Callable, get_next: bool = True):
        
        self.__auto_lock.acquire()
        self.__automatic_refresh = False
        self.__auto_lock.release()
        
        self.__refresh_lock.acquire()
        if get_next:
            message, track = Session.get_instance().get_next()
        else:
            message, track = Session.get_instance().get_previous()
        if track:
            self.__matching_song_data = False
            self.__current_song_data = track.information
        
        self.__refresh_lock.release()
        write_func(message)
    
    def refresh_loop(self, write_func: Callable) -> None:
        
        self.__auto_lock.acquire()
        
        while not self.__refresh_killed:
            
            if self.__automatic_refresh:
                self.__auto_lock.release()
                self.refresh_data(write_func)
            else:
                self.__auto_lock.release()
            
            time.sleep(30)
            self.__auto_lock.acquire()
        
        self.__auto_lock.release()
    
    def refresh_data(self, write_func: Callable) -> None:
        self.__refresh_lock.acquire()
        
        self.__previous_song_data = self.__current_song_data
        self.__current_song_data = None
        self.__matching_song_data = False
        
        write_func("Refreshing...")
        try:
            current_song = self.__callback()
            self.__current_song_data = current_song.information
        except Exception:
            write_func("Can't connect to Spotify")
            return
        
        if not self.current_song_data or not self.previous_song_data:
            self.__matching_song_data = self.current_song_data == self.previous_song_data
        else:
            current_id = self.__current_song_data["basic_info"]["id"]
            prev_id = self.__previous_song_data["basic_info"]["id"]
            self.__matching_song_data = current_id == prev_id
        
        if not self.__matching_song_data:
            Session.get_instance().add_track(current_song)
        
        self.__auto_lock.acquire()
        self.__automatic_refresh = True
        self.__auto_lock.release()
        
        write_func("Updated.")
        self.__refresh_lock.release()
