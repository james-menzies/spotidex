import os
import sys

from models.spotifyAuth import SpotifyAuth
from threading import Lock


class LoginScreenVM:
    def __init__(self):
        self.__auth = SpotifyAuth.get_instance()
        self.success = False
        self.lock = Lock()
    
    def login(self, write_func):
        
        if self.lock.locked():
            write_func("Please only attempt one login at a time.")
            return
        
        self.lock.acquire()
        old_stderr = sys.stderr
        sys.stderr = open(os.devnull, "w")

        if self.success:
            write_func("You are already logged in!")
            return
        
        try:
            if self.__auth.establish_connection():
                self.success = True
                write_func(f"Welcome, {self.__auth.current_user}!")
            else:
                self.success = False
                write_func("Login cancelled by user")
        except Exception:
            self.success = False
            write_func("An unknown login error occurred.")
        finally:
            self.lock.release()
            sys.stderr = old_stderr
