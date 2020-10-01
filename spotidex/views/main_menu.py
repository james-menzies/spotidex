from spotidex.models.session import Session
from spotidex.models.spotifyAuth import SpotifyAuth
from .components import Menu, Choice
import urwid

from .playinfo import PlayInfo
from . import login_screen
from .terminal_wrapper import TerminalWrapper


class MainMenu:
    
    def __init__(self):
        self.__auth = SpotifyAuth.get_instance()
        message = f"Welcome, {self.__auth.current_user}!"
        
        # Menu contexts not yet implemented. Saving for future versions
        choices = [
            Choice("Begin Session", self.begin, """
            Start your Spotify session now!
            """),
            Choice("Log out", self.logout, """
            Log out of Spotidex, note you will need to re-authenticate to re-use.
            """),
            Choice("Exit Spotidex", TerminalWrapper.exit, )
        ]
        
        menu = Menu("Main Menu")
        menu.add_text(urwid.Text(message))
        menu.add_choice_block(choices, description=True)
        self.__widget = menu.build()
    
 
    def begin(self, button):

        TerminalWrapper.change_screen(PlayInfo())
        
    def logout(self, button):
        TerminalWrapper.change_screen(login_screen.LoginScreen())
        Session.get_instance().log_out()
        self.__auth.log_out()
    
    
    @property
    def widget(self):
        return self.__widget
