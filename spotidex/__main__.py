import logging
import os
import sys
import pathlib

from spotidex.models.spotifyAuth import SpotifyAuth
from spotidex.views.login_screen import LoginScreen
from spotidex.views.main_menu import MainMenu
from spotidex.views.terminal_wrapper import TerminalWrapper


def main(args=None):
    
    logging.disable(sys.maxsize)
    sys.stderr = open(os.devnull, "w")
    sys.stdout = open(os.devnull, "w")
    os.environ["SPOTIPY_CLIENT_ID"] = "711661c6916a4a9981244380aa852adc"
    sys.path.insert(0, str(pathlib.Path(__file__).parents[1]))
    
    
    auth = SpotifyAuth.get_instance()
    
    if auth.current_user:
        starting_screen = MainMenu()
    else:
        starting_screen = LoginScreen()
    
    try:
        TerminalWrapper.start_application(starting_screen)
    except KeyboardInterrupt:
        TerminalWrapper.clean_resources()


if __name__ == "__main__":
    sys.exit(main())
