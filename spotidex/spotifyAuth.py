from spotipy import Spotify
from spotipy.oauth2 import SpotifyPKCE, SpotifyOauthError
import os


class SpotifyAuth:

    __instance = None

    @staticmethod
    def getInstance():
        if SpotifyAuth.__instance == None:
            SpotifyAuth.__instance = SpotifyAuth()
        return SpotifyAuth.__instance

    def __init__(self):
        if SpotifyAuth.__instance:
            raise ValueError("There can only be one instance of SpotifyAuth")
        self.__current_user = None

    def __init__pkce(self) -> SpotifyPKCE:
        scope = "user-read-currently-playing"
        client_id = os.getenv("SPOTIDEX_CLIENT_ID")
        redirect_uri = "http://localhost:8080/"
        
        return SpotifyPKCE(
            client_id=client_id, redirect_uri=redirect_uri, scope=scope)

    @property
    def logged_in(self) -> bool:
        return self.__logged_in
    
    @property
    def current_user(self) -> str:
        return self.__current_user

    @property
    def endpoint(self) -> Spotify:
        if not self.__endpoint:
            self.__endpoint = Spotify(auth_manager=self.__pkce)
            
            try:
                self.__current_user = self.__endpoint.current_user()
            except SpotifyOauthError:
                print("User authorization failed.")
                self.__endpoint = None
                return None
        
        self.__logged_in = True
        return self.__endpoint
