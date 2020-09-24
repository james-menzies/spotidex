import urwid
from typing import Protocol
from .login_screen import LoginScreen


class View(Protocol):
    def get_widget(self) -> urwid.Widget:
        ...


class TerminalWrapper:
    __placeholder = urwid.SolidFill()
    __title = urwid.Text("Spotidex v1.0", align='left')
    __frame = urwid.Frame(__placeholder, header=__title)
    __loop = urwid.MainLoop(__frame)
    
    @classmethod
    def start_application(cls, logged_in: bool = False) -> None:
        cls.__loop.widget = LoginScreen().get_widget()
        cls.__loop.run()
    
    @classmethod
    def change_screen(cls, view: View):
        cls.__loop.widget = view.get_widget()
