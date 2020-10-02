import time
from threading import Lock, Thread
from typing import Callable


from models.spotifyTrack import SpotifyTrack
from models.session import Session
from models.spotifyAuth import SpotifyAuth
from views.subviews import *


class PlayInfoVM:
    
    def __init__(self):
        
        self.__callback: Callable[[], SpotifyTrack] = SpotifyAuth.get_instance().currently_playing
        self.__current_song_data: Optional[SpotifyTrack] = None
        self.__previous_song_data: Optional[SpotifyTrack] = None
        self.__refresh_lock: Lock = Lock()
        self.__auto_lock: Lock = Lock()
        self.__automatic_refresh: bool = True
        self.__refresh_killed: bool = False
        self.__session = Session.get_instance()
    
    @property
    def current_song_data(self) -> Optional[Dict]:
        if self.__current_song_data:
            return self.__current_song_data.information
        else:
            return None
    
    @property
    def sub_views(self) -> List[BaseSubView]:
        return [ComposerWikiSubView(), WorkWikiSubView(), RecommendedSubView(), RawInfoSubView()]
    
    @property
    def main_view(self) -> BaseSubView:
        return ClassicalInfoSubView()
    
    @property
    def automatic_refresh(self) -> bool:
        self.__auto_lock.acquire()
        val = self.__automatic_refresh
        self.__auto_lock.release()
        
        return val
    
    @automatic_refresh.setter
    def automatic_refresh(self, value: bool) -> None:
        self.__auto_lock.acquire()
        self.__automatic_refresh = value
        self.__auto_lock.release()
    
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
        
        self.__previous_song_data = None
        self.__current_song_data = None
        
        self.__refresh_lock.acquire()
        if get_next:
            track = self.__session.get_next()
        else:
            track = self.__session.get_previous()
        
        if track:
            self.__current_song_data = track
            message = f"At track # {self.__session.current_index} of {self.__session.size}"
        elif get_next:
            message = "Reached end of playback"
        else:
            message = "Reached start of playback"
        
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
        
        write_func("Refreshing...")
        try:
            new_song = self.__callback()
        except Exception:
            write_func("Can't connect to Spotify. Check internet connection...")
            self.__refresh_lock.release()
            return
        
        if new_song != self.__previous_song_data:
            self.__current_song_data = new_song
        
        if self.__current_song_data and self.__current_song_data.information:
            Session.get_instance().add_track(self.__current_song_data)
        
        self.__auto_lock.acquire()
        self.__automatic_refresh = True
        self.__auto_lock.release()
        
        write_func("Updated.")
        self.__refresh_lock.release()
