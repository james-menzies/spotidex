import logging
import os
import sys

from spotidex.models.spotifyAuth import SpotifyAuth
from spotidex.views.login_screen import LoginScreen
from spotidex.views.main_menu import MainMenu
from spotidex.views.terminal_wrapper import TerminalWrapper

sys.tracebacklimit = 0
logging.disable(sys.maxsize)

auth = SpotifyAuth.get_instance()

if auth.current_user:
    starting_screen = MainMenu()
else:
    starting_screen = LoginScreen()

TerminalWrapper.start_application(starting_screen)
