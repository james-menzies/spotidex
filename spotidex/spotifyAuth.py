from spotipy import Spotify
from spotipy.oauth2 import SpotifyPKCE, SpotifyOauthError, SpotifyException
import os
import json


class SpotifyAuth:

    __instance = None
    __cache_path = "test/resources/valid_cache"

    @staticmethod
    def getInstance():
        if SpotifyAuth.__instance == None:
            SpotifyAuth.__instance = SpotifyAuth()
        return SpotifyAuth.__instance

    def __init__(self):
        if SpotifyAuth.__instance:
            raise ValueError("There can only be one instance of SpotifyAuth")
        
        self.__pkce = self.__init__pkce()
        self.__endpoint = None
        self.__current_user = self.__init_current_user()
        

    def __init__pkce(self) -> SpotifyPKCE:
        scope = "user-read-currently-playing"
        client_id = os.getenv("SPOTIDEX_CLIENT_ID")
        redirect_uri = "http://localhost:8080/"
        
        return SpotifyPKCE(
            client_id=client_id, redirect_uri=redirect_uri, scope=scope,cache_path=SpotifyAuth.__cache_path )


    def __init_current_user(self) -> str:
        cache_path = self.__pkce.cache_path
        if os.path.exists(cache_path):
            with open(cache_path, "r") as cache_file:
                cache_data = json.load(cache_file)
                if "logged_in_user" in cache_data:
                    return cache_data["logged_in_user"]


    @property
    def current_user(self) -> str:
        return self.__current_user

    @property
    def endpoint(self) -> Spotify:
        if not self.__endpoint:
            self.__logged_in = self.establish_connection()
        
        self.__logged_in = True
        return self.__endpoint


    def establish_connection(self):
        self.__endpoint = Spotify(auth_manager=self.__pkce)
        validated = False
        while not validated:
            try:
                self.__current_user = self.__endpoint.current_user()["display_name"]
                validated = True
                self.update_user_in_cache(self.__current_user)
              
            except (SpotifyOauthError, KeyboardInterrupt):
                # user fails or cancels login
                print("User authorization failed.")
                self.__endpoint = None
                return None
            except:
                print("Spotify auth token cache was invalid")
                os.remove(self.__pkce.cache_path)
    

    def update_user_in_cache(self, current_user: str):

        cache_path = self.__pkce.cache_path

        with open(cache_path, "r") as cache_file:
            cache_data = json.load(cache_file)
            cache_data["logged_in_user"] = current_user
        
        with open(cache_path, "w") as cache_file:
            json.dump(cache_data, cache_file)
