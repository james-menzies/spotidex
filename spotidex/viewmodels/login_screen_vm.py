import os
import sys

from spotidex.models.spotifyAuth import SpotifyAuth


class LoginScreenVM:
    def __init__(self):
        self.__auth = SpotifyAuth.get_instance()
        self.success = False
        self.message = ""
    
    def login(self):
        try:
            sys.stderr = open(os.devnull, "w")
            
            if self.__auth.establish_connection():
                self.success = True
                self.message = f"Welcome, {self.__auth.current_user}!"
            else:
                self.success = False
                self.message = "Login cancelled by user"
        except Exception:
                self.success = False
                self.message = "An unknown login error occurred."
        finally:
            sys.stderr = sys.__stderr__
            print("Login attempt completed.")
