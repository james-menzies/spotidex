import os
import sys

from spotidex.models.spotifyAuth import SpotifyAuth


class LoginScreenVM:
    def __init__(self):
        self.__auth = SpotifyAuth.get_instance()
    
    def login(self):
        try:
            sys.stderr = open(os.devnull, "w")
            if self.__auth.establish_connection():
                return True, f"Welcome, {self.__auth.current_user}!"
            else:
                return False, "Login cancelled by user"
        except Exception:
            return False, "An unknown error occurred."
        finally:
            sys.stderr = sys.__stderr__
