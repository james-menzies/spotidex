from spotidex.models.spotifyAuth import SpotifyAuth
from .components import Menu, Choice
from .terminal_wrapper import TerminalWrapper
import urwid


class MainMenu:
    
    def __init__(self):
        self.__auth = SpotifyAuth.get_instance()
        message = f"Welcome, {self.__auth.current_user}!"
        
        choices = [
            Choice("Begin Session", self.begin, """
            Start your Spotify session now!
            """),
            Choice("Settings", self.settings, """
            Customize your Spotidex experience.
            """),
            Choice("Log out", self.logout, """
            Log out of Spotidex, note you will need to re-authenticate to re-use.
            """),
        ]
        
        menu = Menu("Main Menu")
        menu.add_text(urwid.Text(message))
        menu.add_choice_block(choices, description=True)
        self.__widget = menu.build()
    
    def settings(self, button):
        pass
    
    def begin(self, button):
        pass
    
    def logout(self, button):
        pass
    
    @property
    def widget(self):
        return self.__widget
