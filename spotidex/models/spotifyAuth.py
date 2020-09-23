import json
import os
from typing import Callable

from spotipy import Spotify
from spotipy.oauth2 import SpotifyPKCE, SpotifyOauthError

from .spotifyTrack import SpotifyTrack


class SpotifyAuth:
    __instance = None
    __cache_path = ".cache"
    
    @staticmethod
    def get_instance():
        if not SpotifyAuth.__instance:
            SpotifyAuth.__instance = SpotifyAuth()
        return SpotifyAuth.__instance
    
    def __init__(self):
        if SpotifyAuth.__instance:
            raise ValueError("There can only be one instance of SpotifyAuth")
        
        self.__pkce = self.__init__pkce()
        self.__endpoint = Spotify(auth_manager=self.__pkce)
        self.__current_user = self.__init_current_user()
        self.__connected = False
    
    def __init__pkce(self) -> SpotifyPKCE:
        scope = "user-read-currently-playing"
        redirect_uri = "http://localhost:8080/"
        
        return SpotifyPKCE(
            redirect_uri=redirect_uri, scope=scope, cache_path=self.__cache_path)
    
    def __init_current_user(self) -> str:
        cache_path = self.__cache_path
        if os.path.exists(cache_path):
            with open(cache_path, "r") as cache_file:
                cache_data = json.load(cache_file)
                if "logged_in_user" in cache_data:
                    return cache_data["logged_in_user"]
        
        return ""
    
    @property
    def current_user(self) -> str:
        """
        The current user, will be None if no user is logged in
        """
        
        return self.__current_user
    
    @property
    def currently_playing(self) -> Callable[[], SpotifyTrack]:
        """
        Will attempt to connect if not currently connected. However it is recommended
        to call the establish_connection method beforehand, as failure to do so will
        result in an exception being raised.
        """
        if not self.__connected and not self.establish_connection():
            raise ValueError("Unable to establish current user, can't provide callback.")
        else:
            return lambda: self.__endpoint.currently_playing()
    
    def establish_connection(self) -> bool:
        """
        Establishes a connection by calling a function on the spotify endpoint.
        It then runs through all the necessary subroutines to ensure the correct
        properties are exposed and that the cache data is valid.
        """
        
        while not self.__connected:
            try:
                self.__current_user = self.__endpoint.current_user()["display_name"]
                self.__update_user_in_cache(self.__current_user)
                self.__connected = True
            except (SpotifyOauthError, KeyboardInterrupt):
                # user cancels login, abort connection
                print("User has cancelled Spotify authorization.")
                self.__endpoint = None
                return False
            except:
                # Likely some error involving the cached token.
                # There are too many to specify, so it must be a catch all.
                # Loop will run again to correct issue.
                if os.path.exists(self.__cache_path):
                    os.remove(self.__cache_path)
                # If there isn't a cache, some other error has occurred. Must abort.
                else:
                    raise Exception("Unknown error occurred attempting to connect to Spotify.")
        
        return True
    
    def __update_user_in_cache(self, current_user: str) -> None:
        """
        Will update the cache file to include the user associated. 
        May throw errors so should be surrounded in a try block.
        """
        
        cache_path = self.__pkce.cache_path
        
        with open(cache_path, "r") as cache_file:
            cache_data = json.load(cache_file)
            cache_data["logged_in_user"] = current_user
        
        with open(cache_path, "w") as cache_file:
            json.dump(cache_data, cache_file)
