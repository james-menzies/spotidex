import os
import sys
from typing import Tuple, Callable

from spotidex.models.spotifyAuth import SpotifyAuth


class LoginScreenVM:
    def __init__(self):
        self.__auth = SpotifyAuth.get_instance()
        self.success = False
        self.message = ""
    
    def login(self, write_func, close_pipe ):
       
        try:
            sys.stderr = open(os.devnull, "w")
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
            sys.stderr = sys.__stderr__
            close_pipe()
