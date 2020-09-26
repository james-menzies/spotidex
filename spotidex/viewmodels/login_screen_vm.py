import os
import sys
import time

from spotidex.models.spotifyAuth import SpotifyAuth
from threading import Lock
from .utils import flash_message


class LoginScreenVM:
    def __init__(self):
        self.__auth = SpotifyAuth.get_instance()
        self.success = False
        self.message = ""
        self.lock = Lock()
    
    def login(self, write_func):
        
        if self.lock.locked():
            flash_message("Please only attempt one login at a time.", write_func)
            return
        
        self.lock.acquire()
        
        if self.success:
            flash_message("You are already logged in!", write_func)
            return
        
        try:
            sys.stderr = open(os.devnull, "w")
            if self.__auth.establish_connection():
                self.success = True
                flash_message(f"Welcome, {self.__auth.current_user}!", write_func)
            else:
                self.success = False
                flash_message("Login cancelled by user", write_func)
        except Exception:
            self.success = False
            flash_message("An unknown login error occurred.", write_func)
        finally:
            sys.stderr = sys.__stderr__
            self.lock.release()
