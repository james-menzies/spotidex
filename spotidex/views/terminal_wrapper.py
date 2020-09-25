import urwid
from typing import Protocol
from .login_screen import LoginScreen


class View(Protocol):
    def get_widget(self) -> urwid.Widget:
        ...


class TerminalWrapper:
    __palette = {
        ('bg', 'dark green', 'black', ),
        ('reversed', 'black', 'white', ),
    }
    __placeholder = urwid.SolidFill()
    __title = urwid.Text("Spotidex v1.0", align='left')
    __frame = urwid.Frame(__placeholder, header=__title)

    __loop = urwid.MainLoop(__frame, palette=__palette )
    
    @classmethod
    def start_application(cls, initial_screen: View) -> None:
        cls.__loop.widget = urwid.AttrMap(initial_screen.get_widget(), 'bg')
        
        cls.__loop.run()
    
    @classmethod
    def change_screen(cls, view: View):
        cls.__loop.widget = view.get_widget()
