from spotidex.models.spotifyAuth import SpotifyAuth


class MainMenuVM():
    
    def __init__(self):
        self.__auth = SpotifyAuth.get_instance()
        self.__welcome_message = f"Welcome, {self.__auth.current_user}!"
    
    
    