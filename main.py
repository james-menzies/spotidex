import logging
import sys
import os

from spotidex.models.spotifyAuth import SpotifyAuth
from spotidex.views.login_screen import LoginScreen
from spotidex.views.main_menu import MainMenu
from spotidex.views.terminal_wrapper import TerminalWrapper

sys.tracebacklimit = 0
logging.disable(sys.maxsize)
sys.stderr = open(os.devnull, "w")
sys.stdout = open(os.devnull, "w")

auth = SpotifyAuth.get_instance()

if auth.current_user:
    starting_screen = MainMenu()
else:
    starting_screen = LoginScreen()

try:
    TerminalWrapper.start_application(starting_screen)
except KeyboardInterrupt:
    TerminalWrapper.clean_resources()